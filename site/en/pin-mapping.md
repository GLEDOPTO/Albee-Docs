# Pin Mapping
> Firmware: Albee v2.0.9 ｜ Audience: Developer


Complete GPIO pin mapping for the Albee desktop robot (ESP32-S3), covering every peripheral, sensor, and button on the board.

## GPIO Pin Table

| GPIO | Group | Function |
| --------- | ------------------- | ------------------------------------------------------ |
| IO7 | Power Management | Battery voltage sampling (12-bit ADC, 3.0–4.2 V calibration curve) |
| GPIO21 | Power Management | Charging detection (low level = charging) |
| GPIO45 | Power Management | GEK100 power-module control (low level = normal supply) |
| GPIO16 | Power Management | Servo + foot-sensor power-rail switch (high level = powered) |
| GPIO0 | Button Inputs | Function button (Function Button, i.e. the BOOT button), single-click / double-click |
| GPIO4 | Button Inputs | touch control (single-click / double-click) |
| GPIO1 | I2C Bus | I2C SDA — SC7U22 6-axis IMU and 4 × LTR-553 foot sensors |
| GPIO2 | I2C Bus | I2C SCL — same bus |
| GPIO5 | 6-axis IMU | SC7U22 INT1 data-ready (push-pull, active high; polled by the IMU task during sleep instead of being wired as an interrupt) |
| GPIO3 | LCD Display | LCD backlight PWM |
| GPIO9 | LCD Display | SPI CLK (shared with the 2.4 GHz RF chip) |
| GPIO10 | LCD Display | SPI MOSI (shared with the 2.4 GHz RF chip) |
| GPIO11 | LCD Display | LCD reset |
| GPIO12 | LCD Display | LCD CS |
| GPIO46 | LCD Display | LCD D/C |
| GPIO8 | 2.4 GHz RF chip | 2.4 GHz RF chip SPI MISO |
| GPIO13 | 2.4 GHz RF chip | 2.4 GHz RF chip CS |
| GPIO41 | 2.4 GHz RF chip | 2.4 GHz RF chip reset |
| GPIO42 | 2.4 GHz RF chip | 2.4 GHz RF chip PKT (data ready) |
| GPIO14 | 2.4 GHz RF chip | 2.4 GHz RF chip TX/RX enable (TXEN) |
| GPIO17 | Servos | Left-leg servo |
| GPIO18 | Servos | Left-foot servo |
| GPIO38 | Servos | Right-foot servo |
| GPIO39 | Servos | Right-leg servo |
| GPIO15 | LED Ring | WS2811 addressable RGB LED data |
| GPIO47 | Voice Chip | VB6824 codec TX |
| GPIO48 | Voice Chip | VB6824 codec RX |

## Notes

- **I2C bus (GPIO1/GPIO2)**: shared by the SC7U22 6-axis IMU (accelerometer + gyroscope, Mahony AHRS attitude fusion, outputs Euler angles and quaternions; detects standing / tilted / fallen / shaken states) and the four LTR-553 IR proximity sensors (two per foot, used for fall protection — hovering / grounded detection).
- **Shared SPI lines (GPIO9/GPIO10)**: the SPI clock and MOSI are shared between the ST7789 LCD and the 2.4 GHz RF chip; the two devices are distinguished by their separate CS lines (GPIO12 vs GPIO13).
- **LCD**: 1.54-inch 240×240 ST7789, used for the 21 GIF emoji expressions and 6 status animations (low battery / charging / clock / power-on / Wi-Fi / connection-error `cloud_slash`; the power-on animation is new in v2.0.5 and absent from old asset packages).
- **Wi-Fi**: provided by the ESP32-S3's on-chip 2.4 GHz radio (cloud chat, WLED control, mDNS) — no external pin involved.
- **Power**: the GEK100 power module supplies the system; the battery voltage is sampled via IO7 with a 3.0–4.2 V calibration table and low-battery auto shutdown.

---

**Last modified:** 2026-11-09
