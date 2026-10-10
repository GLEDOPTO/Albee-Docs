# Network Change Guide
> Firmware: Albee v2.0.4 or later ｜ Audience: End user


## Method 1: Switch via the Button

1. Restart the device.

2. While the LED on the head shows a blue scrolling/flowing effect (or within 3 seconds after the restart), single-click the function button (Function Button) once.

> [!TIP]
> If Wi-Fi never connects after power-on, you don't need to power-cycle — just single-click the function button once to re-enter provisioning mode.

   <img src="../../assets/img/change-wifi/2.png" width="480">

## Method 2: Switch to a Saved Network via the Web Page

1. Make sure the device is activated and connected to the network.
2. Find the device IP address (see [Find the Device IP Address](./check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).
3. Visit `http://<device-ip>/network` in a browser.
4. Find **SWITCH NETWORK** and click the **Switch** button of a network other than the currently connected one.

<img src="../../assets/img/change-wifi/1.png" width="480">



## Method 3: Join a New Network (Scan)

1. Make sure the device is activated and connected to the network.
2. Find the device IP address (see [Find the Device IP Address](./check-device-ip.md)), then connect your phone or computer to the same Wi-Fi (same local network).
3. Visit `http://<device-ip>/network` in a browser.
4. Click the **Scan** button to scan manually.
5. Wait for the results to appear in the drop-down list.
6. Select a network. Password box rules:

   - Open network: no password needed.
   - Saved network: leave it empty = use the stored password; enter a new password = overwrite the old one (this is the only way to handle a router whose password has been changed).
   - Brand-new network: password required.
7. Click **Switch & Reboot**.

<img src="../../assets/img/change-wifi/3.png" width="480">

---

**Last modified:** 2026-10-09
