#!/bin/sh
# start.sh

# 确保所有Python脚本都使用了正确的解释器和路径
python /usr/src/app/src/spider/code/spider_api.py &
python /usr/src/app/src/spider/code/start_chat.py

# 保持脚本运行，以便Docker容器不退出
wait