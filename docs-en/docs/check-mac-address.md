# How to View the MAC Address
> Firmware: Albee v2.0.5 ｜ Audience: End user


## Method 1: Via the Web Page

1. Make sure the device is activated and connected to the network.

2. Find the device IP address (see [Find the Device IP Address](./check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).

3. Visit `http://<device-ip>/info` in a browser.

   <img src="../../assets/img/check-mac-address/1.png" width="480">

## Method 2: Via a Serial Terminal Tool

You can use a serial terminal tool — there are many available, such as Tera Term, CoolTerm, etc.

1. Connect Albee to your computer with a Type-C cable (make sure it is powered on). Select the corresponding COM port, click **Open Serial Port**, set the baud rate to 115200, and keep the other settings at their defaults.

2. In the serial log, find the line `wifi:mode : sta ( ... )` — the value shown there (highlighted in blue in the screenshot below) is the MAC address.

<img src="../../assets/img/check-mac-address/2.png" width="560">

---

**Last modified:** 2026-10-09
