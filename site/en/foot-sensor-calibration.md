# Foot Sensor Calibration Guide
> Firmware: Albee v2.0.9 ｜ Audience: End user


> Why calibrate? Each of the robot's two feet has a set of distance sensors underneath, used to tell whether the surface below is the desk or a drop — this is what the fall protection relies on (automatically stopping or turning away at a table edge). Sensor readings vary from unit to unit, so every sensor is calibrated at the factory. If the material or colour of the desk changes (for example moving from a light desk to a dark one, or adding a tablecloth or glass mat), the calibrated thresholds may no longer match, which leads to misjudgement: the robot reports it is suspended while standing on the desk, or fails to detect a real table edge. In that case, recalibrate following this guide

## Calibration Steps

1. Make sure the device is activated and connected to the network.
2. Find the device IP address (see [Find the Device IP Address](check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).
3. Visit `http://<device-ip>/foot` in a browser.
4. Place the robot flat on **the surface it is normally used on** (the desk where it usually sits and walks), with all feet resting steadily on the surface — do not press down on or prop up any foot.
5. In the **Sensor Calibration** card, find the row "1 · Ground — flat on its working surface" and click **Sample** (① in the figure). The status shows `waiting for stability…` and then `sampling n/30` in turn; **keep the robot perfectly still** during this time. When done it shows ✓ followed by the readings of the four sensors.
6. Pick the robot up with both hands, hold it about **15 cm** in the air with a firm grip, find the row "2 · Air — held 15 cm airborne", click **Sample** (② in the figure), and again keep it still until sampling finishes.
7. Once both steps show ✓, the **Apply Calibration** button becomes clickable (③ in the figure) — click it to save the calibration. The page shows `Calibration applied` on success, and the badge at the top of the card reads **Calibrated**.

<img src="assets/img/foot_sensor/1.png" width="480">

The four rows at the bottom of the figure are the thresholds currently in effect for each sensor (susp / warn); these values update after a successful calibration.

**Notes:**

- Follow the on-page order — sample Ground first, then Air. Both steps must succeed before the calibration can be applied.
- After you click Sample for a step, the page waits up to 10 seconds for the readings to stabilise. If the robot keeps moving or your grip is not steady enough, the step fails with `cannot stabilise (10 s) — check placement / hold`; just click Sample again.
- When you click Apply, the device judges whether both samples are valid. All four sensors must **pass** before anything is saved. If any one fails, the page tells you which sensor and why (see the FAQ below); in that case **nothing is saved**, the previous calibration stays in effect, and you can resample after fixing the issue.
- While a step is being sampled (status shows `sampling n/30`), do not click other buttons — wait for the step to finish.

## Restoring the Default Thresholds

If the result after calibration is not satisfactory, you can undo it and restore the factory default thresholds: click **Reset Calibration** at the top right of the Sensor Calibration card and confirm the dialog. The page shows `Calibration erased`; the badge then reads **Default thresholds**, and you can recalibrate following the steps above at any time.

> Note: a factory reset does **not** erase the foot calibration data, but it does turn the fall-protection master switch back on. See the [FAQ](faq.md).

## FAQ

- **Apply Calibration stays greyed out**: both the Ground and Air steps must succeed (both show ✓) before you can apply. Check whether a step still shows `not sampled` or failed.
- **It says `l0 rejected: separation too low` (or l1 / r0 / r1)**: the gap between the suspended and grounded readings of that sensor is too small. Make sure the robot was held about 15 cm in the air during the Air sample and that both steps were sampled over the same working surface, then resample. If you have changed to a surface that differs a lot in material or colour, recalibrate on the new surface.
- **It says `noise floor too high`**: the suspended reading is too high. Redo the Air sample — lift the robot, hold it still for a second or two, and then click Sample.
- **It says `ground value too low`**: the grounded reading is too low. Redo the Ground sample and make sure all feet rest steadily on the surface.
- **It says `cannot stabilise (10 s)`**: the readings did not stabilise within 10 seconds. For the Ground step, make sure the robot is set down steadily on a desk that does not wobble; for the Air step, get a firm grip on the robot before clicking Sample.
- **It says `unstable foot link`**: some readings were invalid during sampling. Click Sample and try again; contact support if it keeps happening.
- **It says `sensors not ready (both feet offline?)`**: the device cannot read the foot sensors. Make sure the robot is awake (not in sleep mode) and try again; contact support if it persists.
- **The readings in the Foot Sensors card never change or show as stale**: you can click **Reset Sensors** in the Sensor Maintenance card further down the page. It restores both sensor boards to their factory defaults and re-initialises them — use it only when the readings are stuck.
- **The page says the device is sleeping and the calibration card is greyed out**: the foot sensors are powered off while the device sleeps, so calibration is unavailable. Wake the device as prompted and try again.
- **The page asks for a PIN**: when a web PIN lock is set on the device, unlock it first before calibrating.
- **It still does not stop at a table edge after calibration**: first confirm that Fall Protection at the top of the page shows **Enabled**. Then watch the Foot Sensors card: with the robot standing on the desk, all four sensors should show a green **Grounded**.

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com

---

**Last modified:** 2026-11-24
