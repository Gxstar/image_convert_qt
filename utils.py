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
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(Path(directory).glob(f"*{ext}"))
        image_files.extend(Path(directory).glob(f"*{ext.upper()}"))
    
    return [str(f) for f in image_files]


def show_message(parent, title, message, icon=QMessageBox.Information):
    """
    显示消息对话框
    
    Args:
        parent: 父窗口
        title: 标题
        message: 消息内容
        icon: 图标类型
    """
    QMessageBox(icon, title, message).exec()


def show_question(parent, title, message):
    """
    显示确认对话框
    
    Args:
        parent: 父窗口
        title: 标题
        message: 消息内容
        
    Returns:
        bool: 用户选择结果
    """
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return reply == QMessageBox.Yes


def ensure_directory(directory):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)


def get_output_filename(input_path, output_format):
    """
    生成输出文件名
    
    Args:
        input_path: 输入文件路径
        output_format: 输出格式
        
    Returns:
        str: 输出文件名
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    return f"{base_name}.{output_format}"