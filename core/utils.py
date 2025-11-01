"""
工具函数模块
"""
import os
from pathlib import Path
from PySide6.QtWidgets import QMessageBox


def get_image_files(directory):
    """
    获取目录中的所有图片文件
    
    Args:
        directory: 目标目录路径
        
    Returns:
        list: 图片文件路径列表
    """
    image_extensions = {'.jpg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        # 使用一次glob调用，避免重复（Windows系统glob不区分大小写）
        image_files.extend(Path(directory).glob(f"*{ext}"))
    
    # 去重处理，确保每个文件只出现一次
    unique_files = list(set(image_files))
    return [str(f) for f in unique_files]


def show_message(parent, title, message, icon=None, non_blocking=False):
    """
    显示消息对话框
    
    Args:
        parent: 父窗口
        title: 标题
        message: 消息内容
        icon: 图标
        non_blocking: 是否使用非阻塞模式（推荐在批量处理中使用）
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    if icon:
        msg_box.setIconPixmap(icon.pixmap(32, 32))
    else:
        msg_box.setIcon(QMessageBox.Information)
    
    if non_blocking:
        # 非阻塞模式：使用show()而不是exec()
        msg_box.show()
        # 设置自动关闭定时器（3秒后自动关闭）
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.singleShot(3000, msg_box.close)
    else:
        # 阻塞模式：使用exec()
        msg_box.exec()


def show_question(parent, title, message):
    """
    显示确认对话框
    
    Args:
        parent: 父窗口
        title: 标题
        message: 消息内容
        
    Returns:
        bool: 用户是否点击了"是"
    """
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return reply == QMessageBox.Yes