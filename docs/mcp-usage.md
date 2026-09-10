# MCP IoT Control Usage Guide

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
- **callback**: execution logic invoked when the backend calls the tool. May return a `ReturnValue` of bool, int, or string.
- **user-only tools**: registered via `AddUserOnlyTool`, these are device-owner/admin tools (e.g. `self.reboot`, `self.upgrade_firmware`, `self.screen.snapshot`). They only appear in `tools/list` responses when the request sets `"withUserTools": true`.

Framework built-ins (device status, volume, brightness, camera, etc.) are registered in `McpServer::AddCommonTools()` / `AddUserOnlyTools()` in `main/mcp_server.cc`. Board-specific tools are registered at:

- `RobotController::RegisterMcpTools()` — `main/boards/gledopto-robot/robot_controller.cc` (motion, battery)
- `LightController::RegisterMcpTools()` — `main/boards/gledopto-robot/light/light_controller.cc` (light groups, RF pairing)
- `InitializeAlarmMcpTools()` — `main/boards/gledopto-robot/alarm/alarm_mcp_tools.cc` (reminders/alarms)
- `InitializePowerManager()` — `main/boards/gledopto-robot/gledopto_robot.cc` (power control)

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
- This document shows only a few representative examples, not the complete tool set.
- See [`mcp-protocol.md`](./mcp-protocol.md) for protocol details and advanced usage.