"""
网格视图管理器
负责缩略图网格视图的显示和管理
"""
import os
from PySide6.QtCore import Qt

from widgets.thumbnail_grid_view import ThumbnailGridView


class GridViewManager:
    """网格视图管理器"""
    
    def __init__(self, parent_widget):
        """
        初始化网格视图管理器
        
        Args:
            parent_widget: 父级窗口部件
        """
        self.parent_widget = parent_widget
        self.grid_view = None
        self.image_files = []
        
    def setup_grid_view(self, layout, existing_list_view):
        """
        设置网格视图
        
        Args:
            layout: 父级布局
            existing_list_view: 现有的列表视图（将被替换）
        """
        # 创建网格视图
        self.grid_view = ThumbnailGridView(self.parent_widget)
        
        # 获取现有列表视图的位置和大小
        index = layout.indexOf(existing_list_view)
        if index >= 0:
            # 移除现有列表视图
            layout.takeAt(index)
            existing_list_view.setParent(None)
            
            # 添加网格视图到相同位置
            layout.insertWidget(index, self.grid_view)
        
        # 设置网格视图属性
        self.grid_view.setMinimumHeight(200)
        
    def add_files(self, files):
        """
        添加文件到网格视图
        
        Args:
            files: 文件路径列表
            
        Returns:
            list: 成功添加的文件列表
        """
        # 过滤已存在的文件
        new_files = [f for f in files if f not in self.image_files]
        
        if new_files:
            # 添加到数据列表
            self.image_files.extend(new_files)
            
            # 更新网格视图显示
            if self.grid_view:
                self.grid_view.set_files(self.image_files)
            
        return new_files
    
    def remove_selected(self):
        """移除选中的文件"""
        if not self.grid_view:
            return 0
            
        selected_files = self.grid_view.get_selected_files()
        if selected_files:
            # 从数据列表中移除选中的文件
            self.image_files = [f for f in self.image_files if f not in selected_files]
            
            # 更新网格视图
            self.grid_view.set_files(self.image_files)
            
        return len(selected_files)
    
    def clear_all(self):
        """清空所有文件"""
        count = len(self.image_files)
        self.image_files.clear()
        
        if self.grid_view:
            self.grid_view.clear_files()
            
        return count
    
    def get_file_count(self):
        """获取文件数量"""
        return len(self.image_files)
    
    def get_file_paths(self):
        """获取所有文件路径"""
        return self.image_files[:]