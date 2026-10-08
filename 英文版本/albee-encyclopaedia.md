# Albee Encyclopaedia

> One-stop index of all Albee desktop robot documentation. Every entry below links to a full document — click to jump.
>
> Language: English | 中文版：[../中文版本/Albee百科全书.md](../中文版本/Albee百科全书.md)
>
> Project overview: [README.md](./README.md)

## Document Map

| Category | What it covers | Documents |
|---|---|---|
| [Getting Started](#1-getting-started) | Unbox → flash → first conversation | Firmware Flashing Guide |
| [Console & Account](#2-console--account) | xiaozhi.me console, developer auth, account issues, device fault feedback, knowledge base | 5 documents |
| [Feature Guides](#3-feature-guides) | Lighting control, alarms & reminders, emoji change, FAQ | 4 documents |
| [Firmware & Hardware](#4-firmware--hardware-development) | Compiling from source, pin mapping, OTA API | 3 documents |
| [Protocols & MCP](#5-communication-protocols--mcp) | WebSocket, MQTT+UDP, MCP protocol and usage | 4 documents |
| [Smart Home](#6-smart-home-integration) | Home Assistant integration | 1 document |

## 1. Getting Started

| Document | Description |
|---|---|
| [Firmware Flashing Guide](./docs/firmware-flashing-guide.md) | Flash the robot with the Flash Download Tool on a PC (no IDF environment needed) or via a web browser, plus flashing troubleshooting. |

## 2. Console & Account

| Document | Description |
|---|---|
| [XiaoZhi Console Configuration Guide](./docs/xiaozhi-console.md) | Configure language, voice/timbre, role introduction (with a ready-to-use Albee role template), model selection, memory mode, and voiceprint recognition on xiaozhi.me. |
| [Developer Authentication](./docs/developer-auth.md) | Bind a GitHub account to unlock more LLMs (Qwen3 / DeepSeek full / Doubao / GLM), higher quotas, and beta MCP services. Includes the open-source-user vs. developer benefit comparison. |
| [Account & Device Issues](./docs/account-help.md) | Cannot receive the SMS verification code, forgot username/password, how to get the device ID and MAC address, and how to unbind a device (with the unbind template and serial tool downloads). |
| [Device Freeze or Reboot Feedback Guide](./docs/problem-feedback.md) | How to report an unexpected freeze or reboot: describing what happened, getting the boot reason via `http://<device-ip>/info`, and serial run logs. |
| [Knowledge Base Guide](./docs/knowledge-base.md) | Strengthen the AI in a specific domain: create a knowledge base, upload documents, link it to the agent — with an important description template that tells the AI when it must consult the knowledge base. |

## 3. Feature Guides

| Document | Description |
|---|---|
| [Lighting Control Guide](./docs/lighting-control.md) | Control GLEDOPTO 2.4G RF LED strips and WLED controllers from the built-in web page (`http://<robot-ip>/light`), by voice, or via the HTTP API. Covers pairing, groups, naming, and the full API reference. |
| [Alarm & Reminder Guide](./docs/alarm-reminder.md) | Voice-controlled reminders: one-time countdown, daily, weekly, and interval repeats. Trigger behavior (ring pattern, snooze, auto-stop), limits, and persistence. |
| [Emoji Change Guide](./docs/expression-change-guide.md) | Two ways to change the screen emoji: online via the XiaoZhi console, or replace the GIFs under `extracted_emojis/` and rebuild the firmware. |
| [FAQ](./docs/faq.md) | Volume, Wi-Fi reconfiguration, music, Bluetooth, wake word, voice/timbre, voiceprint recognition, custom voice, voice control of other devices, LLM support, freeze/reboot feedback. |

## 4. Firmware & Hardware Development

| Document | Description |
|---|---|
| [Firmware Compilation Tutorial](./docs/compilation-tutorial.md) | Build the firmware from source: ESP-IDF v5.4.3 environment setup (Linux command line / Windows VSCode), project layout, partition table, build options (menuconfig), flashing methods, firmware merging and release scripts, and a build FAQ. |
| [Pin Mapping](./docs/pin-mapping.md) | Complete GPIO table for every peripheral: power management, buttons, I2C bus, LCD, LT8900 RF, servos, WS2811 LED ring, voice codec — plus notes on the shared SPI lines and I2C devices. |
| [OTA API](./docs/ota-api.md) | The device OTA upgrade REST API: request headers, request body, and full request/response examples. |

## 5. Communication Protocols & MCP

| Document | Description |
|---|---|
| [WebSocket Communication Protocol](./docs/websocket.md) | The device ↔ server WebSocket protocol: handshake, request headers, binary protocol versions v1/v2/v3, all JSON message types (STT/LLM/TTS/MCP/System/Alert/Custom), device state machines, and error handling. |
| [MQTT + UDP Hybrid Communication Protocol](./docs/mqtt-udp.md) | The alternative dual-channel transport: MQTT for control, encrypted UDP (AES-CTR) for real-time audio. Packet format, sequence/anti-replay, state management, and a comparison against WebSocket. |
| [MCP Protocol Interaction Flow](./docs/mcp-protocol.md) | Wire-level MCP: JSON-RPC 2.0 payload structure, the initialize → tools/list (with pagination) → tools/call flow, response formats, and a sequence diagram. |
| [MCP IoT Control Usage Guide](./docs/mcp-usage.md) | How to actually control the robot via MCP: the tool catalog (framework / robot / power / light / alarm / user-only tools), parameter tables, registration API with code examples, and JSON-RPC call examples. |

## 6. Smart Home Integration

| Document | Description |
|---|---|
| [Home Assistant Integration Guide](./docs/home-assistant.md) | Connect Home Assistant through MCP plugins: HA MCP for XiaoZhi (direct WebSocket, no proxy) and Home MCP (standardized device control and data access). |

---

## Reading Paths

- **I just got the robot:** [Flashing Guide](./docs/firmware-flashing-guide.md) → [Console Configuration](./docs/xiaozhi-console.md) → [FAQ](./docs/faq.md)
- **I want to control my lights:** [Lighting Control Guide](./docs/lighting-control.md)
- **I want to develop firmware:** [Compilation Tutorial](./docs/compilation-tutorial.md) → [Pin Mapping](./docs/pin-mapping.md)
- **I want to build a server / integrate the protocol:** [WebSocket](./docs/websocket.md) or [MQTT+UDP](./docs/mqtt-udp.md) → [MCP Protocol](./docs/mcp-protocol.md) → [MCP Usage](./docs/mcp-usage.md) → [OTA API](./docs/ota-api.md)

> Shared images and downloadable assets live in [`../assets/`](../assets/) (images under `assets/img/`), used by both the Chinese and English versions.

---

**Last modified:** 2026-10-08
