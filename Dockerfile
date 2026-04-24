# --- 第一阶段：构建依赖 ---
FROM python:3.10-slim as builder

WORKDIR /app

# 安装构建工具（如果某些 SDK 需要编译）
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- 第二阶段：运行环境 ---
FROM python:3.13

WORKDIR /app

# 从 builder 阶段拷贝安装好的包
COPY --from=builder /root/.local /root/.local
COPY . .

# 确保环境变量包含用户安装的包路径
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 启动命令（Uvicorn 模式）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]