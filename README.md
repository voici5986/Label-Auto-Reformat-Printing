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
- 精致的视觉层次（组框边框、渐变背景）
- 专业的加载动画（旋转指示器 + 半透明遮罩）

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

## � 下载与安装 | Download & Install

**对于普通用户 | For End Users**：

无需安装 Python 或配置环境，直接下载即可使用。
No Python required. Simply download and run.

1. 访问发布页面: [**Releases 页面**](https://github.com/voici5986/Label-Auto-Reformat-Printing/releases)
2. 下载最新版本的 `Label-Auto-Reformat-Printing-Windows-x64.zip`
3. 解压后运行 `Label-Auto-Reformat-Printing.exe`

---

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


## 🚀 开发者指南 | Developer Guide

### 环境要求 | Requirements

- Python 3.13
- Windows 10/11 (推荐)
- [Poetry](https://python-poetry.org/) (推荐的依赖管理工具)

### 安装依赖 | Installation

**推荐方式**（使用 Poetry）：
```bash
poetry install
```

**或手动安装**：
```bash
pip install PyQt6 Pillow reportlab PyMuPDF
```

### 运行程序 | Run

```bash
# 使用 Poetry 运行
poetry run python label_gui_qt.py

# 或在激活的虚拟环境中运行
python label_gui_qt.py
```


## 📂 项目结构 | Project Structure

```
label-printer/
├── label_gui_qt.py          # 启动入口（负责启动画面与主窗体加载）
├── __version__.py           # 版本信息管理
├── requirements.txt         # 项目依赖清单
├── label_bundle.spec        # PyInstaller 打包配置（目录模式）
├── config/                  # 配置模块（默认设置、设置服务、参数验证）
├── i18n/                    # 多语言字典
├── services/                # 业务服务（PDF/PIL 处理、输入验证等）
├── ui/                      # 界面组件（主窗口、面板、样式、UI 常量）
├── widgets/                 # 可复用自定义控件（AspectRatioLabel、加载动画、特效）
├── outputs/                 # 自动生成的输出目录（PDF/PNG）
├── label.ico / label.png    # 程序图标资源
├── settings.json            # 用户设置（运行时自动生成/更新）
├── README.md                # 项目说明文档
└── 打包优化方案.md          # 打包与减体积方案
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

### 参数保存与验证
使用 JSON 格式保存用户设置，并自动验证配置有效性：
- 界面语言（zh/th）
- 排版参数（行数、列数、边距、间距）
- 页面方向（landscape/portrait）
- 自动验证并修正无效配置值

## 📝 开发说明 | Development

### 打包为EXE

使用 PyInstaller 打包程序（推荐使用 Poetry 调用）：

```bash
# 推荐：使用项目提供的目录模式 spec（包含排除/隐藏导入优化）
poetry run pyinstaller label_bundle.spec

# 输出目录
# dist/Label-Auto-Reformat-Printing-Windows-x64.zip (包含自动压缩的发布包)
# dist/Label-Auto-Reformat-Printing/ (解压后的文件夹)
```

> 如需单文件模式，可在 `label_bundle.spec` 基础上调整 `EXE` 与 `COLLECT` 配置，或另写专用 spec。

### 模块概览 | Code Layout

- **label_gui_qt.py**: 程序入口，负责加载字体/启动画面并实例化主窗口
- **__version__.py**: 版本信息管理（版本号、作者、描述）
- **ui/**
  - `main_window.py`: `LabelPrinterQt` 主窗口逻辑（布局、信号槽、业务协调）
  - `control_panel.py`: 左侧控制面板
  - `preview_panel.py`: 右侧预览面板（固定长宽比）
  - `styles.py`: 全局样式表与 UI 常量（`AppConstants`）
- **services/pdf_service.py**: PDF 拼版、预览转换、PDF→PNG 打印辅助、参数验证
- **config/**: 默认设置常量、设置读写服务、配置验证器
- **i18n/**: 多语言文案字典及访问接口
- **widgets/**: 通用控件（`AspectRatioLabel`、`LoadingOverlay` 加载动画）与阴影效果

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

## 📄 许可证 | License

MIT License

## 👨‍💻 作者 | Author

开发者: CW

## 🙏 致谢 | Acknowledgments

- PyQt6 团队提供的优秀GUI框架
- ReportLab 提供的PDF生成库
- PyMuPDF 提供的PDF处理能力

---

**注意**: 本程序主要针对 Windows 系统优化，在其他操作系统上可能需要调整部分功能。

**Note**: This program is primarily optimized for Windows systems and may require adjustments for other operating systems.
