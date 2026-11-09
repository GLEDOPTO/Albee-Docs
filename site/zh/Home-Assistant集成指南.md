# Home Assistant 集成指南
> 适用固件：Albee v2.0.9 ｜ 适用对象：开发者

你可以通过 MCP 插件接入 Home Assistant。下面推荐几个MCP 插件。

## 1.XiaoZhi-MCP-HA

### 简介

一个 Home Assistant 定制集成（HACS），通过 MCP（模型上下文协议）将 Xiaozhi ESP32 AI 聊天机器人连接到 Home Assistant。

### 仓库与文档

请参见：[xiaozhi-mcp-ha](https://github.com/mac8005/xiaozhi-mcp-ha)

## 2. HA MCP for XiaoZhi

### 简介

1. Home Assistant 自身作为 MCP 服务器，通过 WebSocket 协议直接连接小智服务器，无需代理。

2. 在一个实体中选择多个 API 分组（Home Assistant 内置的 Intent API 和用户配置的 MCP 服务器），并代理给小智。

3. 支持同时配置多个实体。

### 仓库与文档

请参见：[ha-mcp-for-xiaozhi操作指南](ha-mcp-for-xiaozhi操作指南.md)（安装与配置教程），仓库与官方文档见 [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/blob/main/README.en.md)

## 3. Home MCP

### 简介

Home-MCP 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的智能家居集成服务器。它为 AI 助手提供标准化的 Home Assistant 设备控制与数据访问能力。通过 MCP 协议，AI 助手可以与 Home Assistant 平台无缝交互 —— 控制智能家居设备、查询状态、分析数据、管理自动化。

### 仓库与文档

请参见：[Home MCP](https://github.com/shenjingnan/home-mcp)

---

**文档最新修改时间：** 2026-11-09
