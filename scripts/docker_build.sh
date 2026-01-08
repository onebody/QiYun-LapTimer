#!/usr/bin/env bash
set -euo pipefail
IMAGE=platformio/platformio-core:latest
WORKDIR="$(pwd)"
docker pull "$IMAGE"
docker run --rm -v "$WORKDIR":/workspace -w /workspace "$IMAGE" bash -lc "\
  pio pkg update && \
  pio run -e QiYun-Laptimer && \
  pio run -e QiYun-Laptimer -t buildfs && \
  mkdir -p dist && \
  cp .pio/build/QiYun-Laptimer/firmware.bin dist/ && \
  cp .pio/build/QiYun-Laptimer/littlefs.bin dist/ && \
  cp .pio/build/QiYun-Laptimer/partitions.bin dist/ && \
  cp .pio/build/QiYun-Laptimer/bootloader.bin dist/ && \
  sha256sum dist/* > dist/checksums.txt \
"
echo "构建完成，产物位于 ./dist"
