![QiYun-LapTimer](assets/wq.png)![Logo](assets/logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 骑云 无人机竞速计时系统

**简单便捷的 FPV 单节点和多节点赛事计时解决方案**

如果你喜欢这个项目，可以通过为代码库做贡献、测试并提供反馈、分享新想法以及帮助传播下它！

[![Donate to PhobosLT](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://paypal.me/phoboslt)

# 关于

QiYun-LapTimer 是基于[PhobosLT](https://github.com/phobos-/PhobosLT)项目的基础修改、迭代开发而来的，是一款为 5.8GHz FPV 飞手设计的简单却强大的圈速计时解决方案！

### 特点

具有以下特点:

- 5.8GHz 模拟、HDZero、Walksnail 系统的单节点和多节点计时。
- 语音播报，可选择包含飞行员姓名。
- 实时 RSSI 读数和校准——即使在 16 平方米或 200 平方英尺的小空间内也能进行计时。
- 连续 2 圈和连续 3 圈的时间，以及可选的实时读数（专为[RaceGOW](https://www.racegow.com/)开发）。
- 可查看的圈速历史。
- 能够设置最小可测量圈速，以避免误报。
- 可配置的低压警报。
- 尺寸小巧，易于搭建，随意组合使用。

# 如何构建

### 硬件

需要的材料:

- 一块 ESP32 开发板，最好带有 USB 接口。该代码库可即插即用 LilyGo T-ENERGY，该板内置 1s 18650 锂离子电池插槽和电压感应电路。支持的开发板：
  - LilyGo T-ENERGY - 推荐.
  - ESP32-DevKit - 功能简单但价格便宜.
- 一个带有 [SPI](https://sheaivey.github.io/rx5808-pro-diversity/docs/rx5808-spi-mod.html) 的 RX5808 模块。
- 任何类型的电池、充电宝等.
- （可选）任何颜色的 LED（+一个匹配的电阻以管理电流）.
- （可选）一个 有源蜂鸣器。

RX5808 与 ESP32 针脚对应表:
| ESP32 PIN | RX5880 |
| :------------- |:-------------|
| 33 | RSSI |
| GND | GND |
| 19 | CH1 |
| 22 | CH2 |
| 23 | CH3 |
| 3V3 | +5V |

可选但推荐的 LED、蜂鸣器和电池电压输入引脚排列:
| ESP32 PIN | Peripheral |
| :------------- |:-------------|
| 21 | LED (+)正极 |
| 27 | 蜂鸣器 (+)正极 |
| 35 | VBAT 输入最大 3.3 伏 |

你可以在下方找到外设的连接图。**对于 T-Energy 和 T-Cell，你只需要连接 RX5808 和一个蜂鸣器即可**

![Connection](assets/connection_diagram.png)

### 固件

Currently building the firmware happens via Visual Studio Code. The toolchain setup is exactly the same as for ExpressLRS, so if you already have an ExpressLRS toolchain set up and running, you should be good. The requirements to build the firmware are as follows:

- Visual Studio Code.
- PlatformIO.
- Git.
