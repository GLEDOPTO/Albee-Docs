# 如何查看MAC地址
> 适用固件：Albee v2.0.4 及以上 ｜ 适用对象：普通用户


##  一、通过网页获取

1. 确保设备已激活已联网

2. 获取设备 IP 地址（见[获取设备 IP 地址](./获取设备IP地址.md)），然后用手机或电脑连接同一个 Wi-Fi（确保同一局域网）

3. 通过浏览器访问：http://<机器人IP>/info

   <img src="../../assets/img/check-mac-address/1.png" width="480">

## 二、通过串口调试软件查看

可以使用串口调试软件，网站有很多，比如：Tera Term、CoolTerm等等

1. 将Albee通过Type-C数据线连接到电脑（请确认已开机）。选择对应的 COM 口，点击**打开串口**，波特率选择115200，其它保持默认。

2. 在串口日志中，找到 `wifi:mode : sta ( ... )` —— 该行显示的值（下方截图中蓝色高亮部分）即为 MAC 地址。

<img src="../../assets/img/check-mac-address/2.png" width="560">

---

**文档最新修改时间：** 2026-10-09
