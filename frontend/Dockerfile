# ======== 构建阶段 ======== #
# 使用官方 Node 镜像作为构建环境
FROM node:18-alpine as builder

# 设置工作目录（容器内路径）
WORKDIR /app

# 优先复制包管理文件以利用 Docker 缓存
COPY package.json pnpm-lock.yaml* ./

# 安装 pnpm（比 npm/yarn 更快的包管理器）
RUN npm install -g pnpm@8 && \
    pnpm install --frozen-lockfile

# 复制所有源代码
COPY . .

# 配置生产环境变量
ENV REACT_APP_API_HOST=http://backend:5000
ENV GENERATE_SOURCEMAP=false

# 执行构建（生成优化后的静态文件）
RUN pnpm build

# ======== 运行阶段 ======== #
# 使用更轻量的 Nginx 镜像提供服务
FROM nginx:1.25-alpine

# 删除默认配置
RUN rm -rf /etc/nginx/conf.d/default.conf

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d

# 从构建阶段复制产物到 Nginx 服务目录
COPY --from=builder /app/build /usr/share/nginx/html

# 暴露端口（与 docker-compose 映射端口一致）
EXPOSE 3000

# 启动 Nginx 并保持在前台运行（Docker 要求）
CMD ["nginx", "-g", "daemon off;"]  