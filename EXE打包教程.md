# 标签打印工具 - EXE打包完整教程

## 📋 目录
1. [环境准备](#环境准备)
2. [安装依赖](#安装依赖)
3. [打包步骤](#打包步骤)
4. [验证测试](#验证测试)
5. [常见问题](#常见问题)

---

## 🔧 环境准备

### 1. 确认Python环境
打开命令提示符(CMD)或PowerShell,输入:
```bash
python --version
```
应该显示 Python 3.8 或更高版本。

### 2. 确认项目文件
确保你的项目文件夹包含以下文件:
```
label/
├── label_gui_qt.py      # 主程序文件
├── label.ico            # 图标文件(ICO格式)
├── label.png            # 图标文件(PNG格式,备用)
└── settings.json        # 配置文件(运行后自动生成)
```

---

## 📦 安装依赖

### 1. 安装PyInstaller
在项目文件夹中打开命令提示符,输入:
```bash
pip install pyinstaller
```

### 2. 确认已安装的其他依赖
```bash
pip install PyQt6 Pillow PyMuPDF reportlab
```

如果已经安装过,会显示"Requirement already satisfied"。

---

## 🚀 打包步骤

### 方法一: 使用命令行打包(推荐)

#### 1. 打开命令提示符
在项目文件夹中,按住 `Shift` 键,右键点击空白处,选择"在此处打开PowerShell窗口"或"在此处打开命令窗口"。

#### 2. 执行打包命令
复制以下命令并粘贴到命令行中,按回车执行:

```bash
pyinstaller --name="标签打印工具" --windowed --onefile --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py
```

#### 3. 等待打包完成
打包过程需要1-3分钟,你会看到类似这样的输出:
```
Building EXE from EXE-00.toc
Building EXE from EXE-00.toc completed successfully.
```

#### 4. 查找生成的EXE文件
打包完成后,在项目文件夹中会出现:
- `dist/` 文件夹 - **这里包含最终的EXE文件**
- `build/` 文件夹 - 临时构建文件
- `标签打印工具.spec` 文件 - 打包配置文件

**你的EXE文件位置**: `dist/标签打印工具.exe`

---

### 方法二: 使用spec文件打包

如果你已经有 `标签打印工具.spec` 文件,可以直接使用:

```bash
pyinstaller 标签打印工具.spec
```

这会使用之前保存的配置重新打包。

---

## ✅ 验证测试

### 1. 测试EXE文件
1. 进入 `dist` 文件夹
2. 双击 `标签打印工具.exe`
3. 程序应该正常启动,显示启动画面后进入主界面

### 2. 测试功能
- ✅ 选择图片文件
- ✅ 调整参数(行数、列数、边距、间距)
- ✅ 切换语言(中文/泰语)
- ✅ 生成预览
- ✅ 生成PDF
- ✅ 生成并打印

### 3. 测试设置保存
1. 关闭程序
2. 重新打开
3. 确认上次的参数设置被保留

---

## 🎯 打包命令详解

让我们理解每个参数的作用:

```bash
pyinstaller \
  --name="标签打印工具" \      # EXE文件名称
  --windowed \                  # 无控制台窗口(GUI程序)
  --onefile \                   # 打包成单个EXE文件
  --icon=label.ico \            # 设置程序图标
  --add-data="label.ico;." \    # 包含图标文件
  --add-data="label.png;." \    # 包含PNG图标(备用)
  label_gui_qt.py               # 主程序文件
```

### 参数说明:

| 参数 | 说明 | 可选/必需 |
|------|------|----------|
| `--name` | 指定生成的EXE文件名 | 可选 |
| `--windowed` | 隐藏控制台窗口(GUI程序必需) | 必需 |
| `--onefile` | 打包成单个EXE文件 | 推荐 |
| `--icon` | 设置程序图标 | 可选 |
| `--add-data` | 包含额外的数据文件 | 按需 |

---

## 🔍 常见问题

### Q1: 打包后EXE文件很大(50MB+)
**答**: 这是正常的。PyInstaller会打包所有依赖库,包括:
- PyQt6 (GUI框架)
- PyMuPDF (PDF处理)
- Pillow (图片处理)
- ReportLab (PDF生成)

### Q2: 双击EXE后没有反应
**答**: 可能的原因:
1. 杀毒软件拦截 - 添加到白名单
2. 缺少依赖 - 重新打包
3. 文件损坏 - 删除 `build` 和 `dist` 文件夹后重新打包

### Q3: 程序启动很慢
**答**: 第一次启动会慢一些(5-10秒),因为需要解压临时文件。后续启动会快一些。

### Q4: 如何修改程序后重新打包?
**答**: 
1. 修改 `label_gui_qt.py` 文件
2. 删除 `build` 和 `dist` 文件夹
3. 重新执行打包命令

### Q5: 打包时出现"ModuleNotFoundError"
**答**: 缺少依赖库,执行:
```bash
pip install PyQt6 Pillow PyMuPDF reportlab
```

### Q6: 如何减小EXE文件大小?
**答**: 可以使用 `--onedir` 代替 `--onefile`:
```bash
pyinstaller --name="标签打印工具" --windowed --onedir --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py
```
这会生成一个文件夹,包含EXE和依赖文件,总大小相同但启动更快。

### Q7: 如何在其他电脑上运行?
**答**: 
1. 复制整个 `dist` 文件夹到目标电脑
2. 双击 `标签打印工具.exe` 即可运行
3. **不需要**安装Python或任何依赖

### Q8: 打包后图标不显示
**答**: 
1. 确认 `label.ico` 文件存在
2. 确认使用了 `--icon=label.ico` 参数
3. 确认使用了 `--add-data="label.ico;."` 参数

---

## 📝 快速参考

### 完整打包流程(一键复制)

```bash
# 1. 安装PyInstaller(首次需要)
pip install pyinstaller

# 2. 执行打包
pyinstaller --name="标签打印工具" --windowed --onefile --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py

# 3. 查找EXE文件
# 位置: dist/标签打印工具.exe
```

### 重新打包(修改代码后)

```bash
# 1. 删除旧文件
rmdir /s /q build dist
del 标签打印工具.spec

# 2. 重新打包
pyinstaller --name="标签打印工具" --windowed --onefile --icon=label.ico --add-data="label.ico;." --add-data="label.png;." label_gui_qt.py
```

---

## 🎉 完成!

现在你已经学会了如何打包Python程序为EXE文件。

**生成的文件位置**: `dist/标签打印工具.exe`

你可以:
- ✅ 直接运行这个EXE文件
- ✅ 复制到其他电脑使用(无需安装Python)
- ✅ 分享给其他用户

---

## 📚 进阶技巧

### 1. 自定义启动画面
修改 `label_gui_qt.py` 中的 `create_splash_screen()` 函数。

### 2. 添加版本信息
创建 `version.txt` 文件,在打包时使用 `--version-file` 参数。

### 3. 数字签名
使用 `signtool.exe` 为EXE添加数字签名,避免杀毒软件误报。

---

**祝你打包顺利! 🚀**