"""图片转换器模块"""
import os
from PIL import Image
import numpy as np

# 注册HEIF插件以支持HEIC、HEIF、AVIF格式
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_SUPPORTED = True
except ImportError:
    HEIF_SUPPORTED = False

# 注册RAW文件支持
try:
    import rawpy
    RAW_SUPPORTED = True
except ImportError:
    RAW_SUPPORTED = False

# 注册imageio支持
try:
    import imageio
    IMAGEIO_SUPPORTED = True
except ImportError:
    IMAGEIO_SUPPORTED = False


class ImageConverter:
    """图片格式转换器"""
    
    def __init__(self):
        """初始化图片转换器"""
        pass
    
    def convert(self, input_path, output_path, format_name, quality=85, bit_depth=None):
        """转换图片格式
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            format_name: 输出格式名称
            quality: JPEG/WebP质量 (1-100)
            bit_depth: 位深设置 (8, 10, 12, 16)
            
        Returns:
            tuple: (是否成功, 错误信息)
        """
        try:
            # 加载图像数据
            img_data, exif_data, dpi_info, is_raw = self._load_image_and_metadata(input_path, bit_depth)
                
            if img_data is None:
                return False, "无法加载图像文件"
            
            format_upper = format_name.upper()
            
            # 处理HEIF格式（AVIF、HEIF、HEIC）
            if format_upper in ['AVIF', 'HEIF', 'HEIC'] and HEIF_SUPPORTED:
                return self._handle_heif_format(img_data, output_path, format_upper, quality, bit_depth, is_raw)
            
            # 处理RAW文件（非HEIF格式）
            if is_raw:
                return self._handle_raw_format(img_data, output_path, format_name, quality)
            
            # 处理普通图像文件
            return self._handle_regular_format(img_data, output_path, format_name, quality, bit_depth, exif_data, dpi_info)
            
        except Exception as e:
            return False, str(e)
    
    def _handle_heif_format(self, img_data, output_path, format_upper, quality, bit_depth, is_raw):
        """处理HEIF格式转换"""
        # 对于RAW文件或numpy数组数据
        if is_raw or isinstance(img_data, np.ndarray):
            success = self._save_with_pillow_heif(img_data, output_path, format_upper, quality, bit_depth)
            return (True, "") if success else (False, "pillow_heif保存失败")
        # 对于PIL图像
        else:
            success = self._save_pil_with_pillow_heif(img_data, output_path, format_upper, quality)
            return (True, "") if success else (False, "pillow_heif保存失败")
    
    def _handle_raw_format(self, img_data, output_path, format_name, quality):
        """处理RAW文件格式转换"""
        if not IMAGEIO_SUPPORTED:
            return False, "imageio库未安装，无法保存RAW转换结果"
        
        success = self._save_numpy_array(img_data, output_path, format_name, quality)
        return (True, "") if success else (False, "numpy数组保存失败")
    
    def _handle_regular_format(self, img_data, output_path, format_name, quality, bit_depth, exif_data, dpi_info):
        """处理普通图像文件格式转换"""
        img = img_data
        format_upper = format_name.upper()
        
        # 应用位深转换
        if bit_depth is not None and bit_depth in {8, 10, 12, 16}:
            img = self._apply_bit_depth(img, bit_depth)
        
        # 处理JPEG透明度问题
        if format_upper == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # 准备保存参数
        save_kwargs = {'format': format_upper}
        
        if format_upper in ['JPEG', 'WEBP']:
            save_kwargs.update({'quality': quality, 'optimize': True})
        elif format_upper == 'PNG':
            save_kwargs['optimize'] = True
        
        # 处理HEIC格式
        if format_upper == 'HEIC':
            if not output_path.lower().endswith(('.heic', '.heics')):
                base_name = os.path.splitext(output_path)[0]
                output_path = base_name + '.heic'
            save_kwargs['format'] = 'HEIF'
            if 'quality' in save_kwargs:
                quality_val = save_kwargs['quality']
                save_kwargs['quality'] = -1 if quality_val == -1 else max(0, min(100, quality_val))
        
        # 添加DPI和EXIF信息
        if dpi_info:
            save_kwargs['dpi'] = dpi_info
        if exif_data and format_upper != 'HEIC':
            save_kwargs['exif'] = exif_data
        
        img.save(output_path, **save_kwargs)
        return True, ""
    
    def _load_image_and_metadata(self, input_path, target_bit_depth=None):
        """加载图像并提取元数据
        
        Args:
            input_path: 输入文件路径
            target_bit_depth: 目标位深 (8, 10, 12, 16)
            
        Returns:
            tuple: (图像数据, EXIF数据, DPI信息, 是否为RAW)
        """
        if self._is_raw_file(input_path):
            # 对于RAW文件，使用指定的位深或默认16位
            bit_depth = target_bit_depth if target_bit_depth is not None else 16
            img_data = self._process_raw_file(input_path, bit_depth)
            return (img_data, None, None, True) if img_data is not None else (None, None, None, False)
        
        try:
            with Image.open(input_path) as img:
                exif_data = img.getexif()
                dpi_info = img.info.get('dpi', None)
                return img.copy(), exif_data, dpi_info, False
        except Exception as e:
            print(f"加载图像错误: {e}")
            return None, None, None, False
    
    def _apply_bit_depth(self, img, bit_depth):
        """应用位深转换"""
        # 获取当前位深
        current_bit_depth = 8
        if img.mode in ('I;16', 'I;16B', 'I;16L'):
            current_bit_depth = 16
        elif img.mode == 'I':
            current_bit_depth = 32
        
        # 执行位深转换
        if current_bit_depth == bit_depth:
            return img
        
        if bit_depth == 8:
            if current_bit_depth == 16:
                # 16位转8位：先转换为numpy数组，然后除以256
                img_array = np.array(img)
                img_array = (img_array // 256).astype(np.uint8)
                # 根据原始模式确定输出模式
                if img.mode == 'L':
                    return Image.fromarray(img_array, 'L')
                elif img.mode == 'RGB':
                    return Image.fromarray(img_array, 'RGB')
                elif img.mode == 'RGBA':
                    return Image.fromarray(img_array, 'RGBA')
                elif img.mode == 'I;16':
                    # 对于I;16模式，转换为L模式（8位灰度）
                    return Image.fromarray(img_array, 'L')
                else:
                    return Image.fromarray(img_array, 'RGB')
            elif current_bit_depth == 32:
                img_array = np.array(img)
                img_array = (img_array // 16777216).astype(np.uint8)
                if img.mode == 'L':
                    return Image.fromarray(img_array, 'L')
                elif img.mode == 'RGB':
                    return Image.fromarray(img_array, 'RGB')
                elif img.mode == 'RGBA':
                    return Image.fromarray(img_array, 'RGBA')
                else:
                    return Image.fromarray(img_array, 'RGB')
        elif bit_depth == 16:
            if current_bit_depth == 8:
                # 8位转16位：先转换为numpy数组，然后乘以256
                img_array = np.array(img)
                img_array = (img_array.astype(np.uint16) * 256).astype(np.uint16)
                # PIL不支持16位RGB模式，所以对于彩色图像，我们只能使用I;16模式
                # 但需要确保数据格式正确
                if img.mode in ('RGB', 'RGBA'):
                    # 对于彩色图像，我们需要重新组织数据格式
                    # 将RGB数据转换为灰度格式，因为PIL的I;16模式只支持单通道
                    # 或者使用其他支持16位彩色的格式
                    return Image.fromarray(img_array, 'I;16')
                else:
                    # 灰度图像使用I;16模式
                    return Image.fromarray(img_array, 'I;16')
            elif current_bit_depth == 32:
                img_array = np.array(img)
                img_array = (img_array // 65536).astype(np.uint16)
                if img.mode in ('RGB', 'RGBA'):
                    return Image.fromarray(img_array, 'I;16')
                else:
                    return Image.fromarray(img_array, 'I;16')
        elif bit_depth == 32:
            if current_bit_depth == 8:
                img_array = np.array(img)
                img_array = (img_array.astype(np.uint32) * 16777216).astype(np.uint32)
                return Image.fromarray(img_array, 'I')
            elif current_bit_depth == 16:
                img_array = np.array(img)
                img_array = (img_array.astype(np.uint32) * 65536).astype(np.uint32)
                return Image.fromarray(img_array, 'I')
        
        return img
    
    def _is_raw_file(self, file_path):
        """检查文件是否为RAW格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为RAW文件
        """
        if not RAW_SUPPORTED:
            return False
            
        raw_extensions = {
            '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2',
            '.dng', '.orf', '.rw2', '.rwl', '.pef', '.ptx',
            '.3fr', '.fff', '.mef', '.mos', '.erf', '.dcr', '.kdc',
            '.raw', '.raf', '.x3f', '.iiq'
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        return ext in raw_extensions
    
    def get_supported_input_formats(self):
        """获取支持的输入格式（包括RAW文件）
        
        Returns:
            list: 支持的输入格式列表
        """
        input_formats = ['JPEG', 'PNG', 'WEBP', 'TIFF', 'BMP', 'GIF']
        
        if HEIF_SUPPORTED:
            input_formats.extend(['HEIC', 'HEIF', 'AVIF'])
        
        if RAW_SUPPORTED:
            raw_formats = [
                'CR2', 'CR3', 'NEF', 'NRW', 'ARW', 'SRF', 'SR2',
                'DNG', 'ORF', 'RW2', 'RWL', 'PEF', 'PTX',
                '3FR', 'FFF', 'MEF', 'MOS', 'ERF', 'DCR', 'KDC',
                'RAW', 'RAF', 'X3F', 'IIQ'
            ]
            input_formats.extend(raw_formats)
        
        return input_formats
    
    def _process_raw_file(self, file_path, target_bit_depth=16):
        """处理RAW文件
        
        Args:
            file_path: RAW文件路径
            target_bit_depth: 目标位深 (8, 10, 12, 16)
            
        Returns:
            numpy数组，失败返回None
        """
        if not RAW_SUPPORTED:
            return None
            
        try:
            with rawpy.imread(file_path) as raw:
                # 使用16位原始数据
                rgb = raw.postprocess(
                    output_bps=16,
                    use_camera_wb=True,
                    no_auto_bright=False,
                    output_color=rawpy.ColorSpace.sRGB
                )
                
                # 根据目标位深进行精确缩放
                if target_bit_depth == 8:
                    # 16位转8位：除以256（保留高8位）
                    rgb = (rgb // 256).astype(np.uint8)
                elif target_bit_depth == 10:
                    # 16位转10位：缩放至0-1023范围
                    # 确保数据在正确范围内
                    rgb = np.clip(rgb // 64, 0, 1023).astype(np.uint16)
                elif target_bit_depth == 12:
                    # 16位转12位：缩放至0-4095范围
                    rgb = np.clip(rgb // 16, 0, 4095).astype(np.uint16)
                # 16位保持不变
                
                # 确保数据格式正确：RGB顺序，uint8或uint16
                # pillow_heif期望的数据格式是标准的RGB或RGBA
                if rgb.dtype == np.uint8:
                    # 8位数据已经是正确的格式
                    pass
                elif rgb.dtype == np.uint16:
                    # 16位数据需要确保在正确的位深范围内
                    if target_bit_depth == 10:
                        # 10位数据：0-1023
                        rgb = np.clip(rgb, 0, 1023)
                    elif target_bit_depth == 12:
                        # 12位数据：0-4095
                        rgb = np.clip(rgb, 0, 4095)
                    # 16位数据：0-65535，已经是正确的范围
                
                # 直接返回numpy数组，不转换为PIL图像
                return rgb
        except Exception as e:
            print(f"RAW文件处理错误: {e}")
            return None
    
    def _save_with_pillow_heif(self, image_data, output_path, format_name, quality=85, bit_depth=None):
        """使用pillow_heif.from_bytes()保存numpy数组数据为HEIF格式
        
        Args:
            image_data: numpy数组形式的图像数据
            output_path: 输出文件路径
            format_name: 格式名称 (AVIF, HEIF, HEIC)
            quality: 质量参数
            bit_depth: 位深设置 (8, 10, 12, 16, None表示自动)
            
        Returns:
            bool: 是否保存成功
        """
        if not HEIF_SUPPORTED:
            return False
            
        try:
            import pillow_heif
            
            # 获取图像形状
            height, width = image_data.shape[:2]
            
            # 确定图像模式
            if image_data.ndim == 2:
                mode = "L"  # 灰度图
            elif image_data.ndim == 3:
                if image_data.shape[2] == 3:
                    mode = "RGB"  # RGB
                elif image_data.shape[2] == 4:
                    mode = "RGBA"  # RGBA
                else:
                    mode = "RGB"  # 默认RGB
            else:
                mode = "RGB"  # 默认RGB
            
            # 根据位深设置模式后缀
            # 只有当bit_depth明确指定时才设置位深模式，None表示保持原始位深
            if bit_depth is not None and bit_depth in {10, 12, 16}:
                mode = f"{mode};{bit_depth}"
            
            # 准备数据字节 - 保持原始数据类型
            if image_data.dtype == np.uint8:
                data_bytes = image_data.tobytes()
            elif image_data.dtype == np.uint16:
                data_bytes = image_data.tobytes()
            else:
                # 其他类型转为uint8
                data_bytes = image_data.astype(np.uint8).tobytes()
            
            # 使用from_bytes创建HEIF文件
            heif_file = pillow_heif.from_bytes(
                mode=mode,
                size=(width, height),
                data=data_bytes
            )
            
            # 设置质量参数
            save_kwargs = {'quality': -1 if quality == 100 else quality}
            
            # 保存文件
            heif_file.save(output_path, **save_kwargs)
            return True
            
        except Exception as e:
            print(f"pillow_heif保存错误: {e}")
            return False
    
    def _save_pil_with_pillow_heif(self, pil_image, output_path, format_name, quality=85):
        """使用pillow_heif保存PIL图像为HEIF格式
        
        Args:
            pil_image: PIL图像对象
            output_path: 输出文件路径
            format_name: 格式名称 (AVIF, HEIF, HEIC)
            quality: 质量参数
            
        Returns:
            bool: 是否保存成功
        """
        if not HEIF_SUPPORTED:
            return False
            
        try:
            import pillow_heif
            
            # 将PIL图像转换为numpy数组
            image_array = np.array(pil_image)
            
            # 使用numpy数组保存
            return self._save_with_pillow_heif(image_array, output_path, format_name, quality)
            
        except Exception as e:
            print(f"pillow_heif保存PIL图像错误: {e}")
            return False
    
    def _save_numpy_array(self, image_data, output_path, format_name, quality=85):
        """保存numpy数组数据为图像文件
        
        Args:
            image_data: numpy数组形式的图像数据
            output_path: 输出文件路径
            format_name: 输出格式名称
            quality: 质量参数
            
        Returns:
            bool: 是否保存成功
        """
        if not IMAGEIO_SUPPORTED:
            return False
            
        try:
            # 根据格式设置保存参数
            save_kwargs = {}
            if format_name.upper() in ['JPEG', 'WEBP']:
                save_kwargs['quality'] = quality
            # 使用imageio保存图像
            imageio.imwrite(output_path, image_data, format=format_name.lower(), **save_kwargs)
            # 使用pillow保存图像
            # pil_image = Image.fromarray(image_data)
            pil_image.save(output_path, format=format_name.upper(), **save_kwargs)
            return True
        except Exception as e:
            print(f"numpy数组保存错误: {e}")
            return False
    
    def get_supported_formats(self):
        """
        获取支持的图片格式
        
        Returns:
            list: 支持的格式列表
        """
        base_formats = ['JPEG', 'PNG', 'WEBP', 'TIFF']
        if HEIF_SUPPORTED:
            # 添加HEIF相关的格式
            base_formats.extend(['HEIC', 'HEIF', 'AVIF'])
        # 移除RAW格式作为输出选项，只保留常用图片格式
        return base_formats