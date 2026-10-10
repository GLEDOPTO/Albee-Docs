# Head LED Effects Change Guide
> Firmware: Albee v2.0.4 or later ｜ Audience: Developer


For what each effect means, see [Device States & LED Indicators](device-led-states.md) — each effect corresponds to a different device state.

## Method 1: Via the Web Page

1. Make sure the device is activated and connected to the network.
2. Find the device IP address (see [Find the Device IP Address](check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).
3. Visit `http://<device-ip>/led` in a browser.

As shown below:

<img src="../assets/img/overhead-led/2.png" width="480">

## Method 2: Via Code

> **Intended audience**: developers who want to change factory behavior, add new effects, or adjust state mapping.
>
> Prerequisite: download the source code and set up the build environment — see the [Firmware Compilation Tutorial](compilation-tutorial.md).

### 2.1 Effect Pipeline Overview

| Stage       | Location                                           | Responsibility                               |
| ----------- | -------------------------------------------------- | -------------------------------------------- |
| State → slot| `led_config.cc` · `LedSlotFor()`                   | Maps `DeviceState` to `LedSlot`              |
| Slot defaults | `led_config.cc` · `kLedDefaults[]`               | Factory effect / color / pace                |
| Config I/O  | `led_config.cc` · `LedConfig`                      | NVS persistence, range validation, revision  |
| Effect names | `led_config.cc` · `kEffectNames[]`               | Sent via the API; the settings-page drop-down is built from it |
| Effect dispatch | `circular_strip.cc` · `CircularStrip::ApplySlot()` | Calls the animation based on the `effect` field |
| Animations  | `circular_strip.cc`                                | Frame-by-frame drawing (frame timer callback) |

The front end (`pages/led.html`) renders entirely from what the API returns — **changing, adding effects or slots requires no front-end changes**.

### 2.2 Change the Default Look of a State

Edit `led_config.cc` · `kLedDefaults[]`. The array rows correspond one-to-one with the `LedSlot` enum order:

| Index | 0        | 1                | 2    | 3          | 4         | 5        | 6         | 7          |
| ----- | -------- | ---------------- | ---- | ---------- | --------- | -------- | --------- | ---------- |
| Slot  | starting | wifi_configuring | idle | connecting | listening | speaking | upgrading | activating |

Each row is a `LedStateConfig`: `{effect, mode, r, g, b, length, interval_ms}`. `r/g/b` are only used in `kCustom` mode; `length` is only used by Scroll.

Example — change Idle from "fade out" to "blue breathe, 2 s":

```cpp
// the idle (index 2) row in kLedDefaults
{LedEffect::kBreathe, LedColorMode::kAutoBlue, 0, 0, 0, 3, 2000},
```

After changing, also update the "value-by-value" comment above `kLedDefaults[]`.

**How changes take effect falls into two categories (common pitfall)**:

- **Non-locked slots**: devices that already have the slot's keys (`st{i}` / `si{i}`) in NVS **keep using the NVS values** and never see the new default. To apply it, click Reset on the web page's "Indicator LED" card (which calls `/api/led/reset` → `LedConfig::ResetToDefaults()`), or erase the `led` namespace.
- **Locked slots** (`starting` / `wifi_configuring` / `upgrading`): `LedConfig::LoadLocked()` forces effect / length / interval back to `kLedDefaults` on every boot, so code changes **take effect immediately**; colors are still read from NVS.

### 2.3 Change the State → Slot Mapping

`led_config.cc` · `LedSlotFor()` — adding a case lets a state reuse an existing effect:

```cpp
case kDeviceStateFatalError: return kLedSlotListening;
```

(By default Unknown / FatalError return -1, no effect.) If you want an **independent** configuration for that state, add a new slot as described below.

### 2.4 Add a New Slot

To split two states into two independent configurations (e.g. give `AudioTesting` its own, separate from `Listening`), 6 places must be changed together, all in `led_config.h` / `led_config.cc`:

1. `led_config.h` · the `LedSlot` enum — **add new slots at the end, before `kLedSlotCount`**; all existing NVS keys remain unaffected;
2. `led_config.cc` · `kSlotKeys[]` — the key names for NVS and JSON;
3. `led_config.cc` · `kSlotLabels[]` — the display names on the settings page;
4. `led_config.cc` · `kLedDefaults[]` — add a row;
5. `led_config.cc` · `kLedSlotLocked[]` — add an entry;
6. `led_config.cc` · `LedSlotFor()` — add a case.

Zero front-end and API changes: `web_led_api.cc` iterates up to `kLedSlotCount` when outputting, and the page renders from the returned data.

### 2.5 Add a New Effect

Four steps in firmware, zero front-end changes:

1. **Enum**: add to `led_config.h` · `LedEffect` — it must go before `kCount`, and **must not be inserted in the middle**: NVS stores the numeric enum value, and inserting in the middle changes what existing stored values mean;
2. **Display name**: add an entry to `led_config.cc` · `kEffectNames[]`, aligned by index with the enum value; the order is the drop-down order on the settings page;
3. **Animation**: write the new animation in `circular_strip.cc` following `Breathe()` / `Scroll()`, with three conventions:
   - Start the frame timer with `StartStripTaskLocked(interval_ms, cb)` (the call site already holds `mutex_`), or `StartStripTask()` (locks automatically);
   - The animation phase variables (breathe brightness, scroll offset, etc.) **must be members of `CircularStrip`** (see the `blink_on_` group of declarations in `circular_strip.h`), not function-local `static` — the old implementation did exactly that, causing animations to resume from their previous phase on restart;
   - Frame callbacks run on the `strip_timer` esp_timer task and hold `mutex_`; `led_strip_refresh()` blocks synchronously on RMT transmission;
4. **Dispatch**: add a case to the switch in `CircularStrip::ApplySlot()`.

**Bit-width limit**: when slot configs are packed into NVS, effect occupies only 3 bits (see `PackSlot()` / `UnpackSlot()` in `led_config.cc`); 6 are currently used (values 0–5), so **at most 2 more can be added** (values 6, 7); beyond that you must widen the effect bits after `kShiftEffect` and update both masks, `kSchemaVersion`, and the compatibility migration.

### 2.6 Fine-tune Existing Animations Frame by Frame

All in `circular_strip.cc`:

- Breathe step: the `* 3` inside `Breathe()` (bigger = faster);
- Rainbow speed: `step = 360000 / 24 / interval_ms` inside `Rainbow()` (≈ 24 frames per revolution);
- Scroll advance: the offset increment at the end of `Scroll()`;
- Blink duty cycle: the on/off flip in `Blink()`.

Also note that the first parameter of `Breathe(low, high, …)` is currently unused; it actually scales by `high` only.

### 2.7 Validation Range Constants

In `led_config.h`: `kLedIntervalMinMs` / `kLedIntervalMaxMs` (pace 50–5000 ms), `kLedScrollLenMin` / `kLedScrollLenMax` (Scroll lit segment 1–7 LEDs), `kLedBrightnessMin` / `kLedBrightnessMax` (brightness percent 0–100). API validation (`LedConfig::ValidateSlotPatch()`) and NVS reads share these values — change them once and the whole chain follows.

### 2.8 Build & Take Effect

- Only changed existing files → `idf.py build flash`;
- **Added a `.cc` file** → run `idf.py reconfigure` first (sources are collected by GLOB and are not rescanned automatically);
- Changed the NVS packing format → bump `kSchemaVersion` in `led_config.cc` and consider migrating old values;
- Existing devices should see new defaults → Reset on the web page, or erase the `led` namespace.

### 2.9 Pitfall Checklist

- `main/boards/gledopto-robot/light/` (`rf_light` / `wled_light`) drives **external RF / WLED lights** and has nothing to do with the on-board indicator LEDs — don't edit the wrong directory;
- `main/led/` is board-common code: by convention `led_config.h` must not include `board.h` / `application.h` (every board compiles it);
- To make a locked slot editable → change `kLedSlotLocked[]`; once unlocked, the preview restriction in `PreviewSlot()` is lifted automatically;
- No manual animation restart needed after changing config at runtime: `LedConfig` bumps the revision on every successful write, and `CircularStrip::OnStateChanged()` redraws automatically on the next call.

---

**Last modified:** 2026-10-09
