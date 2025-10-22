# 将标签打印工具改造为局域网 Web 服务的建议

本指南总结了将现有的 PyQt6 桌面标签排版工具迁移为可在 Windows Server 上运行、供局域网内浏览器访问的 Web 服务时需要考虑的主要技术点与工作量评估。

## 1. 改造目标

- **部署位置**: Windows Server（建议 Windows Server 2019/2022）。
- **访问方式**: 局域网内用户通过浏览器访问（PC/平板均可）。
- **功能保持**: 保留现有的图片排版、参数设置、PDF/PNG 生成与打印能力。
- **多用户并发**: 支持多人同时使用，互不干扰。
- **易维护**: 服务可后台运行并开机自启，日志易于排查。

## 2. 总体架构建议

```text
┌──────────────────────────────────────────┐
│             Browser (LAN users)           │
│  React/Vue/静态页面 + REST API 调用         │
└──────────────────────────────────────────┘
               │ HTTPS/HTTP
┌──────────────────────────────────────────┐
│        Backend Service (Python)          │
│  FastAPI/Flask + Uvicorn/Gunicorn        │
│                                          │
│  ◇ 业务逻辑服务层                         │
│     - 参数验证 & 任务编排                 │
│     - PDF/PNG 生成（复用原有 Pillow 等库）│
│     - 打印队列管理（可选）                │
│  ◇ 存储层                                 │
│     - 本地文件系统 / SMB 共享             │
│     - SQLite/PostgreSQL 记录任务          │
└──────────────────────────────────────────┘
               │ 本地调用
┌──────────────────────────────────────────┐
│        Windows 打印子系统 (可选)          │
│   - 直接调度默认打印机或网络打印机        │
└──────────────────────────────────────────┘
```

- **前端**: 可先使用简单的基于表单的页面，后续视需求改成单页应用。
- **后端**: 推荐使用 FastAPI，既有类型提示又便于生成文档；Flask 亦可。
- **任务执行**: 生成 PDF/PNG 的耗时任务可放入队列（如 RQ/Celery），或采用同步处理 + 前端轮询的方式。
- **文件存储**: 利用服务器磁盘或共享文件夹，提供下载链接与历史记录。

## 3. 核心改造步骤

1. **梳理并抽取业务逻辑**
   - 将 `label_gui_qt.py` 中与 GUI 强耦合的部分（信号槽、窗口更新）与核心排版逻辑解耦。
   - 抽象出独立的 Python 模块，例如 `services/layout_service.py`，负责图片排版、PDF/PNG 生成、设置持久化。

2. **构建 Web API 层**
   - 设计 REST 接口，例如：
     - `POST /api/layouts/preview`：上传图片和参数，返回预览 PNG / PDF URL。
     - `POST /api/layouts/export`：返回最终 PDF 下载链接。
     - `POST /api/layouts/print`：将生成结果送入打印队列。
     - `GET /api/layouts/history`：分页获取历史任务记录。
   - 处理文件上传（FastAPI 的 `UploadFile`）和临时文件保存。

3. **实现前端界面**
   - 初始版本可用简洁的模板引擎（Jinja2）+ Bootstrap，实现与桌面端类似的表单。
   - 需要实时预览时，可通过轮询/轮询+WebSocket 获取生成结果，或直接在新窗口打开 PDF。

4. **任务与打印调度**
   - 若打印机挂在服务器上，可使用 `win32print` 或 `Print Spooler` 进行后台打印。
   - 为避免阻塞，建议使用任务队列（如 `RQ` + Redis）或后台线程池。
   - 对每个任务保存状态（排队、处理中、完成、失败），前端轮询展示。

5. **权限与安全**
   - 局域网环境下至少提供基于账号/令牌的访问控制，防止误用。
   - 使用 HTTPS（可自签或内网 CA）、限制访问网段。

6. **部署与运维**
   - 使用 `uvicorn`/`hypercorn` 作为应用服务器，IIS 或 Nginx 作为反向代理。
   - 设置 Windows 服务（如 NSSM/WinSW）将 Python 应用常驻运行。
   - 配置日志（结构化日志 + 日志轮转）与健康检查脚本。

## 4. 与桌面版共享代码的方式

- 将核心算法与文件生成流程封装为独立模块，桌面版与服务端均可引用。
- 通过环境变量或配置文件区分运行模式（GUI/Web）。
- 公共模块保持无 GUI 依赖，只处理纯逻辑与 I/O。

## 5. 工作量与风险评估

| 工作项 | 预估工作量（单人） | 说明 |
| ------ | ------------------ | ---- |
| 业务逻辑抽取与模块化 | 3-5 天 | 梳理现有代码、补充单元测试 |
| Web API 开发 | 4-6 天 | 包含参数校验、任务管理、文件存储 |
| 前端页面实现 | 3-5 天 | 初始版本使用模板引擎 + JS |
| 打印队列与后台处理 | 3-4 天 | 根据打印方案复杂度有所浮动 |
| 部署与自动化脚本 | 2-3 天 | 包含 Windows 服务配置、反向代理 |
| 安全加固 & 文档 | 1-2 天 | 权限、HTTPS、用户指南 |
| **总计** | **约 80-120 人时** | 取决于团队经验与功能深度 |

> 若只实现“生成 PDF/PNG 并可下载”而不包含在线打印、权限、自启动等扩展功能，工作量可压缩至 40-60 人时。

## 6. 增量迭代建议

1. **第一阶段**: 分离业务逻辑、提供最小化 REST API + 简单前端，支持上传、生成、下载。
2. **第二阶段**: 加入任务历史、权限控制、打印功能。
3. **第三阶段**: 优化 UI/UX、增加批量任务、提供多语言界面、性能监控。

## 7. 其他可选方案

- **远程桌面/应用虚拟化**: 如果仅需远程访问，可在 Windows Server 上运行现有桌面程序，使用 RDP 或 RemoteApp 暴露给用户。改造成本低，但体验不如原生 Web。
- **Electron/Chromium 包装**: 构建局域网可访问的 Chromium 前端，通过自定义协议访问本地 API。
- **容器化**: 若后期需要更灵活的部署，可将服务容器化，使用 Kubernetes/Windows 容器编排。

---

**Summary (English)**

- Extract the core layout logic from the PyQt GUI and expose it via a Python web framework such as FastAPI.
- Build REST endpoints for upload, preview generation, export, and optional printing queue management.
- Implement a lightweight HTML/JS frontend or SPA that mirrors the desktop workflow.
- Host the service on Windows Server with Uvicorn behind IIS/Nginx, run it as a Windows Service, and secure it with HTTPS and basic auth/token.
- Estimated effort: ~80-120 person-hours for a production-ready solution with multi-user support; a lightweight MVP without printing/auth can be delivered in ~40-60 person-hours.
