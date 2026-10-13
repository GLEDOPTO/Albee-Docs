# ha-mcp-for-xiaozhi Guide

> Firmware: Albee v2.0.4 or later ｜ Audience: Developer

Official documentation of ha-mcp-for-xiaozhi: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/blob/main/README.en.md)

## How to Install

> [!IMPORTANT]
>
> Make sure HACS is installed in your Home Assistant

1. Open HACS and search for xiaozhi or ha-mcp-for-xiaozhi

<img src="assets/img/ha-mcp-for-xiaozhi/1.png">

2. Download the component

<img src="assets/img/ha-mcp-for-xiaozhi/2.png">

3. Restart Home Assistant

4. Click through: Settings -> Devices & Services -> Add Integration -> search for "MCP" > find the Xiaozhi MCP server

<img src="assets/img/ha-mcp-for-xiaozhi/3.png">

5. Click "Next" and fill in the XiaoZhi MCP access-point address — see [How to Get the MCP Access-Point Address](mcp-access-point-address.md)

<img src="assets/img/ha-mcp-for-xiaozhi/4.png">

<img src="assets/img/ha-mcp-for-xiaozhi/5.png">

Configuration done! Wait a moment, then open the access-point page on the XiaoZhi console and click refresh to check

<img src="assets/img/ha-mcp-for-xiaozhi/6.png">

### Troubleshooting Notes

1. The exposed tools depend on which kinds of entities you expose to the Home Assistant voice assistant

```
Settings -> Voice assistants -> Expose
```

<img src="assets/img/ha-mcp-for-xiaozhi/7.png">

2. Use the latest version of Home Assistant whenever possible — even between the May and March builds, the tools offered differ noticeably

3. If things do not behave as expected while debugging, check XiaoZhi's chat log first: see how it handled the command and whether it called a Home Assistant tool. The biggest known issue so far: light control and music control conflict with the built-in screen-control and music-control logic. This should be resolved once the server-side built-in tool selection ships next month.

4. If the flow does call the HA built-in functions correctly, enable this integration's debug log to observe what actually executes

## FAQ

- **MCP integration error**: make sure Home Assistant is up to date

---

**Last modified:** 2026-10-13
