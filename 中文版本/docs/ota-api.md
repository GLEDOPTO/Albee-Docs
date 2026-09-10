# OTA API

## 概述

本 API 处理设备 OTA（Over-The-Air，空中升级）请求。设备发送自身设备信息和当前固件版本，服务器返回最新固件版本和下载链接（如有更新）。

## 请求方法

**POST** `/api/ota/`

## 请求头

- `Device-Id`：设备唯一标识（必填，使用 MAC 地址）
- `Client-Id`：客户端唯一标识，UUID v4（必填）
- `User-Agent`：客户端名称和版本号（必填，如 `esp-box-3/1.5.6`）
- `Accept-Language`：客户端当前语言（可选，如 `zh-CN`）

## 请求体

| 字段 | 说明 |
|---|---|
| `application` | 包含设备当前固件版本信息的对象（必填） |
| `mac_address` | MAC 地址（可选） |
| `chip_model_name` | 芯片型号，如 `esp32s3`（可选） |
| `board` | 板子类型、名称、ssid、rssi（必填） |

## ESP32 完整请求示例

```http
POST /xiaozhi/ota/ HTTP/1.1
Host: api.tenclass.net
Content-Type: application/json
User-Agent: xingzhi-cube/1.0.1
Device-Id: 11:22:33:44:55:66
Client-Id: 7b94d69a-9808-4c59-9c9b-704333b38aff

{
  "application": { "version": "1.0.1", "elf_sha256": "..." },
  "board": { "type": "xingzhi-cube", "name": "xingzhi-cube", "ssid": "Home", "rssi": -55 }
}
```

## 响应示例

```json
{
  "mqtt": { "endpoint": "mqtt.example.com", "client_id": "..." },
  "websocket": { "url": "wss://api.tenclass.net/xiaozhi/v1/", "token": "..." },
  "server_time": { "timestamp": 1633024800000 },
  "firmware": { "version": "1.0.0", "url": "https://example.com/firmware/1.0.0.bin" }
}
```
