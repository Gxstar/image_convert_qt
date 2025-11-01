"""
缩略图管理器
负责生成和管理图片缩略图
"""
import os
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QThread, QSize
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtWidgets import QApplication


class ThumbnailWorker(QThread):
    """缩略图生成工作线程"""
    thumbnail_ready = Signal(str, QPixmap)  # 文件路径, 缩略图
    
    def __init__(self, file_path, size):
        super().__init__()
        self.file_path = file_path
        self.size = size
    
    def run(self):
        """生成缩略图"""
        try:
            # 使用QImageReader加载图片，支持更多格式
            reader = QImageReader(self.file_path)
            reader.setAutoTransform(True)
            
            # 设置缩略图大小
            reader.setScaledSize(self.size)
            
            # 读取图片
            image = reader.read()
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                self.thumbnail_ready.emit(self.file_path, pixmap)
        except Exception as e:
            print(f"生成缩略图失败 {self.file_path}: {e}")


class ThumbnailManager(QObject):
    """缩略图管理器"""
    
    thumbnail_loaded = Signal(str)  # 缩略图加载完成信号
    
    def __init__(self, thumbnail_size=QSize(100, 100)):
        super().__init__()
        self.thumbnail_size = thumbnail_size
        self.thumbnail_cache = {}  # 文件路径 -> 缩略图
        self.pending_requests = set()  # 正在处理的请求
        self.active_workers = []  # 活跃的工作线程列表
        
    def get_thumbnail(self, file_path):
        """
        获取缩略图
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            QPixmap or None: 缩略图，如果缓存中不存在则返回None
        """
        if file_path in self.thumbnail_cache:
            return self.thumbnail_cache[file_path]
        
        # 如果不在缓存中且没有正在处理，则启动异步加载
        if file_path not in self.pending_requests:
            self._load_thumbnail_async(file_path)
        
        return None
    
    def _load_thumbnail_async(self, file_path):
        """异步加载缩略图"""
        if not os.path.exists(file_path):
            return
            
        self.pending_requests.add(file_path)
        worker = ThumbnailWorker(file_path, self.thumbnail_size)
        worker.thumbnail_ready.connect(self._on_thumbnail_ready)
        worker.finished.connect(lambda: self._on_worker_finished(worker))
        self.active_workers.append(worker)
        worker.start()
    
    def _on_thumbnail_ready(self, file_path, pixmap):
        """缩略图加载完成"""
        self.pending_requests.discard(file_path)
        self.thumbnail_cache[file_path] = pixmap
        # 发出缩略图加载完成信号
        self.thumbnail_loaded.emit(file_path)
    
    def _on_worker_finished(self, worker):
        """工作线程完成处理"""
        if worker in self.active_workers:
            self.active_workers.remove(worker)
    
    def clear_cache(self):
        """清空缩略图缓存"""
        self.thumbnail_cache.clear()
        self.pending_requests.clear()
    
    def remove_thumbnail(self, file_path):
        """移除指定文件的缩略图"""
        if file_path in self.thumbnail_cache:
            del self.thumbnail_cache[file_path]
        self.pending_requests.discard(file_path)
    
    def cleanup(self):
        """清理所有工作线程"""
        # 终止所有活跃的工作线程
        for worker in self.active_workers:
            if worker.isRunning():
                worker.quit()
                worker.wait(1000)  # 等待1秒让线程正常结束
        self.active_workers.clear()
        self.clear_cache()