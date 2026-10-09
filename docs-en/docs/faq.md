# Albee Desktop Robot FAQ

## Q1: How do I adjust Albee's volume?

**A:** Albee supports voice control for volume. Just tell Albee to set the volume to a specific level (1–100%), or simply say "turn the volume up / down a little". The volume can also be set via the MCP tool `set_volume` — see the [MCP Usage Guide · Tool Catalog](./mcp-usage.md#tool-catalog).

## Q2: How do I reconfigure or switch the Wi-Fi?

**A:** Restart Albee. While the blue LED is blinking during the Wi-Fi connection phase, short-press the **Function button** once and release — you will hear a prompt tone and Albee will re-enter Wi-Fi configuration mode.

Albee also re-enters Wi-Fi configuration mode automatically after failing to connect to the last configured Wi-Fi 3 times. For more ways to switch or join a network (switch to a saved network via the web page, scan and join a new one), see the [Network Change Guide](./change-network.md).

## Q3: Does Albee support music playback?

**A:** Yes — test music is supported. Due to copyright restrictions, the available tracks are limited to test songs, songs submitted by users, and some children's songs.

## Q4: Does Albee support Bluetooth?

**A:** Not currently.

The ESP32-S3 chip/module does support the BLE peripheral mode (it can only be connected to, not initiate connections), but the Albee project does not use it. If you need this feature, you can implement it by writing your own code.

## Q5: Can I change the wake word?

**A:** Not currently supported.

## Q6: Can I change the voice / timbre?

**A:** Yes. Go to the Albee web console — **Role Configuration** — to switch the role voice. You can preview the voices first, then submit to save the configuration. For detailed steps, see the [Console Configuration Guide · Set the Voice](./xiaozhi-console.md#2-set-the-voice).

Console: <https://xiaozhi.me/>

![Configure the role voice in the console](../../assets/img/faq/image-20260826092259737.png)

## Q7: Can Albee recognize and remember who I am by my voice?

**A:** Yes.

**How:** Go to the Albee web console → **Agent** → find **Voiceprint Recognition**. For detailed steps, see the [Console Configuration Guide · Voiceprint Recognition](./xiaozhi-console.md#6-voiceprint-recognition).

![Voiceprint recognition configuration](../../assets/img/faq/image-20260826092410518.png)

## Q8: Can I replace the voice with my own custom voice?

**A:** Supported — currently in public beta.

## Q9: Can Albee control other devices by voice?

**A:** Albee already supports the MCP protocol. See the [MCP Usage Guide](./mcp-usage.md) (full tool catalog) for details; for Home Assistant integration, see the [Home Assistant Integration Guide](./home-assistant.md).

## Q10: Does Albee support GPT or other large language models?

**A:** Not currently. If you want to use another LLM API or a self-hosted model, you need to implement your own server. To unlock more models (Qwen3 / DeepSeek full / Doubao / GLM, etc.), see [Developer Authentication](./developer-auth.md); for protocol details, see the [WebSocket protocol](./websocket.md) and the [MQTT+UDP protocol](./mqtt-udp.md).

Open-source repository: <https://github.com/78/xiaozhi>

## Q11: What should I do if the device freezes or reboots unexpectedly?

**A:** Please collect the fault information and report it to us — see the [Device Freeze or Reboot Feedback Guide](./problem-feedback.md).

## Q12: The robot walks incorrectly / the legs are at an angle — what should I do?

**A:** The servos' reset pose may have a slight deviation. Fine-tune the four servos by ±1° via the web page (`http://<device-ip>/robot`) — see the [Servo Calibration Guide](./servo-calibration.md).

---

**Last modified:** 2026-10-09
