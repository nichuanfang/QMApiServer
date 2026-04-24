# QQ Music API Server 🚀

这是一个基于 [L-1124/QQMusicApi](https://github.com/L-1124/QQMusicApi) 开发的高性能异步 HTTP 后端服务。

本项目采用 **FastAPI** 框架，结合基于 Rust 的 **Granian** 运行环境，旨在为音乐搜索、播放链接获取、歌词解析等提供极致的并发处理能力。

---

## ✨ 核心特性

- **🚀 顶尖性能**: 使用 Rust 驱动的 [Granian](https://github.com/emmett-framework/granian) 作为 ASGI 运行环境，性能优于 Uvicorn。
- **⚡ 全量异步**: 深度适配 `QQMusicApi` 的异步接口，确保 I/O 操作无阻塞。
- **🛡️ 生产就绪**: 提供多阶段构建的 Dockerfile，镜像体积小，启动速度快。
- **🧩 现代化生命周期**: 使用 FastAPI 最新 `Lifespan` 机制管理 API 实例。
- **📋 自动文档**: 内置 Swagger UI (`/docs`) 和 ReDoc (`/redoc`) 接口文档。

---

## 🛠️ 技术栈

- **Web 框架**: FastAPI (v0.110+)
- **API 驱动**: [QQMusicApi](https://github.com/L-1124/QQMusicApi)
- **ASGI 服务器**: Granian (Rust-based)
- **序列化**: Pydantic V2
- **包管理**: uv (推荐) 或 pip