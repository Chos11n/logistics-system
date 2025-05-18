# ======== 构建阶段 ======== #
# 使用官方 Python 基础镜像
FROM python:3.11-slim-bullseye as builder

# 设置工作目录
WORKDIR /app

# 安装系统级依赖（根据物流系统需要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 创建虚拟环境（隔离依赖）
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 先复制依赖文件以利用缓存
COPY requirements.txt .

# 安装依赖（使用国内镜像加速）
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# ======== 运行阶段 ======== #
# 使用更安全的最小化镜像
FROM python:3.11-slim-bullseye

# 设置容器元数据
LABEL org.opencontainers.image.description="物流系统后端API服务"

# 创建非root用户
RUN useradd -m -u 1001 logistics
USER logistics
WORKDIR /home/logistics/app

# 从构建阶段复制虚拟环境
COPY --chown=logistics:logistics --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制应用代码（排除开发文件）
COPY --chown=logistics:logistics src/ ./src
COPY --chown=logistics:logistics config/ ./config

# 配置环境变量（可在docker-compose覆盖）
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV DB_HOST=database
ENV DB_PORT=5432

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# 暴露端口（与docker-compose对应）
EXPOSE 5000

# 使用Gunicorn运行（生产级WSGI服务器）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "src.app:create_app()"]