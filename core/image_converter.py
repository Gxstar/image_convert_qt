"""
图片转换器模块
"""
import os
from PIL import Image

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
    def __init__(self):
        """初始化图片转换器"""
        pass
    
    def convert(self, input_path, output_path, format_name, quality=85):
        """
        转换图片格式
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            format_name: 输出格式名称
            quality: JPEG/WebP质量 (1-100)
            
        Returns:
            tuple: (是否成功, 错误信息)
        """
        try:
            # 获取图像对象和元数据
            img, exif_data, dpi_info = self._load_image_and_metadata(input_path)
            if img is None:
                return False, "无法加载图像文件"
            
            # 处理RGBA到RGB的转换（JPEG不支持透明度）
            if format_name.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 准备保存参数
            save_kwargs = self._prepare_save_params(format_name, quality)
            
            # 添加DPI信息到保存参数
            if dpi_info:
                save_kwargs['dpi'] = dpi_info
            
            # HEIC格式的特殊处理
            if format_name.upper() == 'HEIC':
                # HEIC格式需要特殊处理
                # 根据pillow-heif文档，HEIC格式需要正确的文件扩展名和格式标识
                
                # 确保文件扩展名正确
                if not output_path.lower().endswith(('.heic', '.heics')):
                    # 如果扩展名不正确，添加.heic扩展名
                    base_name = os.path.splitext(output_path)[0]
                    output_path = base_name + '.heic'
                
                # HEIC格式的特殊参数设置
                # 使用HEIF格式标识，pillow-heif会根据文件扩展名自动处理
                save_kwargs['format'] = 'HEIF'
                
                # HEIC格式可能需要不同的质量参数处理
                if 'quality' in save_kwargs:
                    # 确保质量参数在有效范围内
                    quality_val = save_kwargs['quality']
                    if quality_val == -1:
                        # 无损压缩
                        save_kwargs['quality'] = -1
                    else:
                        # 有损压缩，确保在0-100范围内
                        save_kwargs['quality'] = max(0, min(100, quality_val))
            
            # 如果存在EXIF数据，则添加exif参数
            if exif_data and format_name.upper() != 'HEIC':
                # HEIC格式的EXIF处理需要特殊方式，避免直接传递
                save_kwargs['exif'] = exif_data
            
            # 保存图片
            img.save(output_path, **save_kwargs)
            
            return True, ""
        except Exception as e:
            return False, str(e)
    
    def _load_image_and_metadata(self, input_path):
        """
        加载图像并提取元数据
        
        Args:
            input_path: 输入文件路径
            
        Returns:
            tuple: (PIL.Image对象, EXIF数据, DPI信息)
        """
        # 检查是否为RAW文件
        if self._is_raw_file(input_path):
            img = self._process_raw_file(input_path)
            if img is None:
                return None, None, None
            # RAW文件通常不包含标准EXIF和DPI信息
            return img, None, None
        else:
            # 普通图片文件处理
            try:
                with Image.open(input_path) as img:
                    # 提取EXIF信息
                    exif_data = img.getexif()
                    
                    # 提取DPI信息
                    dpi_info = img.info.get('dpi', None)
                    
                    # 返回图像对象和元数据
                    return img.copy(), exif_data, dpi_info
            except Exception as e:
                print(f"加载图像错误: {e}")
                return None, None, None
    
    def _prepare_save_params(self, format_name, quality):
        """
        准备保存参数
        
        Args:
            format_name: 格式名称
            quality: 质量参数
            
        Returns:
            dict: 保存参数
        """
        save_kwargs = {'format': format_name.upper()}
        
        # JPEG和WebP格式的质量参数
        if format_name.upper() in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            
        # PNG格式的优化参数
        if format_name.upper() == 'PNG':
            save_kwargs['optimize'] = True
            
        # HEIF相关格式的质量参数
        if format_name.upper() in ['HEIC', 'HEIF', 'AVIF']:
            # 质量参数范围是0-100，需要转换为HEIF库期望的范围
            # HEIF质量参数: -1表示无损，0-100表示有损
            if quality == 100:
                save_kwargs['quality'] = -1  # 无损
            else:
                save_kwargs['quality'] = quality
            
        return save_kwargs
    
    def _is_raw_file(self, file_path):
        """
        检查文件是否为RAW格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否为RAW文件
        """
        if not RAW_SUPPORTED:
            return False
            
        # 常见RAW文件扩展名
        raw_extensions = {
            '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2',  # Canon, Nikon, Sony
            '.dng', '.orf', '.rw2', '.rwl', '.pef', '.ptx',        # Adobe, Olympus, Panasonic, Pentax
            '.3fr', '.fff', '.mef', '.mos', '.erf', '.dcr', '.kdc', # Hasselblad, Mamiya, Epson, Kodak
            '.raw', '.raf', '.x3f', '.iiq'                           # Leica, Fuji, Sigma, Phase One
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        return ext in raw_extensions
    
    def get_supported_input_formats(self):
        """
        获取支持的输入格式（包括RAW文件）
        
        Returns:
            list: 支持的输入格式列表
        """
        # 基础图片格式
        input_formats = ['JPEG', 'PNG', 'WEBP', 'TIFF', 'BMP', 'GIF']
        
        # 添加HEIF格式
        if HEIF_SUPPORTED:
            input_formats.extend(['HEIC', 'HEIF', 'AVIF'])
        
        # 添加RAW格式
        if RAW_SUPPORTED:
            input_formats.extend([
                'CR2', 'CR3', 'NEF', 'NRW', 'ARW', 'SRF', 'SR2',  # Canon, Nikon, Sony
                'DNG', 'ORF', 'RW2', 'RWL', 'PEF', 'PTX',        # Adobe, Olympus, Panasonic, Pentax
                '3FR', 'FFF', 'MEF', 'MOS', 'ERF', 'DCR', 'KDC', # Hasselblad, Mamiya, Epson, Kodak
                'RAW', 'RAF', 'X3F', 'IIQ'                        # Leica, Fuji, Sigma, Phase One
            ])
        
        return input_formats
    
    def _process_raw_file(self, file_path):
        """
        处理RAW文件
        
        Args:
            file_path: RAW文件路径
            
        Returns:
            PIL.Image: 处理后的PIL图像对象，失败返回None
        """
        if not RAW_SUPPORTED:
            return None
            
        try:
            with rawpy.imread(file_path) as raw:
                # 使用默认参数处理RAW文件
                rgb = raw.postprocess(
                    output_bps=8,  # 改为8位输出，避免16位转换问题
                    use_camera_wb=True,
                    no_auto_bright=False,
                    output_color=rawpy.ColorSpace.sRGB
                )
                
                # 转换为PIL图像
                # rawpy输出的是numpy数组，需要转换为PIL格式
                # 注意：rawpy.postprocess()返回的是uint8或uint16的numpy数组
                # 直接使用Image.fromarray()转换
                img = Image.fromarray(rgb)
                
                return img
                
        except Exception as e:
            print(f"RAW文件处理错误: {e}")
            return None
    
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
        if RAW_SUPPORTED:
            base_formats.append('RAW')  # 表示支持RAW文件输入
        return base_formats