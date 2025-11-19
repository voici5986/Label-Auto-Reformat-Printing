# Changelog

所有项目的重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [Unreleased]

### 计划中
- 待定功能

---

## [1.2.1] - 2025-11-19

### 新增 (Added)
- GroupBox 边框，提升界面层次感
- 预览区域渐变背景和加粗边框
- 专业的加载动画组件（旋转指示器 + 半透明遮罩）
- 自动化 GitHub Actions 打包发布流程

### 改进 (Changed)
- UI 常量集中管理到 `AppConstants` 类
- 优化窗口缩放性能（resize 防抖）
- 英文文件名（`Label-Auto-Reformat-Printing.exe`）以支持多语言系统

### 修复 (Fixed)
- 配置参数验证，防止无效配置
- 输入参数验证，提升程序健壮性
- 临时文件清理机制优化
- 提取重复的 PDF 生成代码

### 技术改进 (Technical)
- 添加 `requirements.txt` 依赖管理
- 添加 `__version__.py` 版本信息管理
- 创建 `LoadingOverlay` 加载动画组件
- 更新项目文档（README.md、打包优化方案.md）

---

## [1.0.0] - 2024-XX-XX

### 新增 (Added)
- 首次发布
- Material Design 风格界面
- 支持中文/泰语双语切换
- PDF 预览和生成功能
- 参数自动保存
- 横向/竖向 A4 纸张支持
- 批量标签排版功能

---

[Unreleased]: https://github.com/你的用户名/你的仓库名/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/你的用户名/你的仓库名/compare/v1.0.0...v1.2.1
[1.0.0]: https://github.com/你的用户名/你的仓库名/releases/tag/v1.0.0
