# OTA API
> 适用固件：Albee v2.0.4 及以上 ｜ 适用对象：开发者


> 普通用户提示：无需对接服务器也可以升级固件 —— 通过设备内置网页上传 `.ota` 文件即可，参见[本地OTA升级指南](./本地OTA升级指南.md)。

## 概述

本 API 处理设备 OTA（Over-The-Air，空中升级）请求。设备发送自身设备信息和当前固件版本，服务器返回最新固件版本和下载链接（如有更新）。

## 请求方法

**POST** `https://api.tenclass.net/xiaozhi/ota/`（路径为 `/xiaozhi/ota/`）

设备**无条件发送**以下请求头；仅当系统信息 JSON 非空时使用 POST 并携带请求体，否则使用 GET（无请求体）。

## 请求头

- `Device-Id`：设备唯一标识（必填）。注意：本固件启用 `CONFIG_ROBOT_IDENTITY_RESET=y`，上报的是**随机持久化的身份 MAC**，不一定是硬件 MAC
- `Client-Id`：客户端唯一标识，UUID v4（必填）
- `User-Agent`：客户端名称和版本号（必填，如 `esp-box-3/1.5.6`）
- `Accept-Language`：客户端当前语言（设备始终携带，如 `zh-CN`）
- `Activation-Version`：激活版本信息
- `Serial-Number`：设备序列号

## 请求体

| 字段 | 说明 |
|---|---|
| `application` | 固件版本信息（必填）：`version`、`name`、`compile_time`、`idf_version` 等 |
| `mac_address` | MAC 地址（可选） |
| `chip_model_name` | 芯片型号，如 `esp32s3`（可选） |
| `board` | 板子信息（必填）：`type`、`name`、`ssid`、`rssi`、`channel`、`ip`、`mac` 等 |

## ESP32 完整请求示例

```http
POST /xiaozhi/ota/ HTTP/1.1
Host: api.tenclass.net
Content-Type: application/json
User-Agent: xingzhi-cube/1.0.1
Device-Id: 11:22:33:44:55:66
Client-Id: 7b94d69a-9808-4c59-9c9b-704333b38aff
Accept-Language: zh-CN
Activation-Version: 1
Serial-Number: xxxxxxxx

{
  "application": { "version": "1.0.1", "name": "xingzhi-cube", "compile_time": "...", "idf_version": "5.4.3", "elf_sha256": "..." },
  "board": { "type": "xingzhi-cube", "name": "xingzhi-cube", "ssid": "Home", "rssi": -55, "channel": 6, "ip": "192.168.1.50", "mac": "11:22:33:44:55:66" }
}
```

## 响应示例

```json
{
  "mqtt": { "endpoint": "mqtt.example.com", "client_id": "..." },
  "websocket": { "url": "wss://api.tenclass.net/xiaozhi/v1/", "token": "..." },
  "server_time": { "timestamp": 1633024800000 },
  "firmware": { "version": "1.0.0", "url": "https://example.com/firmware/1.0.0.bin" },
  "activation": { }
}
```

---

**文档最新修改时间：** 2026-10-13
