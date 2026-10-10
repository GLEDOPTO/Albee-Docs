# Local OTA Upgrade Guide
> Firmware: Albee v2.0.4 or later ｜ Audience: End user


> Developer note: to trigger OTA upgrades from a server (backend integration), see the [OTA API](ota-api.md).

1. Make sure the device is activated and connected to the network.
2. Find the device IP address (see [Find the Device IP Address](check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).
3. Visit `http://<device-ip>/update` in a browser.
4. Click "Tap to choose a firmware file (.ota)".
5. Upload the `Albee_xxx.ota` file.
6. Click **Upload & Flash**.

<img src="../assets/img/local-ota/1.png" width="560">

---

**Last modified:** 2026-10-09
