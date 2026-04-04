FROM python:3.9-slim
WORKDIR /app

# 1. 安装依赖 (利用缓存层)
COPY ./app/code/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

# 2. 复制代码
COPY ./app /app

# 3. 赋予权限
RUN chmod +x *.sh

CMD ["/bin/bash"]