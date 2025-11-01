# 图片格式转换器

基于PySide6和PIL开发的桌面图片格式转换工具，支持多种图片格式的批量转换和缩略图预览。

## 功能特性

- 🖼️ **缩略图网格视图**：CSS cover效果的缩略图显示，支持异步加载
- 📁 **批量处理**：支持单文件和文件夹批量选择
- 🔄 **格式转换**：支持多种图片格式互转
- ⚙️ **质量调节**：可调节输出图片质量
- 📊 **进度显示**：实时显示转换进度
- 📷 **EXIF保留**：自动保留图片EXIF信息

## 快速开始

### 安装依赖
```bash
uv sync
```

### 运行应用
```bash
python main.py
```

## 使用方法

1. **添加图片**：选择图片或文件夹
2. **预览缩略图**：在网格视图中查看图片缩略图
3. **设置转换**：选择目标格式、输出目录和质量
4. **执行转换**：开始批量转换

## 项目结构

```
image_convert_qt/
├── main.py                 # 主应用程序
├── widgets/               # 界面组件
│   └── thumbnail_grid_view.py  # 缩略图网格视图
├── managers/              # 管理器
│   ├── thumbnail_manager.py    # 缩略图管理
│   └── grid_view_manager.py    # 网格视图管理
├── core/                  # 核心功能
│   └── image_converter.py      # 图片转换
└── services/              # 服务层
    └── conversion_service.py   # 转换服务
```

## 技术栈

- **GUI框架**：PySide6
- **图片处理**：Pillow
- **包管理**：uv

## 一些遇到的问题

- pillow无法处理raw格式的输入，且不支持大于8位的RGB图像。输出16位png、tiff格式时，采用opencv输出。
- pyexiv2无法向heif、heic、avif格式的图片写入exif信息，采用中间内存图片的方式解决。
- rawpy官方版本使用的libraw库无法支持最新某些相机的raw格式，我手动编译了最新版本的libraw库、rawpy包，解决了这个问题。

MIT License