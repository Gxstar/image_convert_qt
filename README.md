# 图片格式转换器

基于PySide6和PIL开发的桌面图片格式转换工具，支持多种图片格式的批量转换。

## 功能特性

- 🖼️ 支持多种图片格式：JPEG、PNG、BMP、TIFF、WebP、HEIC、HEIF、AVIF
- 📁 支持单文件选择和文件夹批量选择
- ⚙️ 可调节输出图片质量
- 🔄 支持批量格式转换
- 📊 实时显示转换进度
- ✅ 可选择是否替换同名文件
- 📷 自动保留图片EXIF信息

## 安装运行

### 环境要求
- Python 3.13+
- PySide6 6.10.0+
- Pillow 12.0.0+

### 安装依赖
```bash
uv sync
```

### 运行应用
```bash
python main.py
```

## 使用方法

1. **添加图片**：点击"选择图片"或"选择文件夹"按钮
2. **设置输出**：选择目标格式、输出目录和质量
3. **执行转换**：点击"执行"按钮开始批量转换

## 支持的格式

- **输入格式**：JPG/JPEG、PNG、BMP、TIFF、WebP、HEIC、HEIF、AVIF
- **输出格式**：JPEG、PNG、BMP、TIFF、WebP、HEIC、HEIF、AVIF

## 项目结构

```
image_convert_qt/
├── main.py                 # 主应用程序
├── ui_mainwindow.py        # UI界面代码
├── core/                   # 核心功能模块
│   ├── image_converter.py  # 图片转换器
│   └── utils.py           # 工具函数
├── services/               # 服务层
│   ├── conversion_service.py    # 转换服务
│   └── image_loader_service.py  # 图片加载服务
├── managers/               # 管理器层
│   └── image_list_manager.py    # 图片列表管理
└── pyproject.toml         # 项目配置
```

## 技术栈

- **GUI框架**：PySide6
- **图片处理**：Pillow (PIL)
- **包管理**：uv

## 许可证

MIT License