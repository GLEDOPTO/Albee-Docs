# ha-mcp-for-xiaozhi操作指南

> 适用固件：Albee v2.0.4 及以上 ｜ 适用对象：开发者

ha-mcp-for-xiaozhi官方文档：[ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/blob/main/README.en.md)

## 如何安装

> [!IMPORTANT]
>
> 确保 Home Assistant 中安装了 HACS

1. 打开 HACS，搜索 xiaozhi 或 ha-mcp-for-xiaozhi

<img src="../assets/img/ha-mcp-for-xiaozhi/1.png">

2. 下载组件

<img src="../assets/img/ha-mcp-for-xiaozhi/2.png"> 

3. 重启 Home Assistant

4. 依次点击：设置 -> 设备与服务 -> 添加集成 -> 搜索“MCP” > 查找 Xiaozhi 的 MCP 服务器

<img src="../assets/img/ha-mcp-for-xiaozhi/3.png">

5. 点击"下一步"，填写小智 MCP 接入点地址，查看[如何获取MCP接入点地址](如何获取MCP接入点地址.md)


<img src="../assets/img/ha-mcp-for-xiaozhi/4.png">

<img src="../assets/img/ha-mcp-for-xiaozhi/5.png">

配置完成！等一下，去小智的接入点页面，点击刷新查看

<img src="../assets/img/ha-mcp-for-xiaozhi/6.png">

### 调试说明

1.暴露的工具取决于你公开给Homeassistant语音助手的实体的种类

```
设置 -> 语音助手 -> 公开
```

<img src="../assets/img/ha-mcp-for-xiaozhi/7.png">

2.尽量使用最新版本的homeassistant，单单看5月版本跟3月版本提供的工具就有明显差异

3.调试时未达到预期，优先看小智的聊天记录，看看小智对这句指令如何处理的，是否有调用homeassistant的工具。目前已知比较大的问题是灯光控制和音乐控制会和内置的屏幕控制、音乐控制逻辑冲突，需要等下个月虾哥服务器支持内置工具选择后可解。

4.如果流程正确的调用了ha内置的function，可以打开本插件的调试日志再去观测实际的执行情况

## 常见问题

- **MCP集成错误**：需要确保HomeAssistant是最新的版本

---

**文档最新修改时间：** 2026-10-13