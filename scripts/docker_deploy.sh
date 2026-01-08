#!/usr/bin/env bash
set -euo pipefail
# 使用 Dockerfile 构建产物镜像并提取 dist，然后以容器化方式通过 OTA 上传到设备
IMG=qiyun-laptimer-builder:latest
WORKDIR="$(pwd)"
ESP32_HOST="${ESP32_HOST:-33.0.0.1}"
echo "构建镜像 $IMG"
docker build -t "$IMG" .
CID="$(docker create "$IMG")"
trap 'docker rm -f "$CID" >/dev/null 2>&1 || true' EXIT
mkdir -p dist
docker cp "$CID":/workspace/dist "$WORKDIR"/
echo "产物已提取至 ./dist"
echo "开始OTA部署到 http://$ESP32_HOST/update"
docker run --rm -v "$WORKDIR/dist":/dist curlimages/curl:8.6.0 \
  -sS -o - -w "\nHTTP %{http_code}\n" \
  -X POST -F "file=@/dist/firmware.bin" "http://${ESP32_HOST}/update"
echo "完成"
