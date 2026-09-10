# MCP IoT 控制使用指南

> 本文档介绍如何通过 MCP（Model Context Protocol）控制这台 ESP32 桌面机器人。线级协议细节请参见 [`mcp-protocol.md`](./mcp-protocol.md)。

## 简介

MCP（Model Context Protocol）是本项目推荐的 IoT 控制协议。它使用标准的 JSON-RPC 2.0 消息，承载在基础传输层（WebSocket 或 MQTT）之上，让后端可以发现并调用设备暴露的"工具（tools）"，从而由 AI 智能体代替用户控制机器人。

## 典型使用流程

1. 启动时，设备通过基础协议（WebSocket/MQTT）连接后端，发送 `hello` 消息宣告自身能力，其中包括 `"mcp": true`。
2. 后端通过 `initialize` 方法初始化 MCP 会话。
3. 后端通过 `tools/list` 获取工具目录。传入 `"withUserTools": true` 可额外返回仅用户可用的工具（重启、固件升级等管理功能，默认对普通智能体会话隐藏）。
4. 后端通过 `tools/call` 调用具体工具来控制设备。

完整的消息格式与交互细节请参见 [`mcp-protocol.md`](./mcp-protocol.md)。

## 在设备上注册工具

工具注册在 `McpServer` 单例上（`main/mcp_server.h`）。两个常用的函数签名如下：

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

- **name**：工具唯一标识，遵循 `self.<模块>.<功能>` 命名约定（如 `self.robot.action`）。
- **description**：工具做什么、何时使用的自然语言描述。这是给 LLM 读的，请面向模型而非开发者撰写。描述文案由 `USE_ENGLISH_ENABLE` 编译开关控制，支持中英双语。
- **properties**：输入参数列表。支持 boolean、integer、string 类型，可选范围和默认值。
- **callback**：后端调用该工具时执行的逻辑。可返回 bool、int 或 string 类型的 `ReturnValue`。
- **仅用户可用工具**：通过 `AddUserOnlyTool` 注册，属于设备所有者/管理员工具（如 `self.reboot`、`self.upgrade_firmware`、`self.screen.snapshot`）。只有当 `tools/list` 请求设置 `"withUserTools": true` 时才会出现在响应中。

框架内置工具（设备状态、音量、亮度、摄像头等）注册在 `main/mcp_server.cc` 的 `McpServer::AddCommonTools()` / `AddUserOnlyTools()` 中。板级专用工具注册位置：

- `RobotController::RegisterMcpTools()` —— `main/boards/gledopto-robot/robot_controller.cc`（运动、电池）
- `LightController::RegisterMcpTools()` —— `main/boards/gledopto-robot/light/light_controller.cc`（灯组、RF 配对）
- `InitializeAlarmMcpTools()` —— `main/boards/gledopto-robot/alarm/alarm_mcp_tools.cc`（提醒/闹钟）
- `InitializePowerManager()` —— `main/boards/gledopto-robot/gledopto_robot.cc`（电源控制）

## 工具目录

本固件注册的全部工具，按模块分组。标注了范围/默认值的参数以设备端实际约束为准。

### 框架工具（`main/mcp_server.cc`，`AddCommonTools`）

| 工具 | 参数 | 说明 |
|---|---|---|
| `self.get_device_status` | — | 设备实时状态（扬声器、屏幕、电池、网络）。在询问或修改设备状态前先调用。 |
| `self.audio_speaker.set_volume` | `volume` int 0–100 | 设置扬声器音量。 |
| `self.screen.set_brightness` | `brightness` int 0–100 | 设置屏幕亮度。 |

### 机器人工具（`main/boards/gledopto-robot/robot_controller.cc`）

| 工具 | 参数 | 说明 |
|---|---|---|
| `self.robot.action` | `action` str：`walk`/`turn`/`spin`/`home`（默认 `home`）；`steps` str（默认 `"4"`；spin 用 0.1–0.5 表示圈的比例）；`speed` int 500–2000（默认 800，越小越快）；`direction` int 1/-1（默认 1） | 执行动作并等待完成。 |
| `self.robot.stop` | — | 立即停止所有动作并复位。 |
| `self.battery.get_level` | — | 电量与充电状态（JSON）。 |

### 电源工具（`main/boards/gledopto-robot/gledopto_robot.cc`）

| 工具 | 参数 | 说明 |
|---|---|---|
| `self.power.control` | `action` str：`shutdown`（默认）/ `restart` | 机器人关机或重启。 |

### 灯光工具（`main/boards/gledopto-robot/light/light_controller.cc`）

