"""
图片列表管理器
负责图片列表的显示和管理
"""
import os
from PySide6.QtCore import QStringListModel


class ImageListManager:
    """图片列表管理器"""
    
    def __init__(self, list_view):
        """
        初始化图片列表管理器
        
        Args:
            list_view: QListView实例
        """
        self.list_view = list_view
        self.image_files = []
        self.model = None
    
    def add_files(self, files):
        """
        添加文件到列表
        
        Args:
            files: 文件路径列表
        """
        # 过滤已存在的文件
        new_files = [f for f in files if f not in self.image_files]
        
        if new_files:
            # 添加到数据列表
            self.image_files.extend(new_files)
            
            # 更新UI显示
            self._update_list_view()
            
        return new_files
    
    def remove_selected(self):
        """
        移除选中的项目
        """
        # 获取选中的索引
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return 0
            
        # 按行号排序（从大到小），以便从后往前删除
        selected_rows = sorted([index.row() for index in selected_indexes], reverse=True)
        
        # 删除选中的项目
        for row in selected_rows:
            if row < len(self.image_files):
                self.image_files.pop(row)
        
        # 更新UI显示
        self._update_list_view()
        
        return len(selected_rows)
    
    def clear_all(self):
        """
        清空所有项目
        
        Returns:
            int: 清空的项目数量
        """
        count = len(self.image_files)
        self.image_files.clear()
        self._update_list_view()
        return count
    
    def get_file_count(self):
        """
        获取文件数量
        
        Returns:
            int: 文件数量
        """
        return len(self.image_files)
    
    def get_file_paths(self):
        """
        获取所有文件路径
        
        Returns:
            list: 文件路径列表
        """
        return self.image_files[:]
    
    def _update_list_view(self):
        """更新列表视图显示"""
        # 获取当前显示的文件名列表
        file_names = [os.path.basename(f) for f in self.image_files]
        
        # 更新模型
        if self.model is None:
            self.model = QStringListModel()
            self.list_view.setModel(self.model)
        
        self.model.setStringList(file_names)