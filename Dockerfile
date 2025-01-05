# 使用官方Python镜像作为基础镜像
FROM python:3.12-alpine

# 设置环境变量以避免安装过程中的一些交互提示
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# 安装必要的构建依赖
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        linux-headers \
        python3-dev

# 设置工作目录
WORKDIR /usr/src/app

# 指定copy agentscope与src所有的文件
COPY agentscope/ /usr/src/app/agentscope/
COPY src/ /usr/src/app/src/
COPY start.sh /usr/src/app/start.sh

COPY agentscope/docs/sphinx_doc/requirements.txt /tmp/agentscope_requirements.txt
COPY src/spider/code/requirements.txt /tmp/spider_requirements.txt



RUN pip install -e /usr/src/app/agentscope --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/spider_requirements.txt

# 复制启动脚本并设置为可执行
RUN chmod +x /usr/src/app/start.sh

# 设置环境变量
ENV PYTHONPATH="/usr/src/app/" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


# 告诉Docker容器启动时应该运行的命令
CMD ["/usr/src/app/start.sh"]