| 工具 | 参数 | 说明 |
|---|---|---|
| `self.light.control_group` | `group_name` str（或 `all`）；`action` str：`on`/`off`/`toggle` | 开关某个灯组（RF 和/或 WLED）。 |
| `self.light.set_group_color` | `group_name` str；`red`/`green`/`blue` int 0–255 | 设置 RGB 颜色。白光/暖白光请改用色温。 |
| `self.light.set_group_brightness` | `group_name` str；`brightness` int 0–255 | 设置亮度。 |
| `self.light.set_group_color_temp` | `group_name` str；`temperature` int 0–100（0 = 最暖，100 = 最冷） | 设置色温。 |
| `self.light.set_group_effect` | `group_name` str；`effect` str：`next`/`prev`/`random`/效果 ID/名称 | 设置 WLED 效果（仅 WLED 分组）。 |
| `self.light.get_all_group_name` | — | 列出所有 RF 和 WLED 分组名。 |
| `self.light.get_ip` | — | 返回设备裸 IP 地址。 |
| `self.light.get_light_control_ip` | — | 返回灯光控制页地址（`<IP>/light`）。 |

### 闹钟工具（`main/boards/gledopto-robot/alarm/alarm_mcp_tools.cc`）

| 工具 | 参数 | 说明 |
|---|---|---|
| `add_reminder` | `delay` int（距当前秒数，-1 = 未指定）；`hour` int 0–23（-1）；`minute` int 0–59（-1）；`repeat` int（-1 = 永久）；`content` str；`interval` int 秒（如 3600 = 每小时）；`weekdays` str（如 `Mon,Fri`、`everyday`） | 添加提醒：倒计时、每天、每周或固定间隔。 |
| `delete_reminder` | `keyword` str（默认 `""`） | 删除内容包含关键词的提醒；关键词为空则清空全部。 |
| `list_reminders` | — | 列出所有提醒的 ID、时间、内容和重复类型。 |

### 仅用户可用工具（`main/mcp_server.cc`，`AddUserOnlyTools`）

仅当 `tools/list` 请求设置 `"withUserTools": true` 时才返回。

| 工具 | 参数 | 说明 |
|---|---|---|
| `self.get_system_info` | — | 系统信息（JSON）。 |
| `self.reboot` | — | 重启系统。 |
| `self.upgrade_firmware` | `url` str | 从 URL 下载并安装固件，然后重启（OTA）。 |
| `self.screen.get_info` | — | 屏幕宽/高、单色标志。 |
| `self.screen.snapshot` | `url` str；`quality` int 1–100（默认 80） | 截取屏幕并将 JPEG 上传到 URL。 |
| `self.screen.preview_image` | `url` str | 下载图片并在屏幕上预览。 |
| `self.assets.set_download_url` | `url` str | 设置资源分区的下载 URL。 |

### 按条件注册或在源码中禁用

| 工具 | 状态 |
|---|---|
| `self.camera.take_photo` | 本板未注册（无摄像头）。 |
| `self.screen.set_theme` | 已编译禁用（`mcp_server.cc` 中 `#if 0`）。 |
| `self.light.rf_pair_group` / `rf_clear_group` / `rf_clear_all` | 已编译禁用（`light_controller.cc` 中 `#if 0`）；RF 配对/清除通过网页的 HTTP 接口完成（`/api/light/pair`、`/api/light/clear`），始终可用。 |

## 注册示例

以下示例简化自项目实际代码。

```cpp
auto& mcp = McpServer::GetInstance();

// 1. 无参数：立即停止机器人所有动作
mcp.AddTool("self.robot.stop", "立即停止所有动作并复位",
    PropertyList(),
    [this](const PropertyList&) -> ReturnValue {
        Stop();
        return true;
    });

// 2. 带范围的整数参数：设置扬声器音量
mcp.AddTool("self.audio_speaker.set_volume",
    "设置扬声器的音量。",
    PropertyList({
        Property("volume", kPropertyTypeInteger, 0, 100)
    }),
    [&board](const PropertyList& properties) -> ReturnValue {
        board.GetAudioCodec()->SetOutputVolume(properties["volume"].value<int>());
        return true;
    });

// 3. 带默认值的字符串参数：控制设备电源
mcp.AddTool("self.power.control",
    "控制设备电源。action 为 'shutdown'（默认）时机器人关机；'restart' 时重启。",
    PropertyList({
        Property("action", kPropertyTypeString, "shutdown")
    }),
    [this](const PropertyList& properties) -> ReturnValue {
        // 处理 "shutdown" / "restart" ...
        return std::string("正在关机...");
    });
```

## JSON-RPC 调用示例

### 1. 列出工具

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": { "cursor": "" },
  "id": 1
}
```

### 2. 让机器人行走

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

### 3. 打开所有灯

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

## 注意事项

- 工具名、参数和返回值的权威来源是设备端的 `AddTool` 注册（见上文列出的注册位置）；运行时目录随时可通过 `tools/list` 获取。
- 协议细节和高级用法请参见 [`mcp-protocol.md`](./mcp-protocol.md)。
