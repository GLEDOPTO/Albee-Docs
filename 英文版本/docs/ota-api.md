# OTA API

## Overview

This API handles device OTA (Over-The-Air) upgrade requests. The device sends its device information and current firmware version, and the server returns the latest firmware version and a download link (if an update is available).

## Request Method

**POST** `/api/ota/`

## Request Headers

- `Device-Id`: Unique device identifier (required, use the MAC address)
- `Client-Id`: Unique client identifier, UUID v4 (required)
- `User-Agent`: Client name and version number (required, e.g., `esp-box-3/1.5.6`)
- `Accept-Language`: Current language of the client (optional, e.g., `zh-CN`)

## Request Body

| Field | Description |
|---|---|
| `application` | Object containing the device's current firmware version information (required) |
| `mac_address` | MAC address (optional) |
| `chip_model_name` | Chip model, e.g., `esp32s3` (optional) |
| `board` | Board type, name, ssid, rssi (required) |

## Full ESP32 Request Example

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

## Response Example

```json
{
  "mqtt": { "endpoint": "mqtt.example.com", "client_id": "..." },
  "websocket": { "url": "wss://api.tenclass.net/xiaozhi/v1/", "token": "..." },
  "server_time": { "timestamp": 1633024800000 },
  "firmware": { "version": "1.0.0", "url": "https://example.com/firmware/1.0.0.bin" }
}
```

---

**Last modified:** 2026-09-10
