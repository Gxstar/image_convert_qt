"""
图片转换器模块
"""
import os
from PIL import Image


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
            with Image.open(input_path) as img:
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
                
                # 保存图片
                img.save(output_path, **save_kwargs)
                
            return True, ""
        except Exception as e:
            return False, str(e)
    
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
            
        return save_kwargs
    
    def get_supported_formats(self):
        """
        获取支持的图片格式
        
        Returns:
            list: 支持的格式列表
        """
        return ['JPEG', 'PNG', 'WEBP', 'TIFF']