# Built-in Web Console Overview

> Firmware: Albee v2.0.4 or later ｜ Audience: End user

Once Albee is online it serves a set of web pages on your local network. You can manage the robot straight from a phone or computer browser — no app required. This page is the entry point for all of them.

## 1. Prerequisites

1. Albee is activated and connected to Wi-Fi
2. Your phone or computer is on the same Wi-Fi (same LAN)
3. You know the device IP address — see [Find the Device IP Address](check-device-ip.md)
4. Open `http://<device-IP>/<page>`, for example `http://192.168.1.50/light`

## 2. Pages at a glance

| URL | Purpose | Details |
| --- | --- | --- |
| `http://<device-IP>/` | Home: device overview and entries to each function | — |
| `http://<device-IP>/light` | Lighting control: RF pairing and grouping, WLED scanning and grouping, group on/off | [Lighting Control Guide](lighting-control.md) |
| `http://<device-IP>/network` | Switch between saved Wi-Fi networks, scan and join a new one | [Change Network Guide](change-network.md) |
| `http://<device-IP>/led` | Change the head LED ring effect per device state | [Head LED Effects Guide](head-led-effects.md) |
| `http://<device-IP>/robot` | Servo calibration: ±1° trim for the four servos | [Servo Calibration Guide](servo-calibration.md) |
| `http://<device-IP>/info` | Device info: MAC address, firmware version, boot reason | [How to Check the MAC Address](check-mac-address.md) |
| `http://<device-IP>/update` | Local OTA: upload an `.ota` file to upgrade firmware | [Local OTA Guide](local-ota.md) |
| `http://<device-IP>/alarm` | Alarm / reminder management | [Alarm & Reminder Guide](alarm-reminder.md) |
| `http://<device-IP>/settings` | Device settings | — |
| `http://<device-IP>/foot` | Foot-sensor debugging | — |

> [!NOTE]
> `/robot` (motion control and servo calibration) and `/foot` (foot-sensor debugging) are gated by the build option `enable web robot control`, which is **enabled by default**; the two pages are only unavailable if you disabled the option when compiling your own firmware. All other pages are unaffected.

## 3. FAQ

- **Page won't open:** check that you are on the same LAN and the IP has not changed; AP isolation on the router blocks access between devices.
- **Page says activation is required:** an unactivated device only serves provisioning pages — complete [Device Activation](device-activation.md) first.
- **My change didn't take effect:** LED effect and network changes apply immediately; console-side settings (role, voice, model) only apply after restarting the device.
- **Upgrade failed:** make sure you upload an `.ota` file, not a `.bin`, and keep the device powered during the process — see the [Local OTA Guide](local-ota.md).

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com

---

**Last modified:** 2026-10-13
