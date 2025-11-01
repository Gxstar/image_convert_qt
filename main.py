"""
主程序入口
"""
import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSettings

from ui_mainwindow import Ui_MainWindow
from managers.grid_view_manager import GridViewManager
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
        self.grid_view_manager = GridViewManager(self)
        
        # 设置网格视图
        self.grid_view_manager.setup_grid_view(self.ui.verticalLayout_3, self.ui.imageList)
        
        # 初始化变量
        self.bit_depth = None
        
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
        self.ui.outDirSelect.clicked.connect(self._select_output_directory)
        self.ui.qualityValue.valueChanged.connect(self._update_quality_display)
        self.ui.formatSelection.currentTextChanged.connect(self._on_format_changed)
        
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
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp *.heic *.heif *.avif *.gif *.jp2 *.j2k *.cr2 *.cr3 *.nef *.nrw *.arw *.dng *.orf *.rw2 *.pef *.raf *.raw)"
        )
        
        if file_paths:
            self.grid_view_manager.add_files(file_paths)
            self._update_selected_count()
            
    def _select_directories(self):
        """选择图片目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择目录")
        if directory:
            # 定义支持的图片扩展名（包括RAW格式）
            image_extensions = [
                '*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif', '*.webp', 
                '*.heic', '*.heif', '*.avif', '*.gif', '*.jp2', '*.j2k',
                '*.cr2', '*.cr3', '*.nef', '*.nrw', '*.arw', '*.dng', 
                '*.orf', '*.rw2', '*.pef', '*.raf', '*.raw'
            ]
            image_paths = []
            for extension in image_extensions:
                # 使用glob查找文件
                from pathlib import Path
                paths = Path(directory).glob(f"**/{extension}")
                image_paths.extend([str(p) for p in paths])
                
            if image_paths:
                self.grid_view_manager.add_files(image_paths)
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
        count = self.grid_view_manager.get_file_count()
        self.ui.selectedNum.display(count)
        
    def _remove_selected(self):
        """移除选中的图片"""
        self.grid_view_manager.remove_selected()
        self._update_selected_count()
        
    def _clear_all(self):
        """清除所有图片"""
        self.grid_view_manager.clear_all()
        self._update_selected_count()
        
    def _on_format_changed(self, format_name):
        """格式选择变化事件处理"""
        # 更新位深选项
        self._update_bit_depth_options(format_name)
        
        # 如果选择原格式，设置quality为100
        if format_name == "原格式":
            self.ui.qualityValue.setValue(100)
    
    def _update_format_options(self):
        """更新格式选项"""
        formats = self.conversion_service.get_supported_formats()
        self.ui.formatSelection.clear()
        # 添加"原格式"选项
        self.ui.formatSelection.addItem("原格式")
        self.ui.formatSelection.addItems(formats)
        
        # 更新位深选项
        self._update_bit_depth_options(self.ui.formatSelection.currentText())
        
        # 如果选择原格式，设置quality为100
        if self.ui.formatSelection.currentText() == "原格式":
            self.ui.qualityValue.setValue(100)
        
    def _update_bit_depth_options(self, format_name):
        """根据格式更新位深选项"""
        # 清空现有选项
        self.ui.bitValue.clear()
        
        # 如果选择"原格式"，添加"原位深"选项并默认选中
        if format_name == "原格式":
            self.ui.bitValue.addItems(["原位深", "8位", "10位", "12位", "16位"])
            self.ui.bitValue.setCurrentText("原位深")
        # 根据格式设置位深选项
        elif format_name.upper() in ['JPEG', 'WEBP','AVIF']:
            # JPEG、WEBP、AVIF只支持8位
            self.ui.bitValue.addItems(["8位"])
            self.ui.bitValue.setCurrentText("8位")
        elif format_name.upper() in ['PNG', 'TIFF']:
            # PNG和TIFF支持8位和16位
            self.ui.bitValue.addItems(["8位", "16位"])
            self.ui.bitValue.setCurrentText("8位")
        elif format_name.upper() in ['HEIC', 'HEIF']:
            # HEIC、HEIF支持8位、10位、12位
            self.ui.bitValue.addItems(["8位", "10位", "12位"])
            self.ui.bitValue.setCurrentText("8位")
        else:
            # 其他格式默认只支持8位
            self.ui.bitValue.addItems(["8位"])
            self.ui.bitValue.setCurrentText("8位")
        
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
        if self.grid_view_manager.get_file_count() == 0:
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
        
        # 如果选择"原格式"，则format_ext为None，表示保持原格式
        if format_ext == "原格式":
            format_ext = None
        
        # 获取位深参数
        bit_depth_text = self.ui.bitValue.currentText()
        bit_depth = 8  # 默认设置为8位
        if bit_depth_text == "原位深":
            bit_depth = None  # 表示保持原位深
        elif bit_depth_text:
            # 从文本中提取数字
            if "位" in bit_depth_text:
                bit_depth_str = bit_depth_text.replace("位", "")
                try:
                    bit_depth = int(bit_depth_str)
                except ValueError:
                    bit_depth = 8
        
        # 获取图片文件列表
        image_files = self.grid_view_manager.get_file_paths()
        
        # 预扫描冲突（在主线程中执行）
        conflict_info = self.conversion_service._scan_for_conflicts(image_files, output_dir, format_ext, replace)
        
        # 如果有冲突，在主线程中询问用户
        user_decisions = {}
        if conflict_info:
            title, message, total_conflicts = self.conversion_service.get_conflict_summary(conflict_info, replace)
            if show_question(self, title, message):
                user_decisions = self.conversion_service.create_user_decisions(conflict_info, True)
            else:
                user_decisions = self.conversion_service.create_user_decisions(conflict_info, False)
        
        # 执行转换
        def on_progress(current, total, filename):
            self.ui.statusbar.showMessage(f"正在转换 ({current}/{total}): {filename}")
            
        def on_complete(success_count, error_count, conflict_info):
            self.ui.statusbar.showMessage(f"转换完成: 成功 {success_count} 个, 失败 {error_count} 个")
            show_message(self, "完成", f"转换完成:\n成功: {success_count} 个\n失败: {error_count} 个")
            
        # 立即显示开始转换的进度信息
        total_files = len(image_files)
        self.ui.statusbar.showMessage(f"开始转换: 共 {total_files} 个文件")
            
        # 在线程中执行转换以避免阻塞UI
        from PySide6.QtCore import QThread, Signal
        
        class ConvertThread(QThread):
            progress_signal = Signal(int, int, str)
            complete_signal = Signal(int, int, object)
            
            def __init__(self, conversion_service, image_files, output_dir, format_ext, quality, bit_depth, replace, user_decisions, parent_window=None):
                super().__init__()
                self.conversion_service = conversion_service
                self.image_files = image_files
                self.output_dir = output_dir
                self.format_ext = format_ext
                self.quality = quality
                self.bit_depth = bit_depth
                self.replace = replace
                self.user_decisions = user_decisions
                self.parent_window = parent_window
                
            def run(self):
                def progress_callback(current, total, filename):
                    self.progress_signal.emit(current, total, filename)
                    
                # 立即发送第一个进度信号，显示开始转换
                if self.image_files:
                    self.progress_signal.emit(0, len(self.image_files), "开始转换...")
                    
                success_count, error_count, conflict_info = self.conversion_service.convert_images(
                    self.image_files,
                    self.output_dir,
                    self.format_ext,
                    self.quality,
                    self.bit_depth,  # 传递位深参数
                    self.replace,
                    progress_callback,
                    self.parent_window,
                    self.user_decisions  # 传递用户决策
                )
                self.complete_signal.emit(success_count, error_count, conflict_info)
        
        # 创建并启动转换线程
        self.convert_thread = ConvertThread(
            self.conversion_service,
            image_files,  # 使用预处理的图片文件列表
            output_dir,
            format_ext,
            quality,
            bit_depth,  # 传递位深参数
            replace,
            user_decisions,  # 传递用户决策
            self  # 传递父窗口引用
        )
        
        # 连接信号
        self.convert_thread.progress_signal.connect(on_progress)
        self.convert_thread.complete_signal.connect(on_complete)
        
        # 启动线程
        self.convert_thread.start()
        
    def closeEvent(self, event):
        """关闭事件，保存设置并清理资源"""
        # 保存设置
        self.settings.setValue("output_dir", self.ui.lineEdit.text())
        self.settings.setValue("quality", self.ui.qualityValue.value())
        
        # 清理缩略图管理器的工作线程
        if hasattr(self.grid_view_manager, 'thumbnail_manager'):
            self.grid_view_manager.thumbnail_manager.cleanup()
        
        event.accept()


def main():
    app = QApplication(sys.argv)
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    # 设置应用程序信息
    app.setApplicationName("ImageConverter")
    app.setApplicationDisplayName("图片格式转换器")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
