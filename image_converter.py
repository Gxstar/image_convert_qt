"""
图片转换器模块
"""
import os
from PIL import Image
from utils import ensure_directory


class ImageConverter:
    """图片转换器类"""
    
    def __init__(self):
        """初始化转换器"""
        self.supported_formats = ['jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp']
    
    def convert_image(self, input_path, output_path, output_format, quality=85, **kwargs):
        """
        转换单张图片
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            output_format: 输出格式
            quality: 图片质量 (1-100)
            **kwargs: 其他参数
            
        Returns:
            bool: 转换是否成功
            
        Raises:
            Exception: 转换过程中的异常
        """
        try:
            # 确保输出目录存在
            ensure_directory(os.path.dirname(output_path))
            
            # 打开图片
            with Image.open(input_path) as img:
                # 处理格式转换
                converted_img = self._prepare_image_for_format(img, output_format)
                
                # 设置保存参数
                save_kwargs = self._get_save_kwargs(output_format, quality, **kwargs)
                
                # 保存图片
                converted_img.save(output_path, format=output_format.upper(), **save_kwargs)
                
                return True
                
        except Exception as e:
            raise Exception(f"转换失败 {input_path}: {str(e)}")
    
    def _prepare_image_for_format(self, img, output_format):
        """
        根据输出格式准备图片
        
        Args:
            img: PIL图片对象
            output_format: 输出格式
            
        Returns:
            PIL.Image: 处理后的图片对象
        """
        if output_format == 'jpeg' and img.mode in ('RGBA', 'LA', 'P'):
            # JPEG不支持透明度，转换为RGB
            return self._convert_to_rgb_with_white_background(img)
        
        return img
    
    def _convert_to_rgb_with_white_background(self, img):
        """
        将图片转换为RGB格式，使用白色背景处理透明度
        
        Args:
            img: PIL图片对象
            
        Returns:
            PIL.Image: RGB格式的图片对象
        """
        # 创建白色背景
        background = Image.new('RGB', img.size, (255, 255, 255))
        
        # 处理调色板模式
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # 粘贴图片到背景上
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[-1])
        else:
            background.paste(img)
        
        return background
    
    def _get_save_kwargs(self, output_format, quality, **kwargs):
        """
        获取保存参数
        
        Args:
            output_format: 输出格式
            quality: 图片质量
            **kwargs: 其他参数
            
        Returns:
            dict: 保存参数
        """
        save_kwargs = {}
        
        if output_format in ['jpeg', 'webp']:
            save_kwargs['quality'] = quality
            if output_format == 'jpeg':
                save_kwargs['optimize'] = True
        
        # 添加其他参数
        save_kwargs.update(kwargs)
        
        return save_kwargs
    
    def batch_convert(self, image_files, output_dir, output_format, quality=85, 
                     replace_existing=False, progress_callback=None):
        """
        批量转换图片
        
        Args:
            image_files: 图片文件路径列表
            output_dir: 输出目录
            output_format: 输出格式
            quality: 图片质量
            replace_existing: 是否替换已存在的文件
            progress_callback: 进度回调函数
            
        Returns:
            dict: 转换结果统计 {'success': int, 'error': int, 'skipped': int}
        """
        from utils import get_output_filename
        
        stats = {'success': 0, 'error': 0, 'skipped': 0}
        
        for i, image_path in enumerate(image_files):
            try:
                # 生成输出文件名
                output_filename = get_output_filename(image_path, output_format)
                output_path = os.path.join(output_dir, output_filename)
                
                # 检查文件是否已存在
                if os.path.exists(output_path) and not replace_existing:
                    stats['skipped'] += 1
                    continue
                
                # 转换图片
                self.convert_image(image_path, output_path, output_format, quality)
                stats['success'] += 1
                
                # 调用进度回调
                if progress_callback:
                    progress_callback(i + 1, len(image_files), image_path)
                    
            except Exception as e:
                stats['error'] += 1
                print(f"转换失败 {image_path}: {str(e)}")
        
        return stats