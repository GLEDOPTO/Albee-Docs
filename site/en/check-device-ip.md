# Find the Device IP Address

> Firmware: Albee v2.0.4 or later ｜ Audience: End user

Opening any of Albee's built-in web pages (lighting control, network switching, LED effects, servo calibration, local update) requires knowing its IP address. Pick whichever of the three methods below suits you.

## Method 1: just ask (quickest)

Wake Albee (say "Hi Albee" or single-tap the function button), then say any of the following — it will speak the address and show it on screen:

- "What is your IP address?"
- "Announce your IP address"
- "Tell me your address"

## Method 2: check the router admin page

1. Sign in to your router's admin page (commonly `192.168.1.1` or `192.168.0.1`; check the label on the router)
2. Open **Connected devices** or the **DHCP client list**
3. The entry named **Albee** is the robot — the address shown next to it is its IP

> [!TIP]
> Bind that IP to the device MAC as a static assignment, so the address stays stable after reboots and the web pages keep working.

## Method 3: read the serial log

1. Connect Albee to your computer with a Type-C cable (the device must be powered on)
2. Open a serial terminal (Tera Term, CoolTerm, etc.), select the matching COM port, baud rate **115200**, leave everything else at defaults
3. Once the device joins Wi-Fi the log prints the following two lines — `192.168.0.171` is the device IP on your LAN:

```
I (11563) esp_netif_handlers: sta ip: 192.168.0.171, mask: 255.255.255.0, gw: 192.168.0.1
I (11563) WifiStation: Got IP: 192.168.0.171
```

> [!NOTE]
> Both lines show the same address, so either `sta ip:` or `Got IP:` works. If the log only shows `wifi:connected with CG001` with no `Got IP` line, Wi-Fi is associated but no address has been assigned yet — wait a moment or check the router's DHCP.

## FAQ

- **The page won't open:** make sure the phone or computer is on the same LAN (same Wi-Fi) as Albee, and that the router does not have AP isolation enabled.
- **It worked yesterday but not today:** the router most likely handed out a new IP — look it up again, then consider a static binding.
- **It doesn't answer when asked:** the device must be activated and online; there is no IP while it is in provisioning or connecting state — use method 2 or 3 instead.

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com

---

**Last modified:** 2026-10-10
