"""
主程序入口
"""
import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSettings

from ui_mainwindow import Ui_MainWindow
from managers.image_list_manager import ImageListManager
from services.image_loader_service import ImageLoaderService
from services.conversion_service import ConversionService
from core.utils import show_message, show_question


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 初始化服务和管理器
        self.conversion_service = ConversionService()
        self.loader_service = ImageLoaderService()
        self.image_list_manager = ImageListManager(self.ui.imageList)
        
        # 连接信号和槽
        self._connect_signals()
        
        # 加载设置
        self.settings = QSettings("ImageConverter", "ImageConverter")
        self._load_settings()
        
        # 更新格式选项
        self._update_format_options()
        
    def _connect_signals(self):
        """连接信号和槽"""
        # 输入相关
        self.ui.addImages.clicked.connect(self._select_images)
        self.ui.addDirs.clicked.connect(self._select_directories)
        
        # 输出相关
        self.ui.pushButton.clicked.connect(self._select_output_directory)
        self.ui.qualityValue.valueChanged.connect(self._update_quality_display)
        
        # 图片列表相关
        self.ui.clearSelected.clicked.connect(self._remove_selected)
        self.ui.clearAll.clicked.connect(self._clear_all)
        
        # 转换相关
        self.ui.run.clicked.connect(self._convert_images)
        
    def _select_images(self):
        """选择图片文件"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            "选择图片", 
            "", 
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff *.webp *.heic *.heif *.avif)"
        )
        
        if file_paths:
            self.image_list_manager.add_files(file_paths)
            self._update_selected_count()
            
    def _select_directories(self):
        """选择图片目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择目录")
        if directory:
            # 获取目录下所有图片文件
            image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.webp', '*.heic', '*.heif', '*.avif']
            image_paths = []
            for extension in image_extensions:
                # 使用glob查找文件
                from pathlib import Path
                paths = Path(directory).glob(f"**/{extension}")
                image_paths.extend([str(p) for p in paths])
                
            if image_paths:
                self.image_list_manager.add_files(image_paths)
                self._update_selected_count()
            else:
                show_message(self, "提示", "所选目录中未找到图片文件")
                
    def _select_output_directory(self):
        """选择输出目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if directory:
            self.ui.lineEdit.setText(directory)
            # 保存到设置
            self.settings.setValue("output_dir", directory)
            
    def _update_quality_display(self, value):
        """更新质量显示"""
        self.ui.qualityShow.setText(f"{value}%")
        
    def _update_selected_count(self):
        """更新选中数量显示"""
        count = self.image_list_manager.get_file_count()
        self.ui.selectedNum.display(count)
        
    def _remove_selected(self):
        """移除选中的图片"""
        self.image_list_manager.remove_selected()
        self._update_selected_count()
        
    def _clear_all(self):
        """清除所有图片"""
        self.image_list_manager.clear_all()
        self._update_selected_count()
        
    def _update_format_options(self):
        """更新格式选项"""
        formats = self.conversion_service.get_supported_formats()
        self.ui.formatSelection.clear()
        self.ui.formatSelection.addItems(formats)
        
    def _load_settings(self):
        """加载设置"""
        # 输出目录
        output_dir = self.settings.value("output_dir", "")
        if output_dir:
            self.ui.lineEdit.setText(output_dir)
            
        # 质量设置
        quality = self.settings.value("quality", 100, type=int)
        self.ui.qualityValue.setValue(quality)
        self._update_quality_display(quality)
        
    def _convert_images(self):
        """转换图片"""
        # 检查是否有选中文件
        if self.image_list_manager.get_file_count() == 0:
            show_message(self, "提示", "请先选择要转换的图片")
            return
            
        # 检查输出目录
        output_dir = self.ui.lineEdit.text().strip()
        if not output_dir:
            show_message(self, "提示", "请选择输出目录")
            return
            
        # 确保输出目录存在
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 获取转换参数
        format_ext = self.ui.formatSelection.currentText()
        quality = self.ui.qualityValue.value()
        replace = self.ui.isReplace.isChecked()
        
        # 执行转换
        def on_progress(current, total, filename):
            self.ui.statusbar.showMessage(f"正在转换 ({current}/{total}): {filename}")
            
        def on_complete(success_count, fail_count):
            self.ui.statusbar.showMessage(f"转换完成: 成功 {success_count} 个, 失败 {fail_count} 个")
            show_message(self, "完成", f"转换完成:\n成功: {success_count} 个\n失败: {fail_count} 个")
            
        # 立即显示开始转换的进度信息
        total_files = len(self.image_list_manager.get_file_paths())
        self.ui.statusbar.showMessage(f"开始转换: 共 {total_files} 个文件")
            
        # 在线程中执行转换以避免阻塞UI
        from PySide6.QtCore import QThread, Signal
        
        class ConvertThread(QThread):
            progress_signal = Signal(int, int, str)
            complete_signal = Signal(int, int)
            
            def __init__(self, conversion_service, image_files, output_dir, format_ext, quality, replace):
                super().__init__()
                self.conversion_service = conversion_service
                self.image_files = image_files
                self.output_dir = output_dir
                self.format_ext = format_ext
                self.quality = quality
                self.replace = replace
                
            def run(self):
                def progress_callback(current, total, filename):
                    self.progress_signal.emit(current, total, filename)
                    
                # 立即发送第一个进度信号，显示开始转换
                if self.image_files:
                    self.progress_signal.emit(0, len(self.image_files), "开始转换...")
                    
                success_count, error_count = self.conversion_service.convert_images(
                    self.image_files,
                    self.output_dir,
                    self.format_ext,
                    self.quality,
                    self.replace,
                    progress_callback
                )
                self.complete_signal.emit(success_count, error_count)
        
        # 创建并启动转换线程
        self.convert_thread = ConvertThread(
            self.conversion_service,
            self.image_list_manager.get_file_paths(),
            output_dir,
            format_ext,
            quality,
            replace
        )
        
        # 连接信号
        self.convert_thread.progress_signal.connect(on_progress)
        self.convert_thread.complete_signal.connect(on_complete)
        
        # 启动线程
        self.convert_thread.start()
        
    def closeEvent(self, event):
        """关闭事件，保存设置"""
        # 保存设置
        self.settings.setValue("output_dir", self.ui.lineEdit.text())
        self.settings.setValue("quality", self.ui.qualityValue.value())
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("ImageConverter")
    app.setApplicationDisplayName("图片格式转换器")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
