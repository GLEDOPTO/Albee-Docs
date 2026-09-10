# An MCP-based Chatbot

## Introduction

This project is a derivative development based on version 2.0.5 of the Xiaozhi AI chatbot.

Gledopto Robot Project URL: TODO

Xiaozhi Project URL: [XiaoZhi](https://github.com/78/xiaozhi-esp32)

As a voice interaction entry, the XiaoZhi AI chatbot leverages the AI capabilities of large models like Qwen / DeepSeek, and achieves multi-terminal control via the MCP protocol.

<img src="../assets/img/mcp-based-graph.jpg" alt="Control everything via MCP" width="320">

### Features Implemented

**Voice & Conversation**

- Wi-Fi connectivity, with two communication protocols ([WebSocket](docs/websocket.md) or MQTT+UDP)
- Voice interaction based on streaming ASR + LLM + TTS architecture, OPUS audio codec
- Wake by voice ("Hi Albee") or by short-pressing the function button
- Real-time barge-in: no need to wait for the reply to finish — just speak to interrupt (double-click the function key to toggle)
- Supports 38 languages
- Speaker recognition, identifies the current speaker [3D Speaker](https://github.com/modelscope/3D-Speaker)
- Role customization via the xiaozhi.me console: personality roles, voice/timbre, LLM selection (Qwen3 / DeepSeek / Doubao, etc.), short-term and long-term memory
- Voiceprint recognition — Albee can recognize and remember who is talking

**Motion & Interaction**

- Bipedal walking driven by four digital servos: walk forward/backward, turn left/right, with adjustable step count and arm-swing amplitude
- Desktop anti-fall protection: four IR distance sensors on the feet detect table edges and automatically brake or turn away
- 6-axis IMU emotional reactions — shake it and it gets angry; pick it up and it happily swings its feet

**Display & Emotion**

- 1.54-inch LCD with 21 emoji expressions that follow the conversation mood
- WS2811 ×8 RGB LED ring indicating device state (connecting / listening / speaking / upgrading, etc.)

**Light Control Hub**

- Simultaneously manages 2.4G RF light groups and WLED smart lights by voice
- Built-in web console for RF light pairing and WLED device scanning / room assignment
- Per-light-group state (on/off, brightness, color) stored independently and retained after power loss

**Smart Home, MCP & Tools**

- Device-side MCP for device control (Speaker, LED, Servo, GPIO, etc.)
- Cloud-side MCP with dozens of services (weather, jokes, music, news, knowledge base, etc.) — up to 32 connected at the same time
- Home Assistant integration via MCP plugins
- Voice alarm & reminders: up to 5 active reminders, triggered by ring + emoji + on-screen text (any key stops it)

**Power Management**

- Battery level monitoring, ~10% low-battery warning, automatic power-off protection, and low-battery gait speed limiting
- Power-saving sleep mode
- Type-C 5V charging with status LED (red = charging, green = full); wireless charging supported

**Customization**

- Customizable emojis, and chat backgrounds with online web-based editing ([Custom Assets Generator](https://github.com/78/xiaozhi-assets-generator))

## Hardware

* ESP32-S3 SoC
* Function button + Touch button
* 2.4G RF Module
* Four Digital Servo
* 1.54-inch Screen
* ECM microphone
* 4Ω3W Speaker
* 6-Axis IMU
* IR Proximity Sensor
* Audio Decoder
* WS2811 ×8 RGB LED ring
* Wireless charging
* Type-C port

## Software

### Firmware Flashing

Please See：[Firmware Flashing Guide](./docs/firmware-flashing-guide.md)

### Development Environment

- Cursor or VSCode
- Install ESP-IDF plugin, select SDK version 5.4 or above
- Linux is better than Windows for faster compilation and fewer driver issues
- This project uses Google C++ code style, please ensure compliance when submitting code

### Developer Documentation

- [MCP Protocol IoT Control Usage](./docs/mcp-usage.md) - Learn how to control IoT devices via MCP protocol
- [MCP Protocol Interaction Flow](docs/mcp-protocol.md) - Device-side MCP protocol implementation
- [MQTT + UDP Hybrid Communication Protocol Document](docs/mqtt-udp.md)
- [A detailed WebSocket communication protocol document](docs/websocket.md)

## Large Model Configuration

If you already have a XiaoZhi AI chatbot device and have connected to the official server, you can log in to the [xiaozhi.me](https://xiaozhi.me) console for configuration.

TODO

## Related Open Source Projects

For server deployment on personal computers, refer to the following open-source projects:

- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) Python server
- [joey-zhou/xiaozhi-esp32-server-java](https://github.com/joey-zhou/xiaozhi-esp32-server-java) Java server
- [AnimeAIChat/xiaozhi-server-go](https://github.com/AnimeAIChat/xiaozhi-server-go) Golang server

Other client projects using the XiaoZhi communication protocol:

- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) Python client
- [TOM88812/xiaozhi-android-client](https://github.com/TOM88812/xiaozhi-android-client) Android client

Custom Assets Tools:

- [78/xiaozhi-assets-generator](https://github.com/78/xiaozhi-assets-generator) Custom Assets Generator (Wake words, fonts, emojis, backgrounds)

# Albee Encyclopaedia

Please See:  [Albee Encyclopaedia](./albee-encyclopaedia.md)

## Product Manual

Full product manual (PDF): [Albee Robot Manual.pdf](../docs/Albee%20Robot%20Manual.pdf)

## About the Project

This is an open-source ESP32 project, released under the MIT license, allowing anyone to use it for free, including for commercial purposes.

We hope this project helps everyone understand AI hardware development and apply rapidly evolving large language models to real hardware devices.

TODO: 如果你有任何想法或建议，请随时提出 Issues 或加入 [Discord](https://discord.gg/C759fGMBcZ) 或 QQ 群：1011329060
---

**Last modified:** 2026-09-10
