# Exposing Home Assistant Devices

> Firmware: Albee v2.0.9 ｜ Audience: Developer

> [!IMPORTANT]
>
> **You must expose (add) your existing Home Assistant devices by following this guide before Albee can control them by voice via MCP.** Devices that are not exposed are invisible to MCP and cannot be controlled.

This applies to every scenario where Home Assistant is integrated through an MCP plugin. See the companion guides: [Home Assistant Integration Guide](home-assistant.md) and the [ha-mcp-for-xiaozhi Guide](ha-mcp-for-xiaozhi.md).

## How to Expose Entities

1. The tools available depend on which kinds of entities you expose to the Home Assistant voice assistant

```
Settings -> Voice assistants -> Expose
```

<img src="assets/img/ha-mcp-for-xiaozhi/7.png">

The "Voice assistants -> Expose" page:

<img src="assets/img/ha-mcp-for-xiaozhi/11.png">

Example of the tools available after exposing entities:

<img src="assets/img/ha-mcp-for-xiaozhi/12.png">

2. Once exposed, the devices can be controlled by voice, e.g. "Turn on the living-room light in Home Assistant"

## FAQ

- **Few tools available**: the more entities you expose (and the more kinds), the more tools you get — you need to expose your entity devices
- **Cannot control a device**: make sure you have exposed it

---

**Last modified:** 2026-11-12
