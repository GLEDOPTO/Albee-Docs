# Albee Encyclopaedia

> One-stop index of all Albee desktop robot documentation. Every entry below links to a full document — click to jump.
>
> Language: English | 中文版：[../中文版本/Albee百科全书.md](../中文版本/Albee百科全书.md)
>
> Project overview: [README.md](./README.md)

## Document Map

| Category | What it covers | Documents |
|---|---|---|
| [Getting Started](#1-getting-started) | Unbox → power on & Wi-Fi → activation → first conversation | 1 document |
| [Feature Guides](#2-feature-guides) | Web console overview, finding the device IP, lighting control, alarms & reminders, emoji change, network change, LED states, head LED effects, servo calibration, local OTA upgrade | 10 documents |
| [Troubleshooting & Support](#3-troubleshooting--support) | FAQ, device freeze or reboot feedback | 2 documents |
| [Console & Account](#4-console--account) | xiaozhi.me console, developer auth, account issues, knowledge base, MAC address | 5 documents |
| [Firmware & Hardware Development](#5-firmware--hardware-development) | Firmware flashing, compiling from source, pin mapping, OTA API | 4 documents |
| [Protocols & MCP](#6-communication-protocols--mcp) | WebSocket, MQTT+UDP, MCP protocol and usage | 4 documents |
| [Smart Home](#7-smart-home-integration) | Home Assistant integration, MCP access point, ha-mcp-for-xiaozhi | 3 documents |

## 1. Getting Started

| Document | Description |
|---|---|
| [Device Activation Guide](./docs/device-activation.md) | The first step after unboxing: long-press the power button to start → connect to the Albee-xxxx hotspot and configure Wi-Fi → enter the six-digit activation code on xiaozhi.me to bind the device (including registration/login and language settings). |

## 2. Feature Guides

| Document | Description |
|---|---|
| [Lighting Control Guide](./docs/lighting-control.md) | Control GLEDOPTO 2.4G RF LED strips and WLED controllers from the built-in web page (`http://<robot-ip>/light`), by voice, or via the HTTP API. Covers pairing, groups, naming, and the full API reference. |
| [Alarm & Reminder Guide](./docs/alarm-reminder.md) | Voice-controlled reminders: one-time countdown, daily, weekly, and interval repeats. Trigger behavior (ring pattern, pause between rounds, auto-stop), limits, and persistence. |
| [Emoji Change Guide](./docs/expression-change-guide.md) | Two ways to change the screen emoji: online via the XiaoZhi console, or replace the GIFs under `extracted_emojis/` and rebuild the firmware. |
| [Network Change Guide](./docs/change-network.md) | Three ways to switch Wi-Fi: single-click the function button during the blue flowing-LED phase, switch to a saved network via the web page (`http://<device-ip>/network`), or scan and join a new network (with password-box rules). |
| [Device States & LED Indicators](./docs/device-led-states.md) | The mapping table of 11 device states to 9 LED behaviors, the factory-default state → effect mapping (scroll / blink / fade-out / solid / breathe / rainbow), and brightness scaling notes. |
| [Head LED Effects Change Guide](./docs/head-led-effects.md) | Change the head LED effects online via the web page (`http://<device-ip>/led`); for developers: slots, effects, animation implementation, and NVS packing format in `led_config.cc` / `circular_strip.cc` (with a pitfall checklist). |
| [Servo Calibration Guide](./docs/servo-calibration.md) | Correct the reset-pose deviation of the four servos: fine-tune by ±1° via the web page (`http://<device-ip>/robot`), servo-to-button mapping, and the leg scale mark (lay the robot down while adjusting). |
| [Local OTA Upgrade Guide](./docs/local-ota.md) | Upgrade the firmware locally via the device's built-in web page (`http://<device-ip>/update`) by uploading a `.ota` file — no PC flashing needed. |
| [Built-in Web Console Overview](./docs/web-console.md) | Entry point for the built-in pages: what `/light`, `/network`, `/led`, `/robot`, `/info` and `/update` do, prerequisites, and FAQ. |
| [Find the Device IP Address](./docs/check-device-ip.md) | Read this before opening any web page: three ways to get the IP — ask by voice, router admin page, or serial log. |

## 3. Troubleshooting & Support

| Document | Description |
|---|---|
| [FAQ](./docs/faq.md) | Volume, Wi-Fi reconfiguration, music, Bluetooth, wake word, voice/timbre, voiceprint recognition, custom voice, voice control of other devices, LLM support, freeze/reboot feedback, servo calibration. |
| [Device Freeze or Reboot Feedback Guide](./docs/problem-feedback.md) | How to report an unexpected freeze or reboot: describing what happened, getting the boot reason via `http://<device-ip>/info`, and serial run logs. |

## 4. Console & Account

| Document | Description |
|---|---|
| [XiaoZhi Console Configuration Guide](./docs/xiaozhi-console.md) | Configure language, voice/timbre, role introduction (with a ready-to-use Albee role template), model selection, memory mode, and voiceprint recognition on xiaozhi.me. |
| [Developer Authentication](./docs/developer-auth.md) | Bind a GitHub account to unlock more LLMs (Qwen3 / DeepSeek full / Doubao / GLM), higher quotas, and beta MCP services. Includes the open-source-user vs. developer benefit comparison. |
| [Account & Device Issues](./docs/account-help.md) | Cannot receive the SMS verification code, forgot username/password, how to get the device ID and MAC address, and how to unbind a device (with the unbind template download). |
| [How to View the MAC Address](./docs/check-mac-address.md) | Two ways to get the MAC address: via the web page (`http://<device-ip>/info`) or a serial terminal tool (Tera Term, CoolTerm, etc., 115200 baud). |
| [Knowledge Base Guide](./docs/knowledge-base.md) | Strengthen the AI in a specific domain: create a knowledge base, upload documents, link it to the agent — with an important description template that tells the AI when it must consult the knowledge base. |

## 5. Firmware & Hardware Development

| Document | Description |
|---|---|
| [Firmware Flashing Guide](./docs/firmware-flashing-guide.md) | Flash the robot with the Flash Download Tool on a PC (no IDF environment needed) or via a web browser, plus flashing troubleshooting. |
| [Firmware Compilation Tutorial](./docs/compilation-tutorial.md) | Build the firmware from source: ESP-IDF v5.4.3 environment setup (Linux command line / Windows VSCode), project layout, partition table, build options (menuconfig), flashing methods, firmware merging and release scripts, and a build FAQ. |
| [Pin Mapping](./docs/pin-mapping.md) | Complete GPIO table for every peripheral: power management, buttons, I2C bus, LCD, LT8900 RF, servos, WS2811 LED ring, voice codec — plus notes on the shared SPI lines and I2C devices. |
| [OTA API](./docs/ota-api.md) | The device OTA upgrade REST API: request headers, request body, and full request/response examples. |

## 6. Communication Protocols & MCP

| Document | Description |
|---|---|
| [WebSocket Communication Protocol](./docs/websocket.md) | The device ↔ server WebSocket protocol: handshake, request headers, binary protocol versions v1/v2/v3, all JSON message types (STT/LLM/TTS/MCP/System/Alert/Custom), device state machines, and error handling. |
| [MQTT + UDP Hybrid Communication Protocol](./docs/mqtt-udp.md) | The alternative dual-channel transport: MQTT for control, encrypted UDP (AES-CTR) for real-time audio. Packet format, sequence/anti-replay, state management, and a comparison against WebSocket. |
| [MCP Protocol Interaction Flow](./docs/mcp-protocol.md) | Wire-level MCP: JSON-RPC 2.0 payload structure, the initialize → tools/list (with pagination) → tools/call flow, response formats, and a sequence diagram. |
| [MCP IoT Control Usage Guide](./docs/mcp-usage.md) | How to actually control the robot via MCP: the tool catalog (framework / robot / power / light / alarm / user-only tools), parameter tables, registration API with code examples, and JSON-RPC call examples. |

## 7. Smart Home Integration

| Document | Description |
|---|---|
| [Home Assistant Integration Guide](./docs/home-assistant.md) | Connect Home Assistant through MCP plugins: HA MCP for XiaoZhi (direct WebSocket, no proxy) and Home MCP (standardized device control and data access). |
| [ha-mcp-for-xiaozhi Guide](./docs/ha-mcp-for-xiaozhi.md) | Install the ha-mcp-for-xiaozhi integration via HACS, fill in the MCP access point to finish setup, plus troubleshooting notes (exposed entities decide the available tools, version differences, check the chat log to locate issues). |
| [How to Get the MCP Access-Point Address](./docs/mcp-access-point-address.md) | On the xiaozhi.me console, click Console → Configure → Extensions → Copy MCP access point. |

---

## Reading Paths

- **I want to open the built-in web pages:** [Built-in Web Console Overview](./docs/web-console.md) → [Find the Device IP Address](./docs/check-device-ip.md)
- **I just got the robot:** [Device Activation Guide](./docs/device-activation.md) → [Console Configuration](./docs/xiaozhi-console.md) → [FAQ](./docs/faq.md)
- **I want to control my lights:** [Lighting Control Guide](./docs/lighting-control.md)
- **Something goes wrong with the device:** [FAQ](./docs/faq.md) → [Device Freeze or Reboot Feedback Guide](./docs/problem-feedback.md)
- **I want to upgrade the firmware:** [Local OTA Upgrade Guide](./docs/local-ota.md) (upload a `.ota` file via the web page, no PC flashing)
- **I want to develop firmware:** [Compilation Tutorial](./docs/compilation-tutorial.md) → [Pin Mapping](./docs/pin-mapping.md)
- **I want to integrate smart home:** [Home Assistant Integration Guide](./docs/home-assistant.md) → [How to Get the MCP Access-Point Address](./docs/mcp-access-point-address.md) → [ha-mcp-for-xiaozhi Guide](./docs/ha-mcp-for-xiaozhi.md)
- **I want to build a server / integrate the protocol:** [WebSocket](./docs/websocket.md) or [MQTT+UDP](./docs/mqtt-udp.md) → [MCP Protocol](./docs/mcp-protocol.md) → [MCP Usage](./docs/mcp-usage.md) → [OTA API](./docs/ota-api.md)

> Shared images and downloadable assets live in [`../assets/`](../assets/) (images under `assets/img/`), used by both the Chinese and English versions.

---

**Last modified:** 2026-10-13
