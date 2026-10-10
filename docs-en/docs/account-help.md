# Account & Device Issues
> Firmware: Albee v2.0.4 or later ｜ Audience: End user


This page covers common account problems: not receiving the SMS verification code, forgetting your password or username, and unbinding a device.

## Cannot Receive the SMS Verification Code

Normally the verification code arrives within 5 minutes; for international phone numbers, please allow up to 10 minutes. If you still do not receive it, check whether your phone service is suspended or out of credit, or whether the message was intercepted by a third-party security app.

## Know the Username but Forgot the Password

- If a phone number is bound to your account, log in via SMS instead.
- If no phone number is bound, send an email with your **username** and **device ID** to <service@gledopto.com>.

Email subject format: `【Password Recovery, Username XXX, Device ID XXX】`

## Forgot Both Username and Password

- If a phone number is bound to your account, log in via SMS instead.
- If no phone number is bound, send an email with your **device ID** and **activation date** to <service@gledopto.com>.

Email subject format: `【Username Recovery, Device ID XXX, Activation Date XXX】`

## How to Get the Device ID and MAC Address

- **Device ID** — If your device is working, simply talk to it and ask it to tell you.
- **MAC address** — See [How to View the MAC Address](./check-mac-address.md): get it via the web page (`http://<device-ip>/info`) or from the serial log.

## Device Already Bound to Another Account — How to Unbind

This usually happens when a dev kit or chip module was previously bound to someone else's account and was not unbound on the xiaozhi.me website before being returned or resold.

To unbind it, send an email to <service@gledopto.com> with the subject:

`【Unbind Device, Device ID XXX, MAC Address XXX】`

If you need to unbind multiple devices, download the template below, fill in the device IDs and MAC addresses, attach the completed spreadsheet to the email, and use the subject `【Unbind Device】`:

[Download the unbind template (xlsx)](../../assets/account-help/xiaozhi-device-unbind-template.xlsx)

## How to View the MAC Address

See [How to View the MAC Address](./check-mac-address.md): Method 1 gets it via the web page (`http://<device-ip>/info`), and Method 2 uses a serial terminal tool.

---

**Last modified:** 2026-10-08

---

**Official site:** <http://www.gledoptorobots.com>

**Support:** service@gledopto.com
