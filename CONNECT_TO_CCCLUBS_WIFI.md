# 让ESP32设备连接ccclubs WiFi网络

## 已完成的操作

我已经修改了ESP32项目的默认WiFi配置，将SSID设置为"ccclubs"，密码设置为"88190338"。

修改的文件：`lib/CONFIG/config.cpp`
- 在`setDefaults()`函数中，将默认SSID从空字符串改为"ccclubs"
- 将默认密码从空字符串改为"88190338"

## 对于新设备/首次使用

1. 编译并上传修改后的固件到ESP32设备
2. 设备首次启动时，会自动尝试连接到"ccclubs" WiFi网络（密码：88190338）
3. 如果连接成功，设备LED会停止闪烁并保持熄灭状态
4. 如果连接失败，设备会创建自己的AP热点（名称类似"PhobosLT_XXXXXX"）

## 对于已有配置的现有设备

如果设备已经有保存的WiFi配置，需要以下步骤之一来使用新的ccclubs网络：

### 方法1：通过Web界面更新配置

1. 连接到设备的AP热点（名称类似"PhobosLT_XXXXXX"，密码：phoboslt）
2. 在浏览器中访问：http://20.0.0.1
3. 进入配置页面
4. 将SSID改为"ccclubs"，密码改为"88190338"
5. 保存配置
6. 设备会重启并尝试连接到新的WiFi网络

### 方法2：清除EEPROM恢复默认设置

1. 通过串口连接到设备（波特率：460800）
2. 在串口监视器中，设备启动时可能会显示配置信息
3. 要清除EEPROM，可以：
   - 重新编译并上传固件（某些情况下会触发配置重置）
   - 或者通过Web界面的"恢复默认设置"功能（如果可用）

### 方法3：重新刷写固件

1. 重新编译并上传修改后的固件
2. 在设备启动时，如果检测到配置版本不匹配，会自动恢复默认设置

## 验证连接

1. 设备成功连接到ccclubs网络后，可以通过路由器查看连接的设备
2. 设备会通过mDNS广播为"plt.local"，可以在浏览器中访问 http://plt.local
3. 或者查看设备获取的IP地址，直接访问该IP

## 故障排除

1. **设备无法连接到ccclubs网络**：
   - 确认ccclubs网络可用且密码正确
   - 检查设备与路由器的距离
   - 查看串口调试输出（波特率460800）获取详细错误信息

2. **设备始终创建AP热点**：
   - 检查配置中的SSID和密码是否正确
   - 尝试清除EEPROM恢复默认设置

3. **无法访问Web界面**：
   - 确认设备已成功连接到WiFi网络
   - 尝试通过IP地址访问而不是mDNS名称
   - 检查防火墙设置

## 代码修改详情

修改位置：`lib/CONFIG/config.cpp` 第154-156行

修改前：
```cpp
strlcpy(conf.ssid, "", sizeof(conf.ssid));
strlcpy(conf.password, "", sizeof(conf.password));
```

修改后：
```cpp
strlcpy(conf.ssid, "ccclubs", sizeof(conf.ssid));
strlcpy(conf.password, "88190338", sizeof(conf.password));
```

这个修改确保新设备或重置后的设备会自动尝试连接到指定的WiFi网络。
