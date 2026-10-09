# Home Assistant Integration Guide

You can integrate Home Assistant through MCP plugins. Two MCP plugins are recommended below.

## 1. HA MCP for XiaoZhi

### Description

1. Home Assistant itself acts as an MCP server and connects directly to the XiaoZhi server via the WebSocket protocol, without the need for a proxy.

2. Select multiple API groups (Home Assistant's built-in Intent APIs and user-configured MCP servers) in one entity and proxy them to XiaoZhi.

3. Supports configuring multiple entities at the same time.

### Repository & Documentation

Please see: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/blob/main/README.en.md)

## 2. Home MCP

### Description

Home-MCP is a smart-home integration server based on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). It provides AI assistants with standardized Home Assistant device control and data access. Through the MCP protocol, an AI assistant can interact seamlessly with the Home Assistant platform — controlling smart-home devices, querying states, analyzing data, and managing automations.

### Repository & Documentation

Please see: [Home MCP](https://github.com/shenjingnan/home-mcp)

---

**Last modified:** 2026-09-10
