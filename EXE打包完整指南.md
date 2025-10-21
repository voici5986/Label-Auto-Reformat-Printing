# Python程序打包为EXE完整指南

## 📋 目录
1. [环境准备](#环境准备)
2. [安装PyInstaller](#安装pyinstaller)
3. [打包步骤](#打包步骤)
4. [常见问题解决](#常见问题解决)
5. [高级配置](#高级配置)

---

## 🔧 环境准备

### 1. 确认Python环境
```bash
# 检查Python版本（建议3.8+）
python --version

# 检查pip版本
pip --version
```

### 2. 确认项目依赖
确保所有依赖库都已安装：
```bash
pip list
```

本项目需要的主要依赖：
- PyQt6
- PyQt6-Qt6
- Pillow
- reportlab

---

## 📦 安装PyInstaller

### 方法一：使用pip安装（推荐）
```bash
pip install pyinstaller
```

### 方法二：升级到最新版本
```bash
pip install --upgrade pyinstaller
```

### 验证安装
```bash
pyinstaller --version
```

---

## 🚀 打包步骤

### 步骤1：清理旧文件（可选但推荐）
```bash
# 删除之前的打包文件
rmdir /s /q build
rmdir /s /q dist
del *.spec
```

### 步骤2：基础打包命令
```bash
# 最简单的打包方式
pyinstaller label_gui_qt.py
```

### 步骤3：带图标的打包（推荐）
```bash
# 使用图标文件打包
pyinstaller --onefile --windowed --icon=label.ico --name=标签打印工具 label_gui_qt.py
```

### 步骤4：使用spec文件打包（最推荐）
```bash
# 使用现有的spec配置文件
pyinstaller label_printer.spec
```

---

## 📝 打包参数详解

### 常用参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--onefile` | 打包成单个EXE文件 | `--onefile` |
| `--windowed` | 不显示控制台窗口（GUI程序必用） | `--windowed` |
| `--icon` | 设置程序图标 | `--icon=label.ico` |
| `--name` | 设置输出文件名 | `--name=标签打印工具` |
| `--add-data` | 添加数据文件 | `--add-data "label.ico;."` |
| `--noconsole` | 同`--windowed` | `--noconsole` |
| `--clean` | 清理临时文件后打包 | `--clean` |

### 完整打包命令示例
```bash
pyinstaller --onefile ^
            --windowed ^
            --icon=label.ico ^
            --name=标签打印工具 ^
            --add-data "label.ico;." ^
            --clean ^
            label_gui_qt.py
```

---

## 🎯 使用Spec文件（推荐方式）

### 什么是Spec文件？
Spec文件是PyInstaller的配置文件，可以精确控制打包过程。

### 生成Spec文件
```bash
# 生成基础spec文件
pyi-makespec --onefile --windowed --icon=label.ico label_gui_qt.py
```

### 编辑Spec文件
打开生成的 `label_gui_qt.spec` 文件，可以看到类似内容：

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['label_gui_qt.py'],
    pathex=[],
    binaries=[],
    datas=[('label.ico', '.')],  # 添加图标文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='标签打印工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='label.ico',  # 设置图标
)
```

### 使用Spec文件打包
```bash
pyinstaller label_printer.spec
```

---

## ⚠️ 常见问题解决

### 问题1：打包后程序无法运行
**原因**：缺少依赖或资源文件

**解决方案**：
```bash
# 方法1：使用--hidden-import添加隐藏导入
pyinstaller --hidden-import=PyQt6.QtPrintSupport label_gui_qt.py

# 方法2：在spec文件中添加
hiddenimports=['PyQt6.QtPrintSupport'],
```

### 问题2：图标不显示
**原因**：图标文件未正确打包

**解决方案**：
```bash
# 确保图标文件存在
dir label.ico

# 使用--add-data参数
pyinstaller --add-data "label.ico;." label_gui_qt.py
```

### 问题3：打包文件过大
**原因**：包含了不必要的库

**解决方案**：
```bash
# 使用--exclude-module排除不需要的模块
pyinstaller --exclude-module matplotlib --exclude-module numpy label_gui_qt.py
```

### 问题4：杀毒软件误报
**原因**：PyInstaller打包的程序可能被误判

**解决方案**：
1. 添加到杀毒软件白名单
2. 使用代码签名（需要证书）
3. 使用 `--noupx` 参数（不压缩）

---

## 🔍 测试打包结果

### 1. 查找生成的EXE
```bash
# EXE文件位置
cd dist
dir
```

### 2. 测试运行
```bash
# 直接双击运行，或命令行运行
.\标签打印工具.exe
```

### 3. 检查功能
- ✅ 窗口图标是否正确显示
- ✅ 选择图片功能是否正常
- ✅ 生成PDF功能是否正常
- ✅ 打印功能是否正常
- ✅ 语言切换是否正常

---

## 🎨 高级配置

### 1. 添加版本信息
创建 `version.txt` 文件：
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'标签打印工具'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'LabelPrinter'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'标签打印工具.exe'),
        StringStruct(u'ProductName', u'标签打印工具'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

打包时使用：
```bash
pyinstaller --version-file=version.txt label_gui_qt.py
```

### 2. 优化启动速度
```bash
# 使用UPX压缩（需要先下载UPX）
pyinstaller --upx-dir=C:\upx label_gui_qt.py
```

### 3. 调试模式
```bash
# 保留控制台输出，方便调试
pyinstaller --onefile --console label_gui_qt.py
```

---

## 📊 打包流程图

```
开始
  ↓
安装PyInstaller
  ↓
准备资源文件（图标等）
  ↓
选择打包方式
  ├─→ 命令行打包
  └─→ Spec文件打包（推荐）
  ↓
执行打包命令
  ↓
检查dist文件夹
  ↓
测试EXE程序
  ↓
完成
```

---

## 💡 最佳实践建议

### 1. 打包前检查清单
- [ ] 所有依赖库已安装
- [ ] 图标文件已准备（.ico格式）
- [ ] 代码已测试无误
- [ ] 资源文件路径正确

### 2. 推荐的打包流程
```bash
# 1. 清理旧文件
rmdir /s /q build dist
del *.spec

# 2. 生成spec文件
pyi-makespec --onefile --windowed --icon=label.ico --name=标签打印工具 label_gui_qt.py

# 3. 编辑spec文件（添加资源文件）

# 4. 使用spec文件打包
pyinstaller label_printer.spec

# 5. 测试
cd dist
.\标签打印工具.exe
```

### 3. 版本管理
建议为每次打包创建版本标记：
```bash
# 重命名输出文件
ren "标签打印工具.exe" "标签打印工具_v1.0.0.exe"
```

---

## 🔗 相关资源

- [PyInstaller官方文档](https://pyinstaller.org/)
- [PyQt6文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Python打包指南](https://packaging.python.org/)

---

## 📞 常见问题FAQ

**Q: 打包后的EXE文件很大怎么办？**
A: 可以使用 `--exclude-module` 排除不需要的模块，或使用虚拟环境只安装必要的包。

**Q: 如何让程序在没有Python环境的电脑上运行？**
A: 使用 `--onefile` 参数打包成单文件，包含所有依赖。

**Q: 打包后程序启动很慢？**
A: 这是正常现象，因为需要解压临时文件。可以考虑使用 `--onedir` 模式。

**Q: 如何添加管理员权限？**
A: 需要创建manifest文件并在spec中引用，或使用第三方工具如mt.exe。

---

**最后更新**: 2024年
**适用版本**: Python 3.8+, PyInstaller 5.0+