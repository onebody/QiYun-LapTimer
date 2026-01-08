#!/usr/bin/env bash
set -e

IMAGE_NAME="qiyun-laptimer-web"
CONTAINER_NAME="qiyun-web-server"
PORT=8080

echo "正在构建 Web 镜像: $IMAGE_NAME"
docker build -f Dockerfile.web -t $IMAGE_NAME .

echo "清理旧容器..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "启动新容器..."
echo "访问地址: http://localhost:$PORT"
docker run -d --name $CONTAINER_NAME \
  -p $PORT:80 \
  $IMAGE_NAME

echo "部署完成！"
