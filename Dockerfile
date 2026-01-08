FROM platformio/platformio-core:latest
WORKDIR /workspace
COPY . /workspace
RUN pio pkg update
RUN pio run -e QiYun-Laptimer && pio run -e QiYun-Laptimer -t buildfs
RUN mkdir -p dist && \
    cp .pio/build/QiYun-Laptimer/firmware.bin dist/ && \
    cp .pio/build/QiYun-Laptimer/littlefs.bin dist/ && \
    cp .pio/build/QiYun-Laptimer/partitions.bin dist/ && \
    cp .pio/build/QiYun-Laptimer/bootloader.bin dist/ && \
    sha256sum dist/* > dist/checksums.txt
