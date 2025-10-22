"""
图片加载服务
负责异步加载图片文件
"""
import os
from PySide6.QtCore import QThread, Signal


class ImageLoaderThread(QThread):
    """图片加载线程"""
    progress_updated = Signal(int, int)  # 当前进度, 总数量
    file_loaded = Signal(str)  # 文件路径
    finished_loading = Signal(list)  # 所有加载的文件路径
    
    def __init__(self, files):
        super().__init__()
        self.files = files
        self._is_cancelled = False
    
    def run(self):
        """在后台线程中运行图片加载"""
        total_files = len(self.files)
        loaded_files = []
        
        for i, file_path in enumerate(self.files):
            if self._is_cancelled:
                break
                
            # 检查文件是否存在
            if os.path.exists(file_path):
                loaded_files.append(file_path)
                self.file_loaded.emit(file_path)
            
            # 更新进度
            self.progress_updated.emit(i + 1, total_files)
            
            # 短暂延迟，避免线程占用过高CPU
            self.msleep(10)
        
        if not self._is_cancelled:
            self.finished_loading.emit(loaded_files)
    
    def cancel(self):
        """取消加载"""
        self._is_cancelled = True


class ImageLoaderService:
    """图片加载服务"""
    
    def __init__(self):
        """初始化图片加载服务"""
        self.loader_thread = None
        self.is_loading = False
    
    def start_loading(self, files, progress_callback=None, finished_callback=None):
        """
        启动图片加载
        
        Args:
            files: 文件路径列表
            progress_callback: 进度回调函数
            finished_callback: 完成回调函数
        """
        if self.is_loading:
            return False
        
        self.is_loading = True
        
        # 创建并启动加载线程
        self.loader_thread = ImageLoaderThread(files)
        
        # 连接信号
        if progress_callback:
            self.loader_thread.progress_updated.connect(progress_callback)
        
        if finished_callback:
            self.loader_thread.finished_loading.connect(finished_callback)
        
        self.loader_thread.start()
        return True
    
    def cancel_loading(self):
        """取消图片加载"""
        if self.loader_thread and self.loader_thread.isRunning():
            self.loader_thread.cancel()
            self.loader_thread.wait()  # 等待线程安全退出
        
        self.is_loading = False
        self.loader_thread = None
    
    def is_loading_in_progress(self):
        """
        检查是否正在加载
        
        Returns:
            bool: 是否正在加载
        """
        return self.is_loading