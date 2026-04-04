# 使用官方Python基础镜像 (建议3.9或3.10，兼容性好)
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量 (防止Python缓冲输出)
ENV PYTHONUNBUFFERED=1

# 复制依赖文件 (利用Docker缓存机制，提高构建速度)
COPY ./app/code/requirements.txt /app/requirements.txt

# 在镜像构建阶段安装依赖 (这是为了满足"断网运行"要求)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制代码
COPY ./app /app

# 赋予执行权限
RUN chmod +x *.sh

# 容器启动时的默认命令 (通常不需要，由 docker-compose 控制)
CMD ["/bin/bash"]