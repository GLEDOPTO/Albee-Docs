# MCP IoT Control Usage Guide
> Firmware: Albee v2.0.4+ (tool toggles and `self.screen.show_emoji` require v2.0.5+) ｜ Audience: Developer


> This document explains how to control this ESP32 desktop robot via MCP (Model Context Protocol). For wire-level protocol details, see [`mcp-protocol.md`](./mcp-protocol.md).

## Introduction

MCP (Model Context Protocol) is the recommended protocol for IoT control in this project. It uses standard JSON-RPC 2.0 messages carried over the base transport (WebSocket or MQTT), letting the backend discover and invoke "tools" exposed by the device, so an AI agent can control the robot on behalf of the user.

## Typical Usage Flow

1. On startup, the device connects to the backend over the base protocol (WebSocket/MQTT) and sends a `hello` message announcing its features, including `"mcp": true`.
2. The backend initializes the MCP session with the `initialize` method.
3. The backend retrieves the tool catalog with `tools/list`. Passing `"withUserTools": true` additionally returns user-only tools (admin features such as reboot and firmware upgrade, hidden from normal agent sessions by default).
4. The backend invokes a specific tool with `tools/call` to control the device.

See [`mcp-protocol.md`](./mcp-protocol.md) for the full message format and interaction details.

## Registering Tools on the Device

Tools are registered on the `McpServer` singleton (`main/mcp_server.h`). The two commonly used signatures are:

```cpp
void AddTool(const std::string& name,
             const std::string& description,
             const PropertyList& properties,
             std::function<ReturnValue(const PropertyList&)> callback);

void AddUserOnlyTool(const std::string& name,
                     const std::string& description,
                     const PropertyList& properties,
                     std::function<ReturnValue(const PropertyList&)> callback);
```

- **name**: unique tool identifier, following the `self.<module>.<function>` convention (e.g. `self.robot.action`).
- **description**: natural-language description of what the tool does and when to use it. This is what the LLM reads, so write it for the model, not for the developer. Descriptions are bilingual behind the `USE_ENGLISH_ENABLE` compile flag.
- **properties**: input parameter list. Supported types are boolean, integer, and string, with optional range and default values.
- **callback**: execution logic invoked when the backend calls the tool. `ReturnValue` supports bool, int, string, JSON text (`cJSON*`), and image content (`ImageContent*`, e.g. screen snapshots).
- **user-only tools**: registered via `AddUserOnlyTool`, these are device-owner/admin tools (e.g. `self.reboot`, `self.upgrade_firmware`, `self.screen.snapshot`). They only appear in `tools/list` responses when the request sets `"withUserTools": true`.

Framework built-ins (device status, volume, brightness, etc.) are registered in `McpServer::AddCommonTools()` / `AddUserOnlyTools()` in `main/mcp_server.cc`. Board-specific tools are registered at:

- `RobotController::RegisterMcpTools()` — `main/boards/gledopto-robot/robot_controller.cc` (motion, battery)
- `LightController::RegisterMcpTools()` — `main/boards/gledopto-robot/light/light_controller.cc` (light groups, RF pairing)
- `InitializeAlarmMcpTools()` — `main/boards/gledopto-robot/alarm/alarm_mcp_tools.cc` (reminders/alarms)
- `InitializePowerManager()` — `main/boards/gledopto-robot/gledopto_robot.cc` (power control)
- `InitializeEmojiMcpTool()` — `main/boards/gledopto-robot/gledopto_robot.cc` (on-screen emoji playback `self.screen.show_emoji`, v2.0.5+)

## Tool Catalog

The complete set of tools registered by this firmware, grouped by module. Params marked with a range/default show the values enforced by the device.

### Framework tools (`main/mcp_server.cc`, `AddCommonTools`)

| Tool | Parameters | Description |
|---|---|---|
| `self.get_device_status` | — | Real-time device status (speaker, screen, battery, network). Call before asking about or changing device state. |
| `self.audio_speaker.set_volume` | `volume` int 0–100 | Set the speaker volume. |
| `self.screen.set_brightness` | `brightness` int 0–100 | Set the screen brightness. |

### Robot tools (`main/boards/gledopto-robot/robot_controller.cc`)

| Tool | Parameters | Description |
|---|---|---|
| `self.robot.action` | `action` str: `walk`/`turn`/`spin`/`home` (default `home`); `steps` str (default `"4"`; spin uses 0.1–2.0 = circle count (0.5 = half a turn, 1 = one full turn, 2 = two turns)); `speed` int 500–2000 (default 800, smaller = faster); `direction` int 1/-1 (default 1) | Execute a motion action and wait for completion. |
| `self.robot.stop` | — | Stop all actions immediately and reset. |
| `self.battery.get_level` | — | Battery level and charging status (JSON). |

