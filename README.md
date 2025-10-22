# 🏷️ 标签打印排版工具 | Label Printer

一个现代化的标签批量打印排版工具，支持将标签图片自动排列到A4纸上生成PDF，并提供实时预览和直接打印功能。

A modern label batch printing tool that automatically arranges label images on A4 paper to generate PDFs, with real-time preview and direct printing capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 主要特性 | Key Features

### 🎨 现代化界面
- **Material Design** 风格的用户界面
- 清晰直观的操作流程
- 实时PDF预览功能
- 响应式布局设计

### 🌍 多语言支持
- **中文** (简体中文)
- **泰语** (ภาษาไทย)
- 一键切换语言

### 📐 灵活的排版设置
- 自定义行数和列数 (1-10)
- 可调节页边距 (0-30mm)
- 可调节标签间距 (0-20mm)
- 支持横向/竖向A4纸张
- 自动计算标签数量

### 💾 智能参数保存
- 自动保存上次使用的参数
- 包括行数、列数、边距、间距、方向
- 下次打开自动恢复设置

### 🖨️ 强大的打印功能
- **生成PDF**: 保存为高质量PDF文件
- **生成并打印**: 一键生成并调用打印对话框
- **PDF预览**: 生成前实时预览效果
- **强制预览**: 必须先预览才能生成，避免错误

### 📁 文件管理
- 所有生成的文件保存在 `outputs` 文件夹
- 文件名自动添加时间戳 (格式: `label{月日时分}.pdf`)
- 支持一键打开文件所在位置
- PNG打印文件永久保留

## 🚀 快速开始 | Quick Start

### 环境要求 | Requirements

- Python 3.8 或更高版本
- Windows 10/11 (推荐)

### 安装依赖 | Installation

```bash
pip install PyQt6 Pillow reportlab PyMuPDF
```

### 运行程序 | Run

```bash
python label_gui_qt.py
```

## 📖 使用说明 | Usage Guide

### 1️⃣ 选择标签图片
点击"浏览"按钮，选择要打印的标签图片文件（支持 PNG、JPG、JPEG 格式）

### 2️⃣ 调整排版参数
- **行数**: 设置每页纸上的标签行数
- **列数**: 设置每页纸上的标签列数
- **边距**: 设置页面四周的边距
- **间距**: 设置标签之间的间距
- **方向**: 选择横向或竖向排版

### 3️⃣ 生成预览
点击"🔄 生成预览"按钮，在右侧查看PDF效果

### 4️⃣ 生成或打印
- **📄 生成 PDF**: 保存PDF文件到 `outputs` 文件夹
- **🖨️ 生成并打印**: 生成PDF和PNG，并调用打印对话框

## 📂 项目结构 | Project Structure

```
label-printer/
├── label_gui_qt.py          # 主程序文件
├── label.ico                # 程序图标 (ICO格式)
├── label.png                # 程序图标 (PNG格式)
├── label.svg                # 程序图标 (SVG格式)
├── settings.json            # 用户设置文件 (自动生成)
├── .gitignore              # Git忽略规则
├── README.md               # 项目说明文档
└── outputs/                # 输出文件夹 (自动创建)
    ├── label{timestamp}.pdf  # 生成的PDF文件
    └── label{timestamp}.png  # 打印用PNG文件
```

## 🛠️ 技术栈 | Tech Stack

- **GUI框架**: PyQt6
- **图像处理**: Pillow (PIL)
- **PDF生成**: ReportLab
- **PDF处理**: PyMuPDF (fitz)
- **打印支持**: PyQt6.QtPrintSupport

## 🎯 核心功能实现

### PDF预览
使用 PyMuPDF 将生成的PDF转换为高分辨率图片，实时显示在界面右侧

### 打印功能
1. 生成PDF文件
2. 使用 PyMuPDF 将PDF转换为300 DPI的PNG图片
3. 调用 Windows 系统打印对话框
4. PNG文件保留在 `outputs` 文件夹供后续使用

### 参数保存
使用 JSON 格式保存用户设置，包括：
- 界面语言
- 排版参数（行数、列数、边距、间距）
- 页面方向

## 📝 开发说明 | Development

### 🌐 局域网 Web 服务改造 | Web Service Migration

如果希望将本工具改造成在 Windows Server 上运行的局域网 Web 服务，并通过浏览器供多台电脑使用，请参考 [docs/web_service_migration.md](docs/web_service_migration.md)，其中包含架构方案、改造步骤和工作量评估。

### 打包为EXE

使用 PyInstaller 打包程序：

```bash
# 目录模式打包 (推荐，文件较大时使用)
pyinstaller --name="标签打印工具" --windowed --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py

# 单文件模式打包 (文件较小时使用)
pyinstaller --name="标签打印工具" --windowed --onefile --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py
```

打包后的程序位于 `dist/标签打印工具/` 文件夹中。

### 代码结构

- **LabelPrinterQt**: 主窗口类
  - `init_ui()`: 初始化界面
  - `generate_preview()`: 生成PDF预览
  - `generate_pdf()`: 生成PDF文件
  - `generate_and_print_pdf()`: 生成并打印
  - `tile_label_image_to_pdf()`: 核心PDF生成逻辑
  - `load_settings()` / `save_settings()`: 参数管理

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

## 📄 许可证 | License

MIT License

## 👨‍💻 作者 | Author

开发者: [Your Name]

## 🙏 致谢 | Acknowledgments

- PyQt6 团队提供的优秀GUI框架
- ReportLab 提供的PDF生成库
- PyMuPDF 提供的PDF处理能力

---

**注意**: 本程序主要针对 Windows 系统优化，在其他操作系统上可能需要调整部分功能。

**Note**: This program is primarily optimized for Windows systems and may require adjustments for other operating systems.
