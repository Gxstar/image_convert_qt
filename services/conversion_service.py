"""
转换服务模块
"""
import os
from pathlib import Path
import cv2 as cv
from PIL import Image
import rawpy

from core.image_converter import ImageConverter
from core.utils import show_question, show_message

class ConversionService:
    def __init__(self):
        """初始化转换服务"""
        self.converter = ImageConverter()
        self.parent_window = None

    def convert_images(self, image_files, output_dir, output_format, quality=85, bit_depth=None, replace=False, progress_callback=None, parent_window=None, user_decisions=None):
        """
        转换图片文件
        
        Args:
            image_files: 图片文件路径列表
            output_dir: 输出目录
            output_format: 输出格式
            quality: 图片质量 (1-100)
            bit_depth: 位深设置 (8, 10, 12, 16)
            replace: 是否替换同名文件
            progress_callback: 进度回调函数
            parent_window: 父窗口，用于显示对话框
            user_decisions: 用户决策字典（由调用方提供）
            
        Returns:
            tuple: (成功数量, 失败数量, 详细信息字典)
        """
        success_count = 0
        error_count = 0
        
        # 设置父窗口引用
        if parent_window:
            self.parent_window = parent_window
        
        # 预扫描阶段 - 收集所有冲突信息
        conflict_info = self._scan_for_conflicts(image_files, output_dir, output_format, replace)
        
        # 如果用户决策未提供，使用空字典
        if user_decisions is None:
            user_decisions = {}
        
        total = len(image_files)
        for i, image_path in enumerate(image_files):
            try:
                # 生成输出文件路径
                filename = Path(image_path).stem
                # 确保JPEG格式使用.jpg扩展名而不是.jpeg
                if output_format.upper() == 'JPEG':
                    output_filename = f"{filename}.jpg"
                else:
                    output_filename = f"{filename}.{output_format.lower()}"
                output_path = os.path.join(output_dir, output_filename)
                
                # 检查是否应该跳过
                should_skip = False
                if image_path in user_decisions:
                    decision = user_decisions[image_path]
                    if decision == 'skip':
                        should_skip = True
                    elif decision == 'replace':
                        # 删除冲突文件
                        if image_path in conflict_info:
                            for conflict_file in conflict_info[image_path]['conflict_files']:
                                try:
                                    os.remove(conflict_file)
                                except Exception as e:
                                    print(f"删除冲突文件失败 {conflict_file}: {e}")
                elif not replace and os.path.exists(output_path):
                    # 未选中替换且文件存在，直接跳过
                    should_skip = True
                elif replace:
                    # 选中替换时的自动处理
                    conflict_files = self._find_conflict_files(output_dir, filename)
                    if conflict_files:
                        # 自动删除冲突文件
                        for conflict_file in conflict_files:
                            try:
                                os.remove(conflict_file)
                            except Exception as e:
                                print(f"删除冲突文件失败 {conflict_file}: {e}")
                
                if should_skip:
                    error_count += 1
                    print(f"跳过文件: {output_path}")
                    # 调用进度回调
                    if progress_callback:
                        progress_callback(i + 1, total, image_path)
                    continue
                
                # 检查位深兼容性
                is_compatible, actual_bit_depth = self._check_bit_depth_compatibility(image_path, bit_depth)
                
                # 如果位深不兼容，显示提示信息
                if not is_compatible and bit_depth is not None:
                    original_bit_depth = self._get_image_bit_depth(image_path)
                    message = f"图像 {os.path.basename(image_path)} 的原始位深为 {original_bit_depth} 位，\n"
                    message += f"但您要求输出 {bit_depth} 位。\n\n"
                    message += "位深不能大于原始图像的位深。\n"
                    message += "将按照 8 位进行输出。"
                    
                    if self.parent_window:
                        show_message(self.parent_window, "位深不兼容", message)
                    else:
                        print(message)
                
                # 执行转换
                success, error = self.converter.convert(image_path, output_path, output_format, quality, actual_bit_depth)
                
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
        
        return success_count, error_count, conflict_info
    
    def get_supported_formats(self):
        """
        获取支持的图片格式
        
        Returns:
            list: 支持的格式列表
        """
        supported_formats = ['JPEG', 'PNG', 'TIFF', 'WEBP', 'HEIC', 'HEIF', 'AVIF']
        return supported_formats
    
    def get_supported_input_formats(self):
        """
        获取支持的输入格式（包括RAW文件）
        
        Returns:
            list: 支持的输入格式列表（统一使用大写）
        """
        # Pillow支持的常用图片格式
        pillow_formats = ['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP', 'HEIC', 'HEIF', 'AVIF', 'ICO', 'PPM', 'PGM', 'PBM', 'DDS', 'PCX', 'TGA', 'SGI', 'XBM', 'XPM']
        
        # 常见相机厂商的RAW格式
        raw_formats = ['RAW', 'CR2', 'CR3', 'CRW', 'NEF', 'NRW', 'ARW', 'SR2', 'SRF', 'DNG', 'ORF', 'RW2', 'PEF', 'RAF', 'SRW', '3FR', 'FFF', 'KDC', 'MRW', 'MOS', 'RWL', 'SRW', 'X3F']
        
        # 合并所有支持的输入格式
        supported_input_formats = pillow_formats + raw_formats
        return supported_input_formats
    
    def _find_conflict_files(self, directory, filename_stem):
        """
        查找与指定文件名主体冲突的文件（忽略后缀名）
        
        Args:
            directory: 搜索目录
            filename_stem: 文件名主体（不含后缀）
            
        Returns:
            list: 冲突文件路径列表
        """
        conflict_files = []
        
        # 获取支持的所有图片扩展名
        supported_formats = self.get_supported_formats()
        # 添加常见的小写形式
        all_extensions = set()
        for fmt in supported_formats:
            all_extensions.add(f'.{fmt.lower()}')
            all_extensions.add(f'.{fmt.upper()}')
        
        # 获取支持的输入格式并添加扩展名
        input_formats = self.get_supported_input_formats()
        for fmt in input_formats:
            all_extensions.add(f'.{fmt.lower()}')
            all_extensions.add(f'.{fmt.upper()}')
        
        # 添加一些额外的常见格式
        extra_extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG', 
                           '.bmp', '.BMP', '.gif', '.GIF', '.tiff', '.TIFF', 
                           '.webp', '.WEBP', '.heic', '.HEIC', '.heif', '.HEIF',
                           '.avif', '.AVIF', '.ico', '.ICO', '.ppm', '.PPM',
                           '.pgm', '.PGM', '.pbm', '.PBM', '.dds', '.DDS',
                           '.pcx', '.PCX', '.tga', '.TGA', '.sgi', '.SGI',
                           '.xbm', '.XBM', '.xpm', '.XPM', '.cr2', '.CR2',
                           '.cr3', '.CR3', '.crw', '.CRW', '.nef', '.NEF',
                           '.nrw', '.NRW', '.arw', '.ARW', '.sr2', '.SR2',
                           '.srf', '.SRF', '.dng', '.DNG', '.orf', '.ORF',
                           '.rw2', '.RW2', '.pef', '.PEF', '.raf', '.RAF',
                           '.srw', '.SRW', '.3fr', '.3FR', '.fff', '.FFF',
                           '.kdc', '.KDC', '.mrw', '.MRW', '.mos', '.MOS',
                           '.rwl', '.RWL', '.x3f', '.X3F'}
        all_extensions.update(extra_extensions)
        
        # 检查每个可能的扩展名
        for ext in all_extensions:
            test_filename = f"{filename_stem}{ext}"
            test_path = os.path.join(directory, test_filename)
            if os.path.exists(test_path):
                conflict_files.append(test_path)
        
        return conflict_files
    
    def _scan_for_conflicts(self, image_files, output_dir, output_format, replace):
        """
        预扫描所有文件的冲突情况
        
        Args:
            image_files: 图片文件路径列表
            output_dir: 输出目录
            output_format: 输出格式
            replace: 是否替换同名文件
            
        Returns:
            dict: 冲突信息字典
        """
        conflict_info = {}
        
        for image_path in image_files:
            filename = Path(image_path).stem
            if output_format.upper() == 'JPEG':
                output_filename = f"{filename}.jpg"
            else:
                output_filename = f"{filename}.{output_format.lower()}"
            output_path = os.path.join(output_dir, output_filename)
            
            conflicts = []
            if replace:
                # 忽略后缀名检查同名文件
                conflicts = self._find_conflict_files(output_dir, filename)
            else:
                # 精确匹配检查
                if os.path.exists(output_path):
                    conflicts = [output_path]
            
            if conflicts:
                conflict_info[image_path] = {
                    'output_filename': output_filename,
                    'conflict_files': conflicts
                }
        
        return conflict_info
    
    def _batch_resolve_conflicts(self, conflict_info, replace):
        """
        批量解决冲突，一次性询问用户
        
        Args:
            conflict_info: 冲突信息字典
            replace: 是否替换同名文件
            
        Returns:
            dict: 用户决策字典
        """
        if not conflict_info:
            return {}
        
        # 统计冲突情况
        total_conflicts = len(conflict_info)
        conflict_summary = []
        
        for image_path, info in conflict_info.items():
            conflict_files = info['conflict_files']
            conflict_names = [os.path.basename(f) for f in conflict_files]
            output_filename = info['output_filename']
            conflict_summary.append(f"{output_filename} <- {', '.join(conflict_names)}")
        
        # 构建询问消息
        if replace:
            message = f"发现 {total_conflicts} 个同名文件冲突（忽略后缀名）:\n\n"
            message += "\n".join(conflict_summary[:10])  # 最多显示10个
            if total_conflicts > 10:
                message += f"\n... 还有 {total_conflicts - 10} 个冲突"
            message += "\n\n是否替换所有冲突文件？"
        else:
            message = f"发现 {total_conflicts} 个文件已存在:\n\n"
            message += "\n".join(conflict_summary[:10])  # 最多显示10个
            if total_conflicts > 10:
                message += f"\n... 还有 {total_conflicts - 10} 个已存在"
            message += "\n\n是否替换这些文件？"
        
        # 询问用户
        user_choice = show_question(self.parent_window, "文件冲突", message)
        
        # 根据用户选择生成决策
        decisions = {}
        for image_path in conflict_info.keys():
            if user_choice:
                decisions[image_path] = 'replace'
            else:
                decisions[image_path] = 'skip'
        
    def get_conflict_summary(self, conflict_info, replace):
        """
        获取冲突信息的简化摘要
        
        Args:
            conflict_info: 冲突信息字典
            replace: 是否替换同名文件
            
        Returns:
            tuple: (标题, 消息, 冲突数量)
        """
        if not conflict_info:
            return "", "", 0
        
        total_conflicts = len(conflict_info)
        
        if replace:
            title = "发现同名文件冲突"
            message = f"发现 {total_conflicts} 个同名文件需要替换（忽略后缀名）\n\n是否替换所有冲突文件？"
        else:
            title = "发现文件已存在"
            message = f"发现 {total_conflicts} 个文件已存在\n\n是否替换这些文件？"
        
        return title, message, total_conflicts
    
    def create_user_decisions(self, conflict_info, user_choice):
        """
        根据用户选择创建决策字典
        
        Args:
            conflict_info: 冲突信息字典
            user_choice: 用户是否选择替换
            
        Returns:
            dict: 用户决策字典
        """
        if not conflict_info:
            return {}
        
        decisions = {}
        for image_path in conflict_info.keys():
            if user_choice:
                decisions[image_path] = 'replace'
            else:
                decisions[image_path] = 'skip'
        
        return decisions

    def _get_image_bit_depth(self, image_path):
        """
        获取图像的原始位深
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            int: 图像的原始位深（8, 10, 12, 16等）
        """
        try:
            # 判断是否为RAW文件
            raw_extensions = {
                '.cr2', '.cr3', '.nef', '.nrw', '.arw', '.srf', '.sr2',
                '.dng', '.orf', '.rw2', '.rwl', '.pef', '.ptx',
                '.3fr', '.fff', '.mef', '.mos', '.erf', '.dcr', '.kdc',
                '.raw', '.raf', '.x3f', '.iiq'
            }
            ext = os.path.splitext(image_path)[1].lower()
            is_raw = ext in raw_extensions
            
            if is_raw:
                # RAW文件通常为16位
                return 16
            else:
                # 使用OpenCV读取图像
                img = cv.imread(image_path)
                if img is None:
                    # 如果OpenCV无法读取，尝试使用Pillow
                    with Image.open(image_path) as pil_img:
                        if pil_img.mode in ('I;16', 'I;16B', 'I;16L', 'I;16N'):
                            return 16
                        elif pil_img.mode in ('I;12', 'I;12B', 'I;12L'):
                            return 12
                        elif pil_img.mode in ('I;10', 'I;10B', 'I;10L'):
                            return 10
                        else:
                            return 8
                else:
                    # 检查OpenCV图像的数据类型
                    if img.dtype == 'uint16':
                        return 16
                    elif img.dtype == 'uint8':
                        return 8
                    else:
                        return 8  # 默认返回8位
        except Exception as e:
            print(f"获取图像位深失败 {image_path}: {str(e)}")
            return 8  # 出错时默认返回8位

    def _check_bit_depth_compatibility(self, image_path, requested_bit_depth):
        """
        检查请求的位深是否大于图像的原始位深
        
        Args:
            image_path: 图像文件路径
            requested_bit_depth: 用户请求的输出位深
            
        Returns:
            tuple: (是否兼容, 实际使用的位深)
        """
        if requested_bit_depth is None:
            return True, None
            
        original_bit_depth = self._get_image_bit_depth(image_path)
        
        # 如果请求的位深大于原始位深，则不兼容
        if requested_bit_depth > original_bit_depth:
            return False, 8  # 不兼容时强制使用8位
        else:
            return True, requested_bit_depth  # 兼容时使用请求的位深