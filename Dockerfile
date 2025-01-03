# 使用官方Python镜像作为基础镜像
FROM python:3.12.1-alpine

# 设置工作目录
WORKDIR /usr/src/app

# 指定copy agentscope与src所有的文件
COPY agentscope/ /usr/src/app/agentscope/
COPY src/ /usr/src/app/src/
COPY start.sh /usr/src/app/start.sh

RUN pip install --no-cache-dir --default-timeout=100 -r /usr/src/app/agentscope/docs/sphinx_doc/requirements.txt || \
    (echo "First attempt failed, retrying..." && pip install --no-cache-dir --default-timeout=100 -r /usr/src/app/agentscope/docs/sphinx_doc/requirements.txt)
# 安装Python依赖包
RUN pip install --no-cache-dir --default-timeout=100 -r /usr/src/app/src/spider/code/requirements.txt || \
    (echo "First attempt failed, retrying..." && pip install --no-cache-dir --default-timeout=100 -r /usr/src/app/src/spider/code/requirements.txt)

# 复制启动脚本并设置为可执行
RUN chmod +x /usr/src/app/start.sh

# 设置环境变量，避免在运行时输入
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 告诉Docker容器启动时应该运行的命令
CMD ["/usr/src/app/start.sh"]