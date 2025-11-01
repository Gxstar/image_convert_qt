"""
缩略图网格视图组件
"""
import os
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtWidgets import QListView, QAbstractItemView, QStyledItemDelegate, QStyle
from PySide6.QtGui import QPainter, QFontMetrics, QPalette, QBrush, QPen

from managers.thumbnail_manager import ThumbnailManager


class ThumbnailDelegate(QStyledItemDelegate):
    """缩略图项委托"""
    
    def __init__(self, thumbnail_manager, parent=None):
        super().__init__(parent)
        self.thumbnail_manager = thumbnail_manager
        self.thumbnail_size = QSize(100, 100)
        self.text_height = 30
        self.item_margin = 8
        self.item_size = QSize(
            self.thumbnail_size.width() + self.item_margin * 2,
            self.thumbnail_size.height() + self.text_height + self.item_margin * 2
        )
    
    def sizeHint(self, option, index):
        """返回项的大小"""
        return self.item_size
    
    def paint(self, painter, option, index):
        """绘制项"""
        painter.save()
        
        # 设置背景
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, option.palette.alternateBase())
        else:
            painter.fillRect(option.rect, option.palette.base())
        
        # 获取文件路径
        file_path = index.data(Qt.UserRole)
        if not file_path:
            # 如果UserRole没有数据，尝试从模型获取
            model = index.model()
            if hasattr(model, 'file_paths') and index.row() < len(model.file_paths):
                file_path = model.file_paths[index.row()]
            else:
                painter.restore()
                return
        
        # 计算缩略图位置
        thumbnail_rect = QRect(
            option.rect.left() + self.item_margin,
            option.rect.top() + self.item_margin,
            self.thumbnail_size.width(),
            self.thumbnail_size.height()
        )
        
        # 绘制缩略图
        thumbnail = self.thumbnail_manager.get_thumbnail(file_path)
        if thumbnail:
            # 缩放缩略图以适应指定大小
            scaled_thumbnail = thumbnail.scaled(
                self.thumbnail_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # 居中显示缩略图
            x_offset = (self.thumbnail_size.width() - scaled_thumbnail.width()) // 2
            y_offset = (self.thumbnail_size.height() - scaled_thumbnail.height()) // 2
            
            painter.drawPixmap(
                thumbnail_rect.left() + x_offset,
                thumbnail_rect.top() + y_offset,
                scaled_thumbnail
            )
        else:
            # 绘制占位符
            painter.setPen(QPen(option.palette.mid(), 1))
            painter.setBrush(QBrush(option.palette.window()))
            painter.drawRect(thumbnail_rect)
            
            # 绘制加载中文字
            painter.setPen(QPen(option.palette.text().color()))
            painter.drawText(thumbnail_rect, Qt.AlignCenter, "加载中...")
        
        # 绘制文件名
        file_name = os.path.basename(file_path)
        text_rect = QRect(
            option.rect.left() + self.item_margin,
            option.rect.top() + self.thumbnail_size.height() + self.item_margin,
            self.thumbnail_size.width(),
            self.text_height
        )
        
        # 设置文本颜色
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(option.palette.highlightedText().color()))
        else:
            painter.setPen(QPen(option.palette.text().color()))
        
        # 绘制文件名（自动省略）
        metrics = QFontMetrics(painter.font())
        elided_text = metrics.elidedText(file_name, Qt.TextElideMode.ElideMiddle, text_rect.width())
        painter.drawText(text_rect, Qt.AlignCenter, elided_text)
        
        # 绘制边框
        painter.setPen(QPen(option.palette.mid(), 1))
        painter.drawRect(option.rect.adjusted(0, 0, -1, -1))
        
        painter.restore()


class ThumbnailGridView(QListView):
    """缩略图网格视图"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 初始化缩略图管理器
        self.thumbnail_manager = ThumbnailManager()
        
        # 设置视图属性
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setMovement(QListView.Movement.Static)
        self.setUniformItemSizes(True)
        self.setSpacing(10)
        self.setGridSize(QSize(120, 150))  # 网格大小
        
        # 禁用视图优化，确保所有项目都能正确渲染
        self.setViewportMargins(0, 0, 0, 0)
        self.setBatchSize(100)  # 增加批量处理大小
        
        # 设置委托
        self.delegate = ThumbnailDelegate(self.thumbnail_manager, self)
        self.setItemDelegate(self.delegate)
        
        # 设置选择模式
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragEnabled(True)
        
        # 连接信号
        self.thumbnail_manager.thumbnail_loaded.connect(self._on_thumbnail_loaded)
        self.destroyed.connect(self._cleanup)
    
    def set_files(self, file_paths):
        """设置文件列表"""
        from PySide6.QtCore import QAbstractListModel, QModelIndex
        
        class ThumbnailListModel(QAbstractListModel):
            def __init__(self, file_paths):
                super().__init__()
                self.file_paths = file_paths
            
            def rowCount(self, parent=QModelIndex()):
                return len(self.file_paths)
            
            def data(self, index, role=Qt.DisplayRole):
                if not index.isValid() or index.row() >= len(self.file_paths):
                    return None
                
                file_path = self.file_paths[index.row()]
                
                if role == Qt.DisplayRole:
                    # 显示文件名
                    return os.path.basename(file_path)
                elif role == Qt.UserRole:
                    # 存储文件路径
                    return file_path
                elif role == Qt.DecorationRole:
                    # 返回缩略图（异步加载）
                    return None
                
                return None
        
        # 创建自定义模型
        model = ThumbnailListModel(file_paths)
        self.setModel(model)
        
        # 清空之前的缩略图缓存
        self.thumbnail_manager.clear_cache()
    
    def clear_files(self):
        """清空文件列表"""
        self.setModel(None)
        self.thumbnail_manager.clear_cache()
    
    def get_selected_files(self):
        """获取选中的文件路径"""
        selected_indexes = self.selectedIndexes()
        selected_files = []
        
        for index in selected_indexes:
            file_path = index.data(Qt.UserRole)
            if file_path:
                selected_files.append(file_path)
        
        return selected_files
    
    def _on_thumbnail_loaded(self, file_path):
        """缩略图加载完成，刷新视图"""
        # 找到包含该文件路径的索引并刷新
        model = self.model()
        if model and hasattr(model, 'file_paths'):
            try:
                index = model.file_paths.index(file_path)
                model_index = model.index(index, 0)
                self.update(model_index)
            except ValueError:
                pass  # 文件路径不在模型中
    
    def _cleanup(self):
        """清理资源"""
        self.thumbnail_manager.clear_cache()