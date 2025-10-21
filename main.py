"""
图片格式转换工具 - 主程序
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PySide6.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from utils import get_image_files, show_message, show_question
from image_converter import ImageConverter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("图片格式转换工具")
        
        # 初始化数据
        self.image_files = []
        self.converter = ImageConverter()
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号和槽
        self.connect_signals()
    
    def init_ui(self):
        """初始化UI设置"""
        # 设置输出格式选项
        formats = ["JPEG", "PNG", "BMP", "GIF", "TIFF", "WebP"]
        self.ui.formatSelection.addItems(formats)
        
        # 设置质量滑块范围
        self.ui.qualityValue.setRange(1, 100)
        self.ui.qualityValue.setValue(85)
        
        # 设置列表视图
        self.ui.imageList.setAlternatingRowColors(True)
    
    def connect_signals(self):
        """连接信号和槽"""
        # 质量滑块数值更新
        self.ui.qualityValue.valueChanged.connect(self.update_quality_display)
        
        # 图片选择按钮
        self.ui.addImages.clicked.connect(self.select_images)
        self.ui.addDirs.clicked.connect(self.select_directory)
        
        # 输出目录选择
        self.ui.pushButton.clicked.connect(self.select_output_directory)
        
        # 清除按钮
        self.ui.clearSelected.clicked.connect(self.clear_selected)
        self.ui.clearAll.clicked.connect(self.clear_all)
        
        # 执行按钮
        self.ui.run.clicked.connect(self.start_conversion)
    
    def update_quality_display(self, value):
        """更新质量显示"""
        self.ui.qualityShow.setText(str(value))
    
    def select_images(self):
        """选择图片文件"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("图片文件 (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp)")
        
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            self.add_images_to_list(files)
    
    def select_directory(self):
        """选择文件夹"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择图片文件夹", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            image_files = get_image_files(directory)
            if image_files:
                self.add_images_to_list(image_files)
            else:
                show_message(self, "提示", "所选文件夹中没有找到图片文件")
    
    def add_images_to_list(self, files):
        """添加图片到列表"""
        new_files = []
        for file_path in files:
            if file_path not in self.image_files:
                self.image_files.append(file_path)
                new_files.append(file_path)
        
        # 更新列表显示
        import os
        for file_path in new_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)  # 存储完整路径
            self.ui.imageList.addItem(item)
        
        # 更新已选数量
        self.update_selected_count()
        
        if new_files:
            self.ui.statusbar.showMessage(f"已添加 {len(new_files)} 张图片", 3000)
    
    def update_selected_count(self):
        """更新已选图片数量显示"""
        count = len(self.image_files)
        self.ui.selectedNum.display(count)
    
    def select_output_directory(self):
        """选择输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择输出目录", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            self.ui.lineEdit.setText(directory)
            self.ui.statusbar.showMessage(f"输出目录: {directory}", 3000)
    
    def clear_selected(self):
        """清除已选项目"""
        selected_items = self.ui.imageList.selectedItems()
        if not selected_items:
            show_message(self, "提示", "请先选择要清除的图片")
            return
        
        for item in selected_items:
            file_path = item.data(Qt.UserRole)
            if file_path in self.image_files:
                self.image_files.remove(file_path)
            self.ui.imageList.takeItem(self.ui.imageList.row(item))
        
        self.update_selected_count()
        self.ui.statusbar.showMessage(f"已清除 {len(selected_items)} 张图片", 3000)
    
    def clear_all(self):
        """清除所有图片"""
        if not self.image_files:
            show_message(self, "提示", "列表为空")
            return
        
        if show_question(self, "确认", "确定要清除所有图片吗？"):
            self.image_files.clear()
            self.ui.imageList.clear()
            self.update_selected_count()
            self.ui.statusbar.showMessage("已清除所有图片", 3000)
    
    def start_conversion(self):
        """开始图片转换"""
        if not self.image_files:
            show_message(self, "警告", "请先添加要转换的图片", self.style().standardIcon(self.style().SP_MessageBoxWarning))
            return
        
        output_dir = self.ui.lineEdit.text()
        if not output_dir:
            show_message(self, "警告", "请选择输出目录", self.style().standardIcon(self.style().SP_MessageBoxWarning))
            return
        
        # 获取转换参数
        output_format = self.ui.formatSelection.currentText().lower()
        quality = self.ui.qualityValue.value()
        replace_existing = self.ui.isReplace.isChecked()
        
        # 禁用执行按钮
        self.ui.run.setEnabled(False)
        self.ui.statusbar.showMessage("正在转换图片...")
        
        try:
            # 批量转换
            stats = self.converter.batch_convert(
                self.image_files, output_dir, output_format, quality, replace_existing
            )
            
            # 显示结果
            self._show_conversion_result(stats)
            
        except Exception as e:
            show_message(self, "错误", f"转换过程中发生错误: {str(e)}", self.style().standardIcon(self.style().SP_MessageBoxCritical))
        
        finally:
            # 重新启用执行按钮
            self.ui.run.setEnabled(True)
    
    def _show_conversion_result(self, stats):
        """显示转换结果"""
        success_count = stats['success']
        error_count = stats['error']
        skipped_count = stats['skipped']
        
        if error_count == 0 and skipped_count == 0:
            message = f"转换完成！成功转换 {success_count} 张图片"
            self.ui.statusbar.showMessage(message, 5000)
            show_message(self, "完成", message)
        else:
            message = f"转换完成！\n成功: {success_count} 张"
            if error_count > 0:
                message += f"\n失败: {error_count} 张"
            if skipped_count > 0:
                message += f"\n跳过: {skipped_count} 张"
            
            self.ui.statusbar.showMessage(message.replace('\n', '，'), 5000)
            show_message(self, "完成", message, self.style().standardIcon(self.style().SP_MessageBoxWarning))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
