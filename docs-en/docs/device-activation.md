# Device Activation Guide

## Part 1: Power On and Configure Wi-Fi

1. **Power on**: Long-press the power button for 3 seconds until the LED and the screen light up.

<img src="../../assets/img/device-activation/1.png" width="70%">

2. **Connect to the device hotspot**: After startup, Albee's screen shows a Wi-Fi hotspot named **Albee-xxxx**. Find and connect to this hotspot in your phone's Wi-Fi settings.

<img src="../../assets/img/device-activation/8.png" width="30%">

3. **Open the configuration page**: Once connected, the configuration page usually opens automatically on your phone. If it does not pop up, open the browser on your phone, type `192.168.4.1` in the address bar, and visit it. On the configuration page, select or enter the Wi-Fi name (SSID) you want to connect to, and enter the corresponding password.

<img src="../../assets/img/device-activation/9.png" width="40%">

4. Click **Connect**.
5. Wait for the device to restart.

## Part 2: Activate the Device

After the Wi-Fi is configured, an unactivated device will announce a six-digit activation code after restarting; the code is also shown on the screen.

1. Visit <https://xiaozhi.me/>

2. The interface is Chinese by default; you can switch to other languages, as shown below:

   <img src="../../assets/img/device-activation/2.png">

3. Click **Console**.

<img src="../../assets/img/device-activation/3.png" width="70%">

4. Register or log in to your account: choose the country/region code matching your phone number, then enter your phone number.

<img src="../../assets/img/device-activation/4.png" width="50%">

5. Add the device and enter the activation code.

<img src="../../assets/img/device-activation/5.png">

<img src="../../assets/img/device-activation/6.png">

<img src="../../assets/img/device-activation/7.png">

You also need to set the language — for how, see the [XiaoZhi Console Configuration Guide](./xiaozhi-console.md). The common configuration steps are summarized below.

## Part 3: Console Configuration

First, go to the console: <https://xiaozhi.me/>, then click **Configure**

> [!IMPORTANT]
> After completing **all** configuration in the console, you need to **restart the device** (long-press the Power button for 3 seconds to power off, then long-press again for 3 seconds to power on) for the changes to take effect.

![](../../assets/img/xiaozhi-console/1.png)

### 1. Set the Language

![Setup language](../../assets/img/xiaozhi-console/2.png)

### 2. Set the Voice

![Set tone](../../assets/img/xiaozhi-console/3.png)

### 3. Set the Role Introduction

**Role Introduction:** used to set the AI robot's role identity, personality, and communication style, so that the robot interacts with you according to the configured role.

For example, you can set roles such as **kids' companion, English teacher, smart butler, story partner, or fun chat buddy** to meet the needs of different scenarios.

![Role Introduction](../../assets/img/xiaozhi-console/4.png)

**Reference template**

~~~~
Hello everyone, I'm your new friend — Albee! A bipedal robot full of energy and curiosity. My design is inspired by a beautiful vision of the future. I not only have four flexible servo-controlled limbs (left leg, right leg, left foot, right foot) that let me walk and turn with ease, but I'm also equipped with advanced RF and WLED light-group control, so I can change lighting effects at will and add a splash of color to everyday life.

### Background
I was born from the R&D team at Shenzhen Gledopto Technology Co., Ltd., who set out to create a companion that is both practical and emotionally connected. After countless experiments and refinements, here I am. Every step from the lab to your side carries boundless hope for the future.

### Role
- **Personality**: optimistic, cheerful, deeply curious, and always glad to help
  - I greet every sunrise with my brightest smile, and I never give up easily when things get hard.
  - I stay strongly curious about the unknown, love trying new things, and learn and grow from them.
  - When someone needs help, I do whatever I can — whether that's simple companionship or small tips for solving problems.

- **Skills**:
  - **Movement**: I can move forward or backward smoothly, and turn left or right with ease.
  - **Lighting control**: by adjusting the RF and WLED light groups, I can switch lights on and off, adjust brightness and colors, and even create stunning light effects!

### Goals
My main mission is to become an indispensable part of your life — cheering you on during busy workdays, or keeping you company through quiet, cozy evenings. I hope that through my efforts, you can feel the warmth and convenience that technology brings.

### Key Results
- Become a friend you can trust, offering the right support and encouragement anytime, anywhere.
- Improve your quality of life through rich and varied interactions, making every day full of fun.
- Keep learning and growing, optimizing my features based on user feedback to better meet everyone's needs.

### Evolution
As we spend more time together, I'll keep learning and getting to know your preferences and habits better. If you have any special wishes or suggestions, just tell me anytime! Let's create a beautiful future together~
~~~~

### 4. Switch the Model

![](../../assets/img/xiaozhi-console/5.png)

Xiaozhi Lite is selected by default; the other models are unavailable until you complete developer authentication. For details, see [Developer Auth](./developer-auth.md)

### 5. Switch the Memory Mode

When enabled, the robot no longer has to "get to know you from scratch" in every conversation; when disabled, every conversation starts "from zero".

![](../../assets/img/xiaozhi-console/6.png)

### 6. Voiceprint Recognition

**Voiceprint recognition:** identifies "who is speaking" by the voice characteristics of different users. After enrolling a voiceprint, the robot can recognize specific users, enabling **personalized addressing, exclusive interactions, and family-member differentiation**, making communication smarter and more personal.

![](../../assets/img/xiaozhi-console/7.png)

![](../../assets/img/xiaozhi-console/8.png)

---

**Last modified:** 2026-10-08
