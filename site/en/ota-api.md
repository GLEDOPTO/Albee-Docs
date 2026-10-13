# OTA API
> Firmware: Albee v2.0.4 or later ｜ Audience: Developer


> End-user note: you don't need the server to upgrade the firmware — upload a `.ota` file via the device's built-in web page. See the [Local OTA Upgrade Guide](local-ota.md).

## Overview

This API handles device OTA (Over-The-Air) upgrade requests. The device sends its device information and current firmware version, and the server returns the latest firmware version and a download link (if an update is available).

## Request Method

**POST** `https://api.tenclass.net/xiaozhi/ota/` (path `/xiaozhi/ota/`)

The device sends the headers below **unconditionally**; it uses POST with a body only when the system-info JSON is non-empty, otherwise GET (no body).

## Request Headers

- `Device-Id`: unique device identifier (required). Note: with `CONFIG_ROBOT_IDENTITY_RESET=y` enabled, this firmware reports a **randomized persistent identity MAC**, not necessarily the hardware MAC
- `Client-Id`: unique client identifier, UUID v4 (required)
- `User-Agent`: client name and version number (required, e.g., `esp-box-3/1.5.6`)
- `Accept-Language`: current language of the client (always sent, e.g., `zh-CN`)
- `Activation-Version`: activation version (`1` for devices without a serial number; `2` for devices with one)
- `Serial-Number`: device serial number (**sent only by devices that have one**, in which case `Activation-Version` is `2`; the two headers never appear as the `1` + `Serial-Number` combination in real traffic)

## Request Body

| Field | Description |
|---|---|
| `application` | firmware version info (required): `version`, `name`, `compile_time`, `idf_version`, etc. |
| `mac_address` | MAC address (optional) |
| `chip_model_name` | chip model, e.g., `esp32s3` (optional) |
| `board` | board info (required): `type`, `name`, `ssid`, `rssi`, `channel`, `ip`, `mac`, etc. |

## Full ESP32 Request Example

```http
POST /xiaozhi/ota/ HTTP/1.1
Host: api.tenclass.net
Content-Type: application/json
User-Agent: xingzhi-cube/1.0.1
Device-Id: 11:22:33:44:55:66
Client-Id: 7b94d69a-9808-4c59-9c9b-704333b38aff
Accept-Language: zh-CN
Activation-Version: 2
Serial-Number: xxxxxxxx

{
  "application": { "version": "1.0.1", "name": "xingzhi-cube", "compile_time": "...", "idf_version": "5.4.3", "elf_sha256": "..." },
  "board": { "type": "xingzhi-cube", "name": "xingzhi-cube", "ssid": "Home", "rssi": -55, "channel": 6, "ip": "192.168.1.50", "mac": "11:22:33:44:55:66" }
}
```

## Response Example

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

**Last modified:** 2026-10-13