### Power tool (`main/boards/gledopto-robot/gledopto_robot.cc`)

| Tool | Parameters | Description |
|---|---|---|
| `self.power.control` | `action` str: `shutdown` (default) / `restart` (`reboot` is accepted as an alias of `restart`) | Power the robot off or reboot it. |

### Screen-emoji tool (`main/boards/gledopto-robot/gledopto_robot.cc`, v2.0.5+)

| Tool | Parameters | Description |
|---|---|---|
| `self.screen.show_emoji` | `name` str (emoji name, default `happy`; must match `^[a-z][a-z0-9_-]{0,26}$`) | Play an emoji animation by name on the screen — covers all built-in emoji (happy/sad/angry/sleepy, etc.) and custom emoji uploaded via the `/emoji` web page (see the [Emoji Change Guide](expression-change-guide.md)). Returns `true` on success; a name that is "uploaded but not applied" returns `error: '<name>' is staged but not applied yet — apply the pending list on the /emoji web page first`; an unknown name returns `error: unknown emoji '<name>'. Available: <all available emoji names>`. |

### Light tools (`main/boards/gledopto-robot/light/light_controller.cc`)

| Tool | Parameters | Description |
|---|---|---|
| `self.light.control_group` | `group_name` str (or `all`); `action` str: `on`/`off`/`toggle` | Switch a light group (RF and/or WLED). |
| `self.light.set_group_color` | `group_name` str; `red`/`green`/`blue` int 0–255 | Set RGB color. For white/warm white use color temperature instead. |
| `self.light.set_group_brightness` | `group_name` str; `brightness` int 0–255 | Set brightness. |
| `self.light.set_group_color_temp` | `group_name` str; `temperature` int 0–100 (0 = warmest, 100 = coolest) | Set color temperature. |
| `self.light.set_group_effect` | `group_name` str; `effect` str: `next`/`prev`/`random`/effect ID/name | Set a WLED effect (WLED groups only). |
| `self.light.get_all_group_name` | — | List all RF and WLED group names. |
| `self.light.get_ip` | — | Return the device IP and the lighting page URL (both the bare IP and `<IP>/light`). |
| `self.light.schedule_control` | `group_name` str; `action` str: `on`/`off`/`toggle`; `delay` int s (-1); `hour` int 0–23 (-1); `minute` int 0–59 (-1); `day_offset` int (-1; 0=today/1=tomorrow/2=day after); `weekdays` str; `interval` int s (-1); `repeat` int (1=once, -1=forever, N=total count) | Scheduled / linked lighting (registered when `CONFIG_LIGHT_SCHEDULE_LINKAGE=y`). |

### Alarm tools (`main/boards/gledopto-robot/alarm/alarm_mcp_tools.cc`)

| Tool | Parameters | Description |
|---|---|---|
| `add_reminder` | `delay` int (seconds from now, -1 = not specified); `hour` int 0–23 (-1); `minute` int 0–59 (-1); `day_offset` int (-1; 0=today/1=tomorrow/2=day after); `repeat` int (**required**; 1=once, -1=forever, N=total count); `content` str; `interval` int seconds (-1, e.g. 3600 = hourly); `weekdays` str (default `""`, e.g. `Mon,Fri`, `everyday`) | Add a reminder: countdown, daily, weekly, or fixed-interval. |
| `delete_reminder` | `id` int (-1); `keyword` str (default `""`); `clear_all` bool (default false). Exactly **one of the three**: by ID, by keyword, or clear all. | Delete reminders. |
| `list_reminders` | — | List all reminders with ID, time, content, and repeat type. |

### User-only tools (`main/mcp_server.cc`, `AddUserOnlyTools`)

Only returned by `tools/list` when the request sets `"withUserTools": true`.

| Tool | Parameters | Description |
|---|---|---|
| `self.get_system_info` | — | System information (JSON). |
| `self.reboot` | — | Reboot the system. |
| `self.upgrade_firmware` | `url` str | Download and install firmware from a URL, then reboot (OTA). |
| `self.screen.get_info` | — | Screen width/height, monochrome flag. |
| `self.screen.snapshot` | `url` str; `quality` int 1–100 (default 80) | Snapshot the screen and upload the JPEG to a URL. |
| `self.screen.preview_image` | `url` str | Download an image and preview it on the screen. |
| `self.assets.set_download_url` | `url` str | Set the download URL of the assets partition. |

### Registered conditionally or disabled in source

