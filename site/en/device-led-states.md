# Device States & LED Indicators
> Firmware: Albee v2.0.5 ｜ Audience: Developer


## Part 1: State Overview

There are **11** `DeviceState` values, **9** of which have LED indicator behavior (`device_state.h`):

| DeviceState                   | Meaning              | LED                     |
| ----------------------------- | -------------------- | ----------------------- |
| `kDeviceStateUnknown`         | Unknown (initial)    | **None**                |
| `kDeviceStateStarting`        | Booting              | Yes                     |
| `kDeviceStateWifiConfiguring` | Wi-Fi setup (AP mode)| Yes                     |
| `kDeviceStateIdle`            | Idle                 | Yes                     |
| `kDeviceStateConnecting`      | Connecting to server | Yes                     |
| `kDeviceStateListening`       | Listening            | Yes                     |
| `kDeviceStateSpeaking`        | Speaking / playing   | Yes                     |
| `kDeviceStateUpgrading`       | OTA upgrade          | Yes                     |
| `kDeviceStateActivating`      | Activating           | Yes                     |
| `kDeviceStateAudioTesting`    | Audio test in setup  | Yes (shared with Listening) |
| `kDeviceStateFatalError`      | Fatal error          | **None**                |

As shown below:

<img src="assets/img/overhead-led/1.png" width="560">



## Part 2: State → Effect Mapping (Factory Defaults)

| # | Page name | States | Default effect | Default color |
| --- | --- | --- | --- | --- |
| 0 | Booting | `Starting` | Scroll | Blue |
| 1 | Wi-Fi setup | `WifiConfiguring` | Blink | Blue |
| 2 | Idle | `Idle` | Fade out | (color ignored) |
| 3 | Connecting | `Connecting` | Solid | Blue |
| 4 | Listening | `Listening`, `AudioTesting` | Solid | Red |
| 5 | Speaking | `Speaking` | Solid | Green |
| 6 | Firmware update | `Upgrading` | Blink | Green |
| 7 | Activating | `Activating` | Blink | Green |

Pace and editability per state:

| Page name | Slot key | Pace | Effect / pace editable |
| --- | --- | --- | --- |
| Booting | `starting` | 100 ms/frame, 3 LEDs on | 🔒 Locked |
| Wi-Fi setup | `wifi_configuring` | 500 ms | 🔒 Locked |
| Idle | `idle` | 50 ms/frame | Color only |
| Connecting | `connecting` | — | Editable |
| Listening | `listening` | — | Editable |
| Speaking | `speaking` | — | Editable |
| Firmware update | `upgrading` | 1000 ms | 🔒 Locked |
| Activating | `activating` | 500 ms | Editable |

Behavior notes:

- **Booting**: a 3-LED blue segment scrolls around the ring, advancing 1 LED per frame at a 100 ms frame period.
- **Wi-Fi setup**: blue 500 ms square-wave blink (on/off 500 ms each).
- **Idle**: halves the brightness of **whatever is currently displayed** every frame until fully off (50 ms/frame, roughly 0.4 s), so idle ends with the ring dark. This effect does not read the configured color.
- **Connecting**: solid blue.
- **Listening / AudioTesting**: solid red.
- **Speaking**: solid green.
- **Firmware update**: green 1000 ms blink. The pace is locked to 1 s for a **hardware reason** — `esp_ota_write` disables the flash cache in bursts, which also interrupts the interrupts driving RMT and esp_timer; a shorter interval would look "stuck" rather than "blinking".
- **Activating**: green 500 ms blink.

> Colors are scaled by the **global brightness** percentage (preset channel value = brightness% × 255 / 100; default 15% ≈ 38).

## Part 3: Effect Types

There are 6 in total, selectable on the settings page (except for locked slots):

| Effect     | Name     | Behavior                                                     |
| ---------- | -------- | ------------------------------------------------------------ |
| `kSolid`   | Solid    | A single flat color, constant on; the animation timer stops  |
| `kBlink`   | Blink    | Square wave between color / off; `interval_ms` is the half-period |
| `kFadeOut` | Fade out | Halves the current pixels' brightness every frame until off; **ignores the configured color**; the pace is fixed at 50 ms and not adjustable ("speed" is really the decay depth per step) |
| `kBreathe` | Breathe  | The configured color breathes 0 → brightest → 0 (step 3/frame, `interval_ms` is the frame period) |
| `kScroll`  | Scroll   | A lit segment of `length` LEDs (1–7) travels around the ring, advancing 1 LED per frame |
| `kRainbow` | Rainbow  | The full hue circle is spread evenly around the ring and rotates; `interval_ms` controls the speed (one revolution ≈ 24 frames; 50 ms fastest ≈ 1.2 s/rev) |

---

**Last modified:** 2026-10-09
