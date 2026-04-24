# 第一阶段：构建环境
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# 设置环境变量，防止 Python 产生 .pyc 文件及缓冲输出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安装构建工具（如果某些库需要 C 编译）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装依赖到本地用户目录
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 第二阶段：运行环境
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# 从构建阶段拷贝安装好的库
COPY --from=builder /root/.local /root/.local
COPY . .

# 更新 PATH 以便找到安装的二进制文件
ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 使用 Granian 启动（Rust 驱动，高性能）
# --interface asgi: 指定 FastAPI 接口类型
# --threads: 线程数，适合 I/O 密集型 API
# --opt: 启用优化模式
CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "--threads", "4", "--opt", "main:app"]