| Tool | Status |
|---|---|
| `self.camera.take_photo` | Not registered on this board (no camera). |
| `self.screen.set_theme` | Removed from the source (historically disabled via `#if 0`). |
| `self.light.rf_pair_group` / `rf_clear_group` / `rf_clear_all` | Removed from the source (historically disabled via `#if 0`); RF pairing/clearing is done via the web page's HTTP endpoints (`/api/light/pair`, `/api/light/clear`), which are always available. |

## Tool Toggles (web management, v2.0.5+)

Starting from firmware v2.0.5 the built-in web adds an "MCP Tools" page (`http://<device-ip>/mcp`) where you can toggle individual MCP tools available to the voice assistant:

- The **Manage tools** master switch at the top of the page defaults to **off** (NVS `mcp` namespace, `manage` key, default `false`). While it is off, the tool list is greyed out and non-operable, all tools stay enabled, and the voice assistant is unaffected.
- Individual tools can only be toggled after the master switch is turned on; **turning the master switch off re-enables all tools automatically**.
- User-only tools (registered via `AddUserOnlyTool`, e.g. `self.reboot`) never appear on this page and cannot be toggled here; tools on a backend-built MCP access point never pass through the device either and are out of scope.
- Toggle states persist in the NVS `mcp` namespace `disabled_tools` key (a comma-separated list of tool names); a factory reset clears the namespace and restores all tools to enabled.

Behavior details:

- Disabled tools **do not appear in `tools/list` responses** — they are not reported to the backend and do not count against the backend's tool quota (equivalent to compile-time trimming, but reversible and without a reboot).
- Even if the backend has cached an old tool list, a `tools/call` to a disabled tool is rejected by the device with the error `Tool disabled: <tool name>`.
- After every toggle the device sends a `notifications/tools/list_changed` notification prompting the backend to re-fetch the list (the backend may ignore it; see section 5 of the [protocol document](mcp-protocol.md)).
- **When it takes effect**: new sessions, no device reboot needed. If the AI still says "no such feature" after reopening the conversation, start a new conversation and try again.

HTTP endpoints (`main/boards/gledopto-robot/web/web_mcp_api.cc`):

| Request | Description |
|---|---|
| `GET /api/mcp/tools` | Returns `{"success":true,"manage":<bool>,"tools":[{"name","description","enabled"},...]}` (user-only tools not included) |
| `POST /api/mcp/tools`, body `{"manage": true/false}` | Toggle the master switch; setting `false` re-enables all tools automatically |
| `POST /api/mcp/tools`, body `{"name":"<tool>","enabled":true/false}` | Toggle one tool; with the master switch off it errors `tool management is off`, unknown tools error `unknown tool: <name>` |

Note: if a console PIN is set on the device, POSTs must unlock first (`POST /api/auth/unlock`) before changing toggles; GET is unaffected.

## Registration Examples

The examples below are simplified from the actual project code.

```cpp
auto& mcp = McpServer::GetInstance();

// 1. No parameters: stop all robot actions immediately
mcp.AddTool("self.robot.stop", "Immediately stop all actions and reset",
    PropertyList(),
    [this](const PropertyList&) -> ReturnValue {
        Stop();
        return true;
    });

// 2. Integer parameter with range: set the speaker volume
mcp.AddTool("self.audio_speaker.set_volume",
    "Set the volume of the audio speaker.",
    PropertyList({
        Property("volume", kPropertyTypeInteger, 0, 100)
    }),
    [&board](const PropertyList& properties) -> ReturnValue {
        board.GetAudioCodec()->SetOutputVolume(properties["volume"].value<int>());
        return true;
    });

// 3. String parameter with default value: control the device power
mcp.AddTool("self.power.control",
    "Control the device power. Action 'shutdown' (default) powers the robot off; 'restart' reboots it.",
    PropertyList({
        Property("action", kPropertyTypeString, "shutdown")
    }),
    [this](const PropertyList& properties) -> ReturnValue {
        // handle "shutdown" / "restart" ...
        return std::string("Shutting down...");
    });
```

## JSON-RPC Call Examples

### 1. List tools

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": { "cursor": "" },
  "id": 1
}
```

### 2. Make the robot walk

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.robot.action",
    "arguments": { "action": "walk", "steps": "4", "speed": 800, "direction": 1 }
  },
  "id": 2
}
```

### 3. Turn on all lights

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.light.control_group",
    "arguments": { "group_name": "all", "action": "on" }
  },
  "id": 3
}
```

## Notes

- The authoritative source for tool names, parameters, and return values is the device-side `AddTool` registration (see the registration sites listed above); the runtime catalog is always available via `tools/list`.
- See [`mcp-protocol.md`](./mcp-protocol.md) for protocol details and advanced usage.

---

**Last modified:** 2026-10-13
