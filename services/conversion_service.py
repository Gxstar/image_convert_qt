"""
转换服务模块
"""
import os
from pathlib import Path

from core.image_converter import ImageConverter


class ConversionService:
    def __init__(self):
        """初始化转换服务"""
        self.converter = ImageConverter()
    
    def convert_images(self, image_files, output_dir, output_format, quality=85, replace=False, progress_callback=None):
        """
        转换图片文件
        
        Args:
            image_files: 图片文件路径列表
            output_dir: 输出目录
            output_format: 输出格式
            quality: 图片质量 (1-100)
            replace: 是否替换同名文件
            progress_callback: 进度回调函数
            
        Returns:
            tuple: (成功数量, 失败数量)
        """
        success_count = 0
        error_count = 0
        
        total = len(image_files)
        for i, image_path in enumerate(image_files):
            try:
                # 生成输出文件路径
                filename = Path(image_path).stem
                output_filename = f"{filename}.{output_format.lower()}"
                output_path = os.path.join(output_dir, output_filename)
                
                # 如果不替换且文件已存在，则跳过
                if not replace and os.path.exists(output_path):
                    error_count += 1
                    print(f"文件已存在，跳过: {output_path}")
                    # 调用进度回调
                    if progress_callback:
                        progress_callback(i + 1, total, image_path)
                    continue
                
                # 执行转换
                success, error = self.converter.convert(image_path, output_path, output_format, quality)
                
                if success:
                    success_count += 1
                else:
                    error_count += 1
                    print(f"转换失败 {image_path}: {error}")
                
                # 调用进度回调
                if progress_callback:
                    progress_callback(i + 1, total, image_path)
                    
            except Exception as e:
                error_count += 1
                print(f"转换异常 {image_path}: {str(e)}")
        
        return success_count, error_count
    
    def get_supported_formats(self):
        """
        获取支持的图片格式
        
        Returns:
            list: 支持的格式列表
        """
        return self.converter.get_supported_formats()