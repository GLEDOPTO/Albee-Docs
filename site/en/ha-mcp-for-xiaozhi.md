# ha-mcp-for-xiaozhi Guide

> Firmware: Albee v2.0.5 ｜ Audience: Developer

Official documentation of ha-mcp-for-xiaozhi: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/blob/main/README.en.md)

## How to Install

### Online Installation

> [!IMPORTANT]
>
> Make sure HACS is installed in your Home Assistant

1. Open HACS and search for xiaozhi or ha-mcp-for-xiaozhi

<img src="assets/img/ha-mcp-for-xiaozhi/1.png">

2. Download the component

<img src="assets/img/ha-mcp-for-xiaozhi/2.png">

3. Restart Home Assistant

### Offline Installation

1. Visit: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi)
2. Pick the version you want

<img src="assets/img/ha-mcp-for-xiaozhi/8.png">

3. Click download

<img src="assets/img/ha-mcp-for-xiaozhi/9.png">

4. Extract the archive and upload the ws_mcp_server folder to homeassistant/custom_components

> [!NOTE]
>
> You can upload it with the File browser add-on; add it under Settings -> Add-ons

<img src="assets/img/ha-mcp-for-xiaozhi/10.png">

5. Restart Home Assistant

## Enable the Integration

1. Click through: Settings -> Devices & Services -> Add Integration -> search for "MCP" > find the Xiaozhi MCP server

<img src="assets/img/ha-mcp-for-xiaozhi/3.png">

2. Click "Next" and fill in the XiaoZhi MCP access-point address — see [How to Get the MCP Access-Point Address](mcp-access-point-address.md)


<img src="assets/img/ha-mcp-for-xiaozhi/4.png">

<img src="assets/img/ha-mcp-for-xiaozhi/5.png">

3. Configuration done! Wait a moment, then open the access-point page on the XiaoZhi console and click refresh to check

<img src="assets/img/ha-mcp-for-xiaozhi/6.png">

## How to Use

Once the restart finishes, talk to Albee to control your home by voice, for example:

~~~~
"Show me the devices in Home Assistant"
"Turn on device x in Home Assistant"
~~~~

### Troubleshooting Notes

1. The exposed tools depend on which kinds of entities you expose to the Home Assistant voice assistant

```
Settings -> Voice assistants -> Expose
```

<img src="assets/img/ha-mcp-for-xiaozhi/7.png">

The "Voice assistants -> Expose" page:/n/n<img src="assets/img/ha-mcp-for-xiaozhi/11.png">

Example of the tools available after exposing entities:/n/n<img src="assets/img/ha-mcp-for-xiaozhi/12.png">

2. Use the latest version of Home Assistant whenever possible — even between the May and March builds, the tools offered differ noticeably

3. If things do not behave as expected while debugging, check XiaoZhi's chat log first: see how it handled the command and whether it called a Home Assistant tool. The biggest known issue so far: light control and music control conflict with the built-in screen-control and music-control logic. This should be resolved once the server-side built-in tool selection ships next month. From firmware v2.0.5 you can also disable the conflicting built-in tools (e.g. the light-group tools) directly on the device web page `http://<device-ip>/mcp`, so XiaoZhi falls back to the Home Assistant tools; toggles take effect in a new conversation (see the [MCP Usage Guide](mcp-usage.md)).

4. If the flow does call the HA built-in functions correctly, enable this integration's debug log to observe what actually executes

## FAQ

- **MCP integration error**: make sure Home Assistant is up to date
- **Few tools available**: you need to expose your entity devices

## Notes

This project ships with some built-in MCP tools — for example the lighting-control MCP tool (see the [Lighting Control Guide](lighting-control.md)) — so when controlling Home Assistant lights by voice through Albee, you need to specify that you mean the device in HASS

---

**Last modified:** 2026-10-16
