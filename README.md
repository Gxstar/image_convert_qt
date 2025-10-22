# 图片格式转换工具

一个基于PySide6和PIL库开发的桌面图片格式转换工具，支持多种图片格式的批量转换。

## 功能特性

- 🖼️ 支持多种图片格式：JPEG、PNG、BMP、GIF、TIFF、WebP
- 📁 支持单文件选择和文件夹批量选择
- ⚙️ 可调节输出图片质量（适用于JPEG和WebP格式）
- 🔄 支持批量格式转换
- 📊 实时显示已选图片数量
- ✅ 可选择是否替换同名文件
- 🎯 简洁直观的用户界面
- 📷 自动保留图片EXIF信息（支持JPEG、WebP、TIFF格式）

## 安装和运行

### 环境要求
- Python 3.13+
- PySide6 6.10.0+
- Pillow 12.0.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

如果使用uv作为包管理工具：
```bash
uv sync
```

### 运行应用
```bash
python main.py
```

## 使用方法

1. **添加图片**
   - 点击"选择图片"按钮选择单个或多个图片文件
   - 点击"选择文件夹"按钮批量添加文件夹内的所有图片

2. **设置输出选项**
   - 在"输出格式选择"下拉框中选择目标格式
   - 点击"选择目录"按钮设置输出目录
   - 使用"输出质量"滑块调整图片质量（1-100）
   - 勾选"是否替换同名文件"选项控制文件覆盖行为

3. **管理图片列表**
   - 在右侧列表中查看已添加的图片
   - 使用"清除已选"按钮删除选中的图片
   - 使用"清除所有"按钮清空整个列表

4. **执行转换**
   - 点击"执行"按钮开始批量转换
   - 转换完成后会显示成功和失败的统计信息

## 支持的图片格式

- **输入格式**：JPG/JPEG、PNG、BMP、GIF、TIFF、WebP
- **输出格式**：JPEG、PNG、BMP、GIF、TIFF、WebP

## 注意事项

- 转换JPEG格式时，透明背景会被自动填充为白色
- 建议设置合适的输出质量以平衡文件大小和图片质量
- 大量图片转换可能需要一些时间，请耐心等待
- 程序会自动保留图片的EXIF信息（如拍摄时间、相机型号等）
- EXIF信息在JPEG、WebP、TIFF格式间转换时保留，转换为PNG、HEIF、HEIC、AVIF等其他格式时将不保留EXIF信息

## 技术栈

- **GUI框架**：PySide6
- **图片处理**：Pillow (PIL)
- **UI设计**：Qt Designer
- **构建工具**：Python标准库

## 项目结构

```
image_convert_qt/
├── main.py              # 主应用程序文件
├── main.ui              # Qt Designer UI文件
├── ui_mainwindow.py     # 转换后的Python UI代码
├── pyproject.toml       # 项目配置文件
├── README.md           # 项目说明文档
└── requirements.txt    # 依赖列表
```

## 开发说明

UI文件使用Qt Designer设计，通过以下命令转换为Python代码：
```bash
pyside6-uic main.ui -o ui_mainwindow.py
```

## 许可证

MIT License