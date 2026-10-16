# 本地OTA升级指南
> 适用固件：Albee v2.0.5 ｜ 适用对象：普通用户


> 开发者提示：如需由服务器下发 OTA 升级请求（对接后端），请参见 [OTA API](./OTA接口.md)。

1. 确保设备已激活已联网
2. 获取设备 IP 地址（见[获取设备 IP 地址](./获取设备IP地址.md)），然后用手机或电脑连接同一个 Wi-Fi（确保同一局域网）
3. 通过浏览器访问：http://<机器人IP>/update
4. 点击 “Tap to choose a firmware file (.ota)”
5. 上传Albee_xxx.ota文件
6. 点击Upload & Flash

<img src="../../assets/img/local-ota/1.png" width="560">

---

**文档最新修改时间：** 2026-10-09