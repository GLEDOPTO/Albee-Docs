# An MCP-based Chatbot

## Introduction

This project is a derivative development based on version 2.0.5 of the Xiaozhi AI chatbot.

Gledopto Robot Project URL: TODO

Xiaozhi Project URL: [XiaoZhi](https://github.com/78/xiaozhi-esp32)

As a voice interaction entry, the XiaoZhi AI chatbot leverages the AI capabilities of large models like Qwen / DeepSeek, and achieves multi-terminal control via the MCP protocol.

<img src="../assets/img/mcp-based-graph.jpg" alt="Control everything via MCP" width="320">

### Features Implemented

**Voice & Conversation**

- Wi-Fi connectivity, with two communication protocols ([WebSocket](docs/websocket.md) or [MQTT+UDP](docs/mqtt-udp.md))
- Voice interaction based on streaming ASR + LLM + TTS architecture, OPUS audio codec
- Wake by voice ("Hi Albee") or by short-pressing the function button
- Real-time barge-in: no need to wait for the reply to finish — just speak to interrupt (double-click the function key to toggle)
- Supports 38 languages
- Speaker recognition, identifies the current speaker [3D Speaker](https://github.com/modelscope/3D-Speaker)
- Role customization via the xiaozhi.me console: personality roles, voice/timbre, LLM selection (Qwen3 / DeepSeek / Doubao, etc.), memory mode (see the [XiaoZhi Console Configuration Guide](docs/xiaozhi-console.md))
- Voiceprint recognition — Albee can recognize and remember who is talking (configuration in the [console guide · Voiceprint Recognition](docs/xiaozhi-console.md#6-voiceprint-recognition))

**Motion & Interaction**

- Bipedal walking driven by four digital servos: walk forward/backward, turn left/right, with adjustable step count and arm-swing amplitude
- Desktop anti-fall protection: four IR distance sensors on the feet detect table edges and automatically brake or turn away
- 6-axis IMU emotional reactions — shake it and it gets angry; pick it up and it happily swings its feet

**Display & Emotion**

- 1.54-inch LCD with 21 emoji expressions that follow the conversation mood
- WS2811 ×8 RGB LED ring indicating device state (connecting / listening / speaking / upgrading, etc.)

**Light Control Hub**

- Simultaneously manages 2.4G RF light groups (compatible with all 2.4G RF LED strip controllers from GLEDOPTO) and WLED smart lights (WLED-series controllers) by voice
- Built-in web console for RF light pairing and WLED device scanning / grouping, up to 4 groups each
- Group names and on/off state stored independently in device NVS, retained after power loss
- See the [Lighting Control Guide](docs/lighting-control.md) for voice commands and the HTTP API reference

**Smart Home, MCP & Tools**

- Device-side MCP for device control (speaker, screen, robot motion, lights, power, GPIO, etc.) — full tool catalog in the [MCP Usage Guide](docs/mcp-usage.md)
- Cloud-side MCP with dozens of services (weather, jokes, music, news, knowledge base, etc.) — up to 32 connected at the same time; upload your own material as a [knowledge base](docs/knowledge-base.md) for the AI to consult
- Home Assistant integration via MCP plugins — see the [Home Assistant Integration Guide](docs/home-assistant.md)
- Voice alarms & reminders: one-time / daily / weekly / fixed-interval, up to 5 active at once; triggered by ring + emoji + on-screen text, stopped by key, touch, or voice (see the [Alarm & Reminder Guide](docs/alarm-reminder.md))

**Power Management**

- Battery level monitoring, ~10% low-battery warning, automatic power-off protection, and low-battery gait speed limiting
- Power-saving sleep mode
- Type-C 5V charging with status LED (red = charging, green = full); wireless charging supported

**Customization**

- Customizable emojis and chat backgrounds: change online via the console, or replace the firmware emoji assets and rebuild (see the [Emoji Change Guide](docs/expression-change-guide.md)); online editing also available with the [Custom Assets Generator](https://github.com/78/xiaozhi-assets-generator)

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

See the [Pin Mapping](docs/pin-mapping.md) document for the complete GPIO assignment.

## Software

### Firmware Flashing

Please See：[Firmware Flashing Guide](./docs/firmware-flashing-guide.md)

### Development Environment

- Cursor or VSCode
- Install the ESP-IDF plugin and use v5.4.3 (dependencies require >= 5.3; the current sdkconfig is based on 5.4.3)
- Linux is better than Windows for faster compilation and fewer driver issues
- This project uses Google C++ code style, please ensure compliance when submitting code
- For full environment setup, building, flashing, and release scripts, see the [Firmware Compilation Tutorial](docs/compilation-tutorial.md)

### Developer Documentation

- [MCP Protocol IoT Control Usage](./docs/mcp-usage.md) - Learn how to control IoT devices via MCP protocol (full tool catalog)
- [MCP Protocol Interaction Flow](docs/mcp-protocol.md) - Device-side MCP protocol implementation
- [MQTT + UDP Hybrid Communication Protocol Document](docs/mqtt-udp.md)
- [A detailed WebSocket communication protocol document](docs/websocket.md)
- [OTA API](docs/ota-api.md) - Device firmware over-the-air upgrade interface

## Large Model Configuration

If you already have a XiaoZhi AI chatbot device and have connected to the official server, you can log in to the [xiaozhi.me](https://xiaozhi.me) console for configuration.

- Language, voice/timbre, role introduction, model, and memory mode: see the [XiaoZhi Console Configuration Guide](docs/xiaozhi-console.md)
- To unlock more models (Qwen3 / DeepSeek full / Doubao / GLM): see [Developer Authentication](docs/developer-auth.md)
- **Restart the device** after completing all configuration for the changes to take effect

## Related Open Source Projects

For server deployment on personal computers, refer to the following open-source projects:

- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) Python server
- [joey-zhou/xiaozhi-esp32-server-java](https://github.com/joey-zhou/xiaozhi-esp32-server-java) Java server
- [AnimeAIChat/xiaozhi-server-go](https://github.com/AnimeAIChat/xiaozhi-server-go) Golang server

Other client projects using the XiaoZhi communication protocol:

- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) Python client
- [TOM88812/xiaozhi-android-client](https://github.com/TOM88812/xiaozhi-android-client) Android client

Custom Assets Tools:

- [78/xiaozhi-assets-generator](https://github.com/78/xiaozhi-assets-generator) Custom Assets Generator (fonts, emojis, backgrounds)

# Albee Encyclopaedia

Please See: [Albee Encyclopaedia](./albee-encyclopaedia.md) — the categorized index and reading paths for all documents; for everyday questions see the [FAQ](docs/faq.md).

## Product Manual

Full product manual (PDF): [Albee Robot Manual.pdf](../docs/Albee%20Robot%20Manual.pdf)

## About the Project

This is an open-source ESP32 project, released under the MIT license, allowing anyone to use it for free, including for commercial purposes.

We hope this project helps everyone understand AI hardware development and apply rapidly evolving large language models to real hardware devices.

---

**Last modified:** 2026-10-09
