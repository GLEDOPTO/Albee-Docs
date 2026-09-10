# Method 1: Flash via the Flash Download Tool on a PC (No IDF Development Environment Required)

## Preparation

Install the Flash Download Tool: https://dl.espressif.com/public/flash_download_tool.zip

## Firmware

Latest firmware URL: TODO

### Download Settings

(1) Chip Type: select **ESP32-S3**

(2) Work Mode: select **Develop**

(3) Load Mode: **UART** is recommended

![flashing interface](../img/flashing interface.png)

(4) Plug the data cable into your computer and into the Type-C port on the side of the robot

> [!IMPORTANT]
>
> Preferably use the original cable that came with the device, or make sure the cable you use supports data transfer
>
> Make sure the device is powered on (long-press the Power button for 3 seconds to turn it on)

### 2) Load Firmware & SPI Download Settings

(1) Click the **...** button on the first empty row and select the directory of the .bin file to import it, as shown below:

TODO

(2) Tick the checkbox in front of the imported bin file row (this must be checked), and enter `0x0`, `0x00`, or `0` in the input box after the bin file selection box (this downloads the firmware to the start of flash region 1 on the board)

(3) Select the corresponding COM port

(4) Check the other options as shown below

(5) Click **START** to begin flashing. The progress bar appears; when it completes, the status shows **FINISH**, as shown below.

TODO

(6) After flashing is complete, restart the device (long-press the Power button for 3 seconds to power off, release, then long-press for 3 seconds again to power on)

# Method 2: Flash via a Web Browser

## Preparation

(1) Power on the device

(2) Plug the data cable into your computer and into the Type-C port on the side of the robot

(3) Visit: TODO

## Download Firmware

TODO

## Error Messages & Troubleshooting

### **Q1: The COM port is not displayed?**

(1) Check whether the device is powered on

(2) Check whether the cable you are using supports data transfer

(3) Restart the device and try unplugging/replugging a few times

### **Q2: The program does not run properly after flashing?**

(1) Check whether the device is powered on

**For other issues not mentioned above, please contact us by email: service@gledopto.com.**
