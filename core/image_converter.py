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


class ImageConverter:
    """图片格式转换器"""
    
    def __init__(self):
        """初始化图片转换器"""
        pass
    
    def convert(self, input_path, output_path, format_name, quality=85, bit_depth=8):
        """转换图像格式"""
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            return False, "输入文件不存在"
        
        # 检查输出目录是否存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return False, f"创建输出目录失败: {e}"
        
        # 检查输出格式是否支持
        format_upper = format_name.upper()
        if format_upper not in self.get_supported_formats():
            return False, f"不支持的输出格式: {format_name}"
        
        # 加载输入图像
        pil_image, img_data, is_raw, success = self._load_image(input_path)
        if not success:
            return False, "加载图像失败"
        
        # 处理HEIF格式
        if format_upper in {'AVIF', 'HEIF', 'HEIC'}:
            if is_raw:
                image_data = img_data
            else:
                # 对于PIL图像，确保正确的数据类型
                if bit_depth == 16:
                    # 16位模式需要转换为uint16
                    image_data = np.array(pil_image).astype(np.uint16)
                elif bit_depth in {10, 12}:
                    # 10位/12位模式需要先转换为16位，然后在_save_with_pillow_heif中处理
                    image_data = np.array(pil_image).astype(np.uint16)
                else:
                    # 8位模式
                    image_data = np.array(pil_image).astype(np.uint8)
            
            success = self._save_with_pillow_heif(image_data, output_path, format_upper, quality, bit_depth)
            return (True, "") if success else (False, "pillow_heif保存失败")
        
        # 处理RAW文件
        if is_raw:
            return self._handle_raw_file(img_data, output_path, format_upper, quality, bit_depth)
        
        # 处理16位格式
        if bit_depth == 16:
            return self._handle_16bit_format(pil_image, img_data, output_path, format_upper, quality)
        
        # 处理8位格式
        return self._handle_8bit_format(pil_image, img_data, output_path, format_upper, quality)
    
    def _load_image(self, input_path):
        """加载图像数据"""
        if self._is_raw_file(input_path):
            img_data = self._process_raw_file(input_path)
            return None, img_data, True, img_data is not None
        
        try:
            with Image.open(input_path) as img:
                return img.copy(), None, False, True
        except Exception:
            return None, None, False, False
    
    def _handle_raw_file(self, img_data, output_path, format_upper, quality, bit_depth):
        """处理RAW文件转换"""
        if img_data is None:
            return False, "RAW文件处理失败"
        
        # 处理HEIF格式
        if format_upper in {'AVIF', 'HEIF', 'HEIC'}:
            success = self._save_with_pillow_heif(img_data, output_path, format_upper, quality, bit_depth)
            return (True, "") if success else (False, "pillow_heif保存失败")
        
        # 处理其他格式
        success = self._save_numpy_array(img_data, output_path, format_upper, quality)
        return (True, "") if success else (False, "保存失败")
    
    def _handle_16bit_format(self, pil_image, img_data, output_path, format_upper, quality):
        """处理16位格式转换"""
        try:
            if img_data is not None:
                # 对于numpy数组数据
                if img_data.dtype != np.uint16:
                    img_data = img_data.astype(np.uint16)
                success = self._save_numpy_array(img_data, output_path, format_upper, quality)
            else:
                # 对于PIL图像
                save_kwargs = {'format': format_upper}
                
                # 设置无损压缩选项
                if quality == 100:
                    if format_upper == 'PNG':
                        save_kwargs['optimize'] = False  # 无损PNG不需要优化
                    elif format_upper == 'TIFF':
                        save_kwargs['compression'] = 'tiff_lzw'  # LZW压缩是无损的
                else:
                    if format_upper == 'PNG':
                        save_kwargs['optimize'] = True
                    elif format_upper == 'TIFF':
                        save_kwargs['compression'] = 'tiff_lzw'
                
                pil_image.save(output_path, **save_kwargs)
                success = True
            
            return (True, "") if success else (False, "16位格式保存失败")
        except Exception as e:
            return False, f"16位格式保存错误: {e}"
    
    def _handle_8bit_format(self, pil_image, img_data, output_path, format_upper, quality):
        """处理8位格式转换"""
        try:
            if img_data is not None:
                # 对于numpy数组数据
                if img_data.dtype != np.uint8:
                    img_data = img_data.astype(np.uint8)
                success = self._save_numpy_array(img_data, output_path, format_upper, quality)
            else:
                # 对于PIL图像
                save_kwargs = {'format': format_upper}
                
                # 设置无损压缩选项
                if quality == 100:
                    if format_upper == 'PNG':
                        save_kwargs['optimize'] = False  # 无损PNG不需要优化
                    elif format_upper == 'TIFF':
                        save_kwargs['compression'] = 'tiff_lzw'  # LZW压缩是无损的
                    elif format_upper in ['JPEG', 'WEBP']:
                        # JPEG和WEBP不支持真正的无损压缩，使用最高质量
                        save_kwargs.update({'quality': 100, 'optimize': True})
                else:
                    if format_upper in ['JPEG', 'WEBP']:
                        save_kwargs.update({'quality': quality, 'optimize': True})
                    elif format_upper == 'PNG':
                        save_kwargs['optimize'] = True
                    elif format_upper == 'TIFF':
                        save_kwargs['compression'] = 'tiff_lzw'
                
                # 处理JPEG透明度问题
                if format_upper == 'JPEG' and pil_image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', pil_image.size, (255, 255, 255))
                    if pil_image.mode == 'P':
                        pil_image = pil_image.convert('RGBA')
                    background.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode == 'RGBA' else None)
                    pil_image = background
                
                pil_image.save(output_path, **save_kwargs)
                success = True
            
            return (True, "") if success else (False, "8位格式保存失败")
        except Exception as e:
            return False, f"8位格式保存错误: {e}"
    
    def _is_raw_file(self, file_path):
        """检查文件是否为RAW格式"""
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
    
    def _process_raw_file(self, file_path, target_bit_depth=8):
        """处理RAW文件"""
        if not RAW_SUPPORTED:
            return None
            
        try:
            with rawpy.imread(file_path) as raw:
                # 使用16位原始数据
                rgb = raw.postprocess(output_bps=16, use_camera_wb=True, no_auto_bright=False, output_color=rawpy.ColorSpace.sRGB)
                
                # 根据目标位深进行精确缩放
                if target_bit_depth == 8:
                    rgb = (rgb // 256).astype(np.uint8)
                elif target_bit_depth == 10:
                    rgb = np.clip(rgb // 64, 0, 1023).astype(np.uint16)
                elif target_bit_depth == 12:
                    rgb = np.clip(rgb // 16, 0, 4095).astype(np.uint16)
                else:
                    rgb = rgb.astype(np.uint16)
                
                return rgb
        except Exception:
            return None
    
    def _save_with_pillow_heif(self, image_data, output_path, format_name, quality=85, bit_depth=None):
        """使用pillow_heif保存numpy数组数据为HEIF/AVIF格式"""
        if not HEIF_SUPPORTED:
            return False
            
        try:
            import pillow_heif
            from pillow_heif import options
            
            # 获取图像形状
            height, width = image_data.shape[:2]
            
            # 确定图像模式
            if image_data.ndim == 2:
                base_mode = "L"
            elif image_data.ndim == 3:
                base_mode = "RGB" if image_data.shape[2] == 3 else "RGBA"
            else:
                base_mode = "RGB"
            
            # 根据位深设置正确的模式格式
            if bit_depth == 10:
                mode = f"{base_mode};10"
                # 10位模式需要将16位数据转换为10位
                if image_data.dtype == np.uint16:
                    image_data = np.clip(image_data // 64, 0, 1023).astype(np.uint16)
            elif bit_depth == 12:
                mode = f"{base_mode};12"
                # 12位模式需要将16位数据转换为12位
                if image_data.dtype == np.uint16:
                    image_data = np.clip(image_data // 16, 0, 4095).astype(np.uint16)
            elif bit_depth == 16:
                mode = f"{base_mode};16"
            else:
                mode = base_mode
                # 8位模式需要确保数据类型正确
                if image_data.dtype != np.uint8:
                    image_data = image_data.astype(np.uint8)
            
            # 准备数据字节
            data_bytes = image_data.tobytes()
            
            # 设置编码器选项
            format_upper = format_name.upper()
            
            # 创建HEIF文件
            heif_file = pillow_heif.from_bytes(mode=mode, size=(width, height), data=data_bytes)
            
            # 设置保存选项
            save_options = {}
            
            # 设置质量
            if quality == 100:
                save_options['quality'] = -1  # 无损质量
                # 对于无损编码，需要设置chroma=444
                save_options['chroma'] = 444
            else:
                save_options['quality'] = quality
            
            # 设置编码器类型
            if format_upper == 'AVIF':
                save_options['encoder'] = 'aom'
            else:
                save_options['encoder'] = 'x265'
            
            # 保存文件
            heif_file.save(output_path, **save_options)
            return True
            
        except Exception as e:
            print(f"HEIF保存错误: {e}")
            return False
    

    
    def _save_numpy_array(self, image_data, output_path, format_name, quality=85):
        """保存numpy数组数据为图像文件"""
        try:
            # 根据格式设置保存参数
            save_kwargs = {}
            format_upper = format_name.upper()
            
            if format_upper in ['JPEG', 'WEBP']:
                save_kwargs['quality'] = quality
            
            # 确定图像模式
            if image_data.ndim == 2:
                mode = 'L' if image_data.dtype == np.uint8 else 'I;16'
            elif image_data.ndim == 3:
                if image_data.shape[2] == 3:
                    mode = 'RGB' if image_data.dtype == np.uint8 else 'I;16'
                elif image_data.shape[2] == 4:
                    mode = 'RGBA' if image_data.dtype == np.uint8 else 'I;16'
                else:
                    mode = 'RGB' if image_data.dtype == np.uint8 else 'I;16'
            else:
                return False
            
            # 对于16位彩色图像，转换为灰度
            if image_data.dtype != np.uint8 and image_data.ndim == 3 and image_data.shape[2] == 3:
                image_data = np.dot(image_data[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint16)
                mode = 'I;16'
            
            pil_img = Image.fromarray(image_data, mode)
            pil_img.save(output_path, format=format_upper, **save_kwargs)
            return True
        except Exception:
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