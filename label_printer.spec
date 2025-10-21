# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 优化配置文件
# 用于创建启动更快的单文件可执行程序

block_cipher = None

a = Analysis(
    ['label_gui_qt.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('label.ico', '.'),  # 包含图标文件
        ('label.png', '.'),  # 包含PNG图标作为备用
    ],
    hiddenimports=[
        'PIL._tkinter_finder',  # PIL 需要
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'tkinter',           # 不使用 tkinter
        'matplotlib',        # 不使用 matplotlib
        'numpy',             # 不使用 numpy
        'pandas',            # 不使用 pandas
        'scipy',             # 不使用 scipy
        'IPython',           # 不使用 IPython
        'notebook',          # 不使用 Jupyter
        'pytest',            # 不需要测试框架
        'setuptools',        # 不需要安装工具
        'distutils',         # 不需要分发工具
        '_pytest',           # 不需要测试
        'test',              # 不需要测试
        'tests',             # 不需要测试
        'unittest',          # 不需要单元测试
        'xml.etree',         # 如果不需要 XML 处理
        'pydoc',             # 不需要文档
        'doctest',           # 不需要文档测试
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='标签打印工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 启用 UPX 压缩（如果已安装）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='label.ico',  # 设置EXE图标
)