# Albee Desktop Robot FAQ

> Firmware: Albee v2.0.4 or later ｜ Audience: End user

Jump to a section: [Buttons and controls](faq.md?id=_1-buttons-and-controls) · [Network](faq.md?id=_2-network) · [Voice and conversation](faq.md?id=_3-voice-and-conversation) · [Lights and motion](faq.md?id=_4-lights-and-motion) · [Account and activation](faq.md?id=_5-account-and-activation) · [Upgrade and troubleshooting](faq.md?id=_6-upgrade-and-troubleshooting)

## 1. Buttons and controls

**Q: How many buttons does Albee have, and what do they do?**

A: Two physical buttons plus one touch area. Long-press the power button for 3 s to turn Albee on or off. The function button: single-click starts or ends a conversation round (and stops a ringing alarm), double-click toggles real-time barge-in, long-press for 10 s runs a factory reset. The touch control supports single and double taps and also stops a ringing alarm. See [Device Activation Guide · Buttons and Controls](device-activation.md?id=part-1-buttons-and-controls).

**Q: How do I perform a factory reset?**

A: Long-press the function button for 10 s. The device erases Wi-Fi credentials, alarms, light groups and every other user setting, then reboots automatically; Wi-Fi must be configured again after the reboot. **Avoid pressing it by accident** (holding the button down triggers it).

## 2. Network

**Q: How do I re-configure or switch Wi-Fi?**

A: Restart Albee, then short-press the function button once while the blue LED is blinking during the Wi-Fi connection phase — you will hear a prompt tone and Albee re-enters provisioning mode. It also re-enters provisioning automatically after three failed connection attempts. For switching between saved networks or scanning for a new one, see the [Change Network Guide](change-network.md).

**Q: It never connects to Wi-Fi after power-on. What should I do?**

A: No need to power-cycle — just **single-click the function button** to re-enter provisioning mode; the device also re-enters provisioning automatically after three failed connection attempts. Other options (switch saved networks, scan and join a new one) are in the [Change Network Guide](change-network.md).

**Q: How do I find the device IP address?**

A: See [Find the Device IP Address](check-device-ip.md) — ask by voice, check the router admin page, or read the serial log.

## 3. Voice and conversation

**Q: How do I adjust the volume?**

A: Just say "set the volume to 50" or "turn the volume up a bit" (1–100%); you can also use the MCP tool `set_volume` — see the [MCP Usage Guide · Tool Catalog](mcp-usage.md?id=tool-catalog).

**Q: Can it play music?**

A: Yes, though copyright limits the catalogue to test tracks, user-submitted songs and some children's songs.

**Q: Does it support Bluetooth?**

A: Not at the moment.

**Q: Can I change the wake word?**

A: Not at the moment — the default wake word is "Hi Albee".

**Q: Can I change the voice?**

A: Yes. Console → role configuration → switch the voice; you can preview before saving. See [XiaoZhi Console Configuration Guide · Set the Voice](xiaozhi-console.md?id=_2-set-the-voice).

**Q: Can it recognize and remember who I am?**

A: Yes. Console → Agent → voiceprint recognition — see [XiaoZhi Console Configuration Guide · Voiceprint Recognition](xiaozhi-console.md?id=_6-voiceprint-recognition).

**Q: Can I clone my own voice?**

A: Yes — currently in public beta.

**Q: Does it support GPT or other LLMs?**

A: Not by default. Completing [Developer Authentication](developer-auth.md) unlocks Qwen3, full DeepSeek, Doubao, GLM and more.

Alternatively, you can run your own server and plug in other models — see [Related open source projects](README.md?id=related-open-source-projects).

**Q: Can I run my own server?**

A: Yes. The XiaoZhi communication protocol is open and the community maintains server implementations in Python, Java, Go and more — deploy one on your own computer or a cloud instance to plug in the model of your choice. Start with [Related open source projects](README.md?id=related-open-source-projects) and the [WebSocket protocol document](websocket.md).

## 4. Lights and motion

**Q: Can I control the lights at home by voice?**

A: Yes — 4 RF groups and 4 WLED groups. See the [Lighting Control Guide](lighting-control.md); for Home Assistant, see the [Home Assistant Integration Guide](home-assistant.md).

**Q: The walking posture looks off / the legs are misaligned?**

A: The servo reset position may be slightly off. Use `http://<device-ip>/robot` to trim each of the four servos by ±1° — see the [Servo Calibration Guide](servo-calibration.md).

## 5. Account and activation

**Q: The SMS verification code never arrives?**

A: Delivery normally takes under 5 minutes (allow up to 10 minutes for international numbers). Check that the number is active, has credit, and that no security app is blocking the message.

**Q: I forgot my password or username?**

A: See [Account and Device Help](account-help.md).

**Q: The device is already bound to another account?**

A: Contact support by email to unbind it — see [Account and Device Help](account-help.md).

## 6. Upgrade and troubleshooting

**Q: How do I upgrade the firmware?**

A: Upload an `.ota` file through the built-in web page — no computer flashing required. See the [Local OTA Guide](local-ota.md).

**Q: The device freezes or reboots on its own?**

A: Follow the [Freeze / Reboot Reporting Guide](problem-feedback.md) to collect the boot reason and logs, then email them to support.

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com

---

**Last modified:** 2026-10-10
