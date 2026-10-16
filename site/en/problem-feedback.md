# Device Freeze or Reboot Feedback Guide
> Firmware: Albee v2.0.5 ｜ Audience: End user


If your device freezes or reboots unexpectedly, please send an email to [service@gledopto.com](mailto:service@gledopto.com) with the following information:

1. **What was happening at the time**: What state was the device in? What were you doing?
2. **Boot reason**: Get the device IP address (see [Find the Device IP Address](check-device-ip.md)), then visit `http://<device-ip>/info` in a browser, check the boot reason, and provide it (see the example below). Note: your phone or computer must be on the same local network as Albee. **When providing the boot reason screenshot, do not restart or upgrade the device — you need to visit this page as soon as possible after the freeze/reboot to capture the information.**

<img src="assets/img/problem-feedback/1.png" width="560">

3. **Run logs (if available)**: If you have a serial terminal tool on your computer, connect Albee with a Type-C cable and check the device run logs. If you find any error messages, please include them as well to help troubleshoot the problem.

---

**Last modified:** 2026-10-09

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com
