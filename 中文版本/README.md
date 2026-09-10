# 基于 MCP 的聊天机器人

## 简介

本项目是基于小智 AI 聊天机器人 2.0.5 版本的衍生开发。

格乐（Gledopto）机器人项目地址：TODO

小智项目地址：[XiaoZhi](https://github.com/78/xiaozhi-esp32)

小智 AI 聊天机器人作为语音交互入口，借助 Qwen / DeepSeek 等大模型的 AI 能力，通过 MCP 协议实现多端控制。

<img src="../assets/img/mcp-based-graph.jpg" alt="通过 MCP 控制一切" width="320">

### 已实现的功能

**语音与对话**

- Wi-Fi 联网，支持两种通信协议（[WebSocket](docs/websocket.md) 或 MQTT+UDP）
- 基于流式 ASR + LLM + TTS 架构的语音交互，OPUS 音频编解码
- 语音唤醒（"Hi Albee"）或短按功能键唤醒
- 实时打断：无需等回复播完，直接说话即可打断（双击功能键可开关）
- 支持 38 种语言
- 说话人识别，识别当前说话人 [3D Speaker](https://github.com/modelscope/3D-Speaker)
- 通过 xiaozhi.me 控制台自定义角色：人格角色、音色、大模型选择（Qwen3 / DeepSeek / 豆包等）、短期与长期记忆
- 声纹识别 —— Albee 能认出并记住谁在说话

**运动与交互**

- 四个数字舵机驱动的双足行走：前进/后退、左转/右转，步数与摆臂幅度可调
- 桌面防跌落保护：脚部四个红外测距传感器检测桌沿，自动刹车或避让
- 六轴 IMU 情绪反应 —— 摇晃它会生气，抱起来它会开心地晃脚

**显示与表情**

- 1.54 英寸 LCD，21 个表情随对话情绪变化
- WS2811 ×8 RGB 灯环指示设备状态（连接中 / 听取 / 播报 / 升级等）

**灯光控制中枢**

- 同时管理 2.4G RF 灯组与 WLED 智能灯，语音控制
- 内置 Web 控制台，用于 RF 灯配对、WLED 设备扫描与房间分组
- 各灯组状态（开关、亮度、颜色）独立存储，掉电不丢失

**智能家居、MCP 与工具**

- 设备端 MCP，用于设备控制（扬声器、LED、舵机、GPIO 等）
- 云端 MCP 数十种服务（天气、笑话、音乐、新闻、知识库等），最多同时接入 32 个
- 通过 MCP 插件接入 Home Assistant
- 语音闹钟与提醒：最多 5 个提醒同时生效，铃声 + 表情 + 屏幕文字触发（任意按键停止）

**电源管理**

- 电量监测，约 10% 低电量提醒、自动关机保护、低电量步态限速
- 省电休眠模式
- Type-C 5V 充电，带充电指示灯（红灯充电中、绿灯充满）；支持无线充电

**个性化定制**

- 表情、聊天背景可自定义，支持在线网页编辑（[自定义素材生成器](https://github.com/78/xiaozhi-assets-generator)）

## 硬件

* ESP32-S3 主控
* 功能按键 + 触摸按键
* 2.4G RF 模块
* 四个数字舵机
* 1.54 英寸屏幕
* ECM 麦克风
* 4Ω3W 喇叭
* 六轴 IMU
* 红外接近传感器
* 音频解码芯片
* WS2811 ×8 RGB 灯环
* 无线充电
* Type-C 接口

## 软件

### 固件烧录

请查看：[固件烧录指南](./docs/firmware-flashing-guide.md)

### 开发环境

- Cursor 或 VSCode
- 安装 ESP-IDF 插件，选择 5.4 及以上版本 SDK
- Linux 比 Windows 编译更快、驱动问题更少
- 本项目使用 Google C++ 代码风格，提交代码请确保遵守

### 开发者文档

- [MCP 协议 IoT 控制使用](./docs/mcp-usage.md) - 了解如何通过 MCP 协议控制 IoT 设备
- [MCP 协议交互流程](docs/mcp-protocol.md) - 设备端 MCP 协议实现
- [MQTT + UDP 混合通信协议文档](docs/mqtt-udp.md)
- [详细的 WebSocket 通信协议文档](docs/websocket.md)

## 大模型配置

如果你已有小智 AI 聊天机器人设备并连接了官方服务器，可登录 [xiaozhi.me](https://xiaozhi.me) 控制台进行配置。

TODO

## 相关开源项目

在个人电脑上部署服务器，可参考以下开源项目：

- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) Python 服务器
- [joey-zhou/xiaozhi-esp32-server-java](https://github.com/joey-zhou/xiaozhi-esp32-server-java) Java 服务器
- [AnimeAIChat/xiaozhi-server-go](https://github.com/AnimeAIChat/xiaozhi-server-go) Golang 服务器

其他使用小智通信协议的客户端项目：

- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) Python 客户端
- [TOM88812/xiaozhi-android-client](https://github.com/TOM88812/xiaozhi-android-client) Android 客户端

自定义素材工具：

- [78/xiaozhi-assets-generator](https://github.com/78/xiaozhi-assets-generator) 自定义素材生成器（唤醒词、字体、表情、背景）

# 更多文档

请查看：[更多关于 Albee 的资料](./albee-encyclopaedia.md)

## 关于本项目

这是一个开源的 ESP32 项目，采用 MIT 许可证发布，任何人都可以免费使用，包括用于商业用途。

我们希望这个项目能帮助大家了解 AI 硬件开发，将快速演进的大语言模型应用到真实的硬件设备上。

TODO: 如果你有任何想法或建议，请随时提出 Issues 或加入 [Discord](https://discord.gg/C759fGMBcZ) 或 QQ 群：1011329060

---

**文档最新修改时间：** 2026-09-10
