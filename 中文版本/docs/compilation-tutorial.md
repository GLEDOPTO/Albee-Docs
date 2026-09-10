# 固件编译教程

本文档介绍如何从源码编译并烧录格乐机器人（ESP32-S3 桌面机器人）固件，以及常用构建配置和辅助脚本的用法。

## 1. 环境要求

| 项目 | 要求 |
| ---- | ------------------------------------------------------------ |
| 操作系统 | Linux（命令行 / VSCode）或 Windows 10/11（VSCode + ESP-IDF 扩展） |
| ESP-IDF | **v5.4.3**（`dependencies.lock` 要求 >= 5.3；当前 `sdkconfig` 基于 5.4.3） |
| Python | >= 3.8（ESP-IDF 官方要求；构建脚本也需要） |
| CMake | >= 3.16 |
| 网络 | 首次构建需要联网，从 ESP 组件仓库拉取 `managed_components/` 依赖 |

## 2. 搭建 ESP-IDF 环境

二选一即可。如已安装 v5.4.x，可跳过本节。

> **官方教程**（英文，v5.4.4，与本项目使用的 v5.4.x 同系列；切换版本或语言只需替换 URL 中的 `en/v5.4.4` —— 例如中文版为 `zh_CN/v5.4.3`）：
>
> - [ESP32-S3 入门（如何获取 ESP-IDF）](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/index.html)
> - [Linux 和 macOS 标准工具链搭建](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/linux-macos-setup.html)
> - [Windows 标准工具链搭建](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/windows-setup.html)
> - [建立与 ESP32-S3 的串口连接](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/establish-serial-connection.html)
> - [烧录故障排除](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/flashing-troubleshooting.html)

### 2.1 Linux（命令行）

**第 1 步：安装系统依赖**（Ubuntu / Debian）：

```bash
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv \
    cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

CentOS / Arch 等其他发行版请参见官方"标准搭建"文档中的命令。

**第 2 步：获取 ESP-IDF 并安装工具链**：

```bash
mkdir -p ~/esp && cd ~/esp
git clone -b v5.4.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32s3        # 只安装 esp32s3 目标以节省时间
```

如果从你的网络访问 GitHub 较慢（如中国大陆），安装前切换到乐鑫镜像下载服务器（只影响工具下载；git 仓库地址不变）：

```bash
export IDF_GITHUB_ASSETS="dl.espressif.cn/github_assets"
./install.sh esp32s3
```

**第 3 步：激活环境。** 每次打开新终端，先激活 IDF 环境：

```bash
. ~/esp/esp-idf/export.sh
```

`idf.py`、`esptool` 等命令只有激活后才可用。如果经常使用，可在 `~/.bashrc` 中添加别名；之后在任意终端输入 `get_idf` 即可激活环境：

```bash
alias get_idf='. $HOME/esp/esp-idf/export.sh'
```

> 注意：ESP-IDF 构建系统不支持 ESP-IDF 安装路径或项目路径中包含空格。

### 2.2 Windows（VSCode + ESP-IDF 扩展）

推荐使用乐鑫官方 VSCode 扩展，它会自动下载并配置 ESP-IDF、交叉编译工具链和 Python 虚拟环境。详细步骤参见[官方扩展文档](https://docs.espressif.com/projects/vscode-esp-idf-extension/en/latest/installation.html)。

1. **安装 VSCode**：从 [code.visualstudio.com](https://code.visualstudio.com/) 下载安装。
2. **安装 ESP-IDF 扩展**：在左侧扩展面板（`Ctrl+Shift+X`）搜索 "ESP-IDF"（发布者：Espressif Systems）并安装。
3. **安装 ESP-IDF 工具链**：在命令面板（`Ctrl+Shift+P`）运行 `ESP-IDF: Open ESP-IDF Installation Manager`（EIM 图形安装器）：
   - 下载源选择 `Download`（乐鑫服务器，大陆更快）或 `GitHub`；
   - 选择版本 **v5.4.3**；
   - 等待 ESP-IDF 和整套工具链自动下载（数 GB，视网络而定）。
   - 旧版扩展中该入口名为 `ESP-IDF: Configure ESP-IDF Extension` → **EXPRESS**，功能相同。
4. **选择 IDF 版本**：在命令面板运行 `ESP-IDF: Select Current ESP-IDF Version` 并选择 v5.4.3；如有异常可用 `ESP-IDF: Doctor Command` 自检环境。
5. **打开项目**：`File → Open Folder` 选择仓库根目录（包含 `CMakeLists.txt` 的文件夹）。
6. **日常开发**：使用底部状态栏的图标 —— 选择串口（设备以 USB-Serial-JTAG 方式出现，显示为 `COMx`）、火焰图标设置目标芯片为 `esp32s3`（仓库自带 `sdkconfig`，通常已设置好）、圆筒图标构建、闪电图标烧录（ESP32-S3 同时支持 UART 和 DFU；本项目使用 UART）、屏幕图标打开串口监视器。也可以打开 `Terminal → ESP-IDF Terminal` 使用已激活环境的终端，直接运行 `idf.py build` 等命令。

> Windows 注意事项：仓库中的 `robot_flash.sh` 和 `robot_bin.sh` 是 bash 脚本，无法在 PowerShell/CMD 中直接运行。日常烧录请使用扩展按钮或 `idf.py flash`；合并固件请使用 `python scripts/release.py`（跨平台 Python 脚本）；整理 `firmware/` 目录请在 Git Bash / WSL 中运行 `robot_bin.sh`。

## 3. 项目概览

| 路径 | 说明 |
| ---------------------------------- | ------------------------------------------------------------ |
| `CMakeLists.txt` | 项目名 `Albee`，版本 `PROJECT_VER`（当前 2.0.4；合并脚本从这里读取版本号） |
| `main/` | 应用源代码；`main/Kconfig.projbuild` 定义项目专用构建选项 |
| `main/boards/gledopto-robot/` | 唯一支持的板级代码（灯光控制 / 闹钟 / 足部传感器 / Web 控制等） |
| `partitions/v2/16m.csv` | 分区表（16 MB flash，双 OTA + 资源分区） |
| `sdkconfig` / `sdkconfig.defaults` | 当前生效的配置 / 默认基线 |
| `scripts/` | 构建辅助脚本（语言生成、资源打包等） |
| `extracted_emojis/` | 表情资源（`normal/` 约 444 KB，`large/` 约 912 KB） |
| `managed_components/` | 组件管理器自动下载的第三方组件 —— 请勿手动修改 |

分区表布局（`partitions/v2/16m.csv`）：

| 分区 | 类型 | 偏移 | 大小 |
| -------- | ----------- | -------- | -------- |
| nvs | data/nvs | 0x9000 | 0x4000 |
| otadata | data/ota | 0xd000 | 0x2000 |
| phy_init | data/phy | 0xf000 | 0x1000 |
| ota_0 | app | 0x20000 | 0x3f0000 |
| ota_1 | app | auto | 0x3f0000 |
| assets | data/spiffs | 0x800000 | 8M |

## 4. 构建

仓库自带完整的 `sdkconfig`（目标 esp32s3、板级 gledopto-robot、中文语言和默认资源均已配置好），可直接构建：

```bash
cd /path/to/gledopto-robot
idf.py build
```

构建过程中会自动执行两个项目专用的生成步骤：

1. **语言配置生成**：`scripts/gen_lang.py` 根据 `CONFIG_LANGUAGE_*` 生成 `main/assets/lang_config.h`，并将所选语言的提示音（`.ogg`）嵌入固件（缺失项回退到 en-US）。
2. **资源分区镜像生成**：`scripts/build_default_assets.py` 将表情集、字体和唤醒词模型打包为 `build/generated_assets.bin`。表情集取自 `extracted_emojis/normal` 或 `large`（取决于 `CONFIG_FULL_EMOJIS_DISPLAY`）。

构建成功后的关键产物（均在 `build/` 下）：

| 文件 | 说明 |
| ------------------------------------- | --------------------------------- |
| `Albee.bin` | 应用固件 |
| `bootloader/bootloader.bin` | 引导加载器 |
| `partition_table/partition-table.bin` | 分区表 |
| `ota_data_initial.bin` | 初始 OTA 数据 |
| `generated_assets.bin` | 资源分区镜像（表情 / 字体 / 模型） |

### 常用 idf.py 命令

| 命令 | 用途 |
| ----------------------------------- | ------------------------------------------------------------ |
| `idf.py build` | 构建 |
| `idf.py menuconfig` | 图形化配置 |
| `idf.py set-target esp32s3` | 设置目标芯片（会清空构建产物并重置 `sdkconfig` —— 不要随意运行） |
| `idf.py -p PORT flash` | 构建并烧录 |
| `idf.py -p PORT monitor` | 串口监视器；`Ctrl+]` 退出（`Ctrl+T` 打开工具菜单） |
| `idf.py -p PORT flash monitor` | 一条命令完成构建 + 烧录 + 监视 |
| `idf.py clean` / `idf.py fullclean` | 清理增量产物 / 删除整个构建目录 |
| `idf.py -p PORT erase-flash` | 擦除整个 flash（包括 NVS 中的配网等配置 —— 恢复出厂） |
| `idf.py -p PORT erase-otadata` | 只擦除 OTA 数据分区（用于 OTA 升级异常或切换启动分区） |

常用参数：`-p` 选择串口；`-b` 设置烧录波特率（默认 460800）；`-j N` 设置并行构建任务数。

## 5. 常用构建选项（menuconfig）

```bash
idf.py menuconfig
```

项目专用选项位于 **Albee** 菜单下（定义于 `main/Kconfig.projbuild`）：

| 选项 | 默认值 | 说明 |
| -------------------------- | --------------------- | ------------------------------------------------------------ |
| `Board Type` | gledopto-robot | 唯一支持的板型 —— 不要修改 |
| `Language` | Chinese (Simplified) | 语音 / 提示音语言；支持 30+ 种语言 |
| `Assets` | 构建时生成默认资源 | 也可以选择自定义 `assets.bin` 或跳过资源烧录 |
| `full emojis display` | n | 打包大表情集（`large/`）并启用全屏表情显示样式；占用更多 flash |
| `sleep show time` | n | 省电休眠时表情与时钟交替显示（依赖上一项） |
| `emojis new display` | n | 新版状态表情钩子（低电量 / WiFi / 充电动图） |
| `enable web robot control` | n | 内置网页包含机器人运动控制面板（否则只有灯光控制页） |
| `robot quiet lively mode` | n | 长按 BOOT 键切换安静/活泼模式 |
| `robot low power limit` | y | 低电量时限制步态速度；建议保持开启 |
| `foot sensor set` | n | 编译足部 LTR-553 寄存器配置下载（仅在调试传感器参数时开启） |
| `enable debug log` | y | 所有模块日志的总开关 |

> 注意：`USE_ENGLISH_ENABLE`（切换 MCP 工具描述等的输出语言）不是 Kconfig 选项 —— 它是 `main/boards/gledopto-robot/config.h` 中的宏。请在那里修改后重新编译。

修改配置后，直接再次运行 `idf.py build` 即可。删除 `sdkconfig` 后重新构建会从 `sdkconfig.defaults` 重新生成 —— **当前的所有自定义配置都会丢失**，删除前请谨慎。

## 6. 烧录

### 方法一：idf.py（日常开发推荐）

```bash
idf.py flash monitor    # 烧录并打开串口监视器；Ctrl+] 退出
idf.py -p /dev/ttyACM0 flash monitor   # 指定串口
```

当 `CONFIG_FLASH_DEFAULT_ASSETS=y` 时，`idf.py flash` 会**同时烧录资源分区**（固件 + 表情一步完成）。

烧录前确认串口：

- **Windows**：设备管理器 → "端口 (COM 和 LPT)" 显示 `COMx`；
- **Linux**：`ls /dev/tty*` —— USB-Serial-JTAG 端口为 `/dev/ttyACM0`；外接 USB-UART 转接板为 `/dev/ttyUSB0`。

如果烧录时反复打印 `Connecting........_____` 且无法连接，请手动进入下载模式：**按住 BOOT，短按一次 RESET，然后松开 BOOT**，再重新烧录。ESP32-S3 的原生 USB 通常会自动复位进入下载模式；只有在自动方式失效时才需要手动操作。

### 方法二：robot_flash.sh（无 IDF 环境的独立整机烧录）

```bash
./robot_flash.sh              # 默认串口 /dev/ttyACM0
./robot_flash.sh /dev/ttyUSB0 # 指定串口
```

该脚本直接调用 esptool，按固定地址烧录（16 MB flash，DIO，80 MHz）：

| 镜像 | 烧录地址 |
| -------------------- | -------- |
| bootloader.bin | 0x0 |
| partition-table.bin | 0x8000 |
| ota_data_initial.bin | 0xd000 |
| Albee.bin | 0x20000 |
| generated_assets.bin | 0x800000 |

如缺少 `generated_assets.bin`，脚本会警告"设备将无表情启动"并要求确认。

## 7. 固件整理与合并

| 工具 | 用途 |
| --------------------------- | ------------------------------------------------------------ |
| `./robot_bin.sh` | 将 `build/` 中的 5 个固件产物同步到 `firmware/`（先清空目录再复制；任一文件缺失则报错） |
| `python scripts/release.py` | 调用 `idf.py merge-bin` 将引导加载器 / 分区表 / OTA 数据 / 固件 / 资源合并为单一文件，自动输出到 `releases/Albee_all_<版本>.bin`（版本号取自 `CMakeLists.txt` 的 `PROJECT_VER`）；适合量产烧录或分发 |

`release.py` 必须在激活 ESP-IDF 环境后运行（内部调用 `idf.py`）。不带参数时以"打包当前构建目录"模式运行：

```bash
python scripts/release.py
```

发布流程参考：修改 `CMakeLists.txt` 中的 `PROJECT_VER` → `idf.py build` → `python scripts/release.py` → 产物自动输出到 `releases/Albee_all_<版本>.bin`。

`release.py` 还支持按板级配置一键构建打包：从 `main/boards/<板型>/config.json` 读取变体定义，对每个变体依次执行 `set-target`、追加 `sdkconfig_append` 选项、以 `-DBOARD_NAME=<变体>` 构建、合并并输出。

```bash
python scripts/release.py --list-boards                        # 列出所有板型和变体
python scripts/release.py gledopto-robot                       # 构建该板型的所有变体
python scripts/release.py gledopto-robot --name gledopto-robot # 只构建指定变体
```

> 注意：板型模式会按 `config.json` 重置并追加配置（gledopto-robot 变体会追加 `CONFIG_USE_DEVICE_AEC=y`、`CONFIG_USE_WAKE_WORD_DETECT=n` 等），因此结果可能与你手动编辑 `sdkconfig` 后的日常构建产物不同。

## 8. 常见问题

- **首次构建卡在下载组件**：组件管理器需要访问 ESP 组件仓库；请确保网络可达。依赖锁定在 `dependencies.lock` 中。
- **设备不显示表情**：资源分区未烧录。用 `idf.py flash`（含资源）或 `./robot_flash.sh` 重新烧录。
- **固件大小接近分区上限**：关闭 `full emojis display`，使用 `normal` 表情集。
- **串口权限不足**：Linux 下将用户加入 `dialout` 组（`sudo usermod -aG dialout $USER`；Arch 系发行版组名为 `uucp`），然后注销重新登录。
- **烧录提示串口被占用**：其他程序占用了端口 —— 关闭正在运行的监视器（`Ctrl+]`）、PuTTY、串口助手等。
- **反复 `Connecting...` 不成功**：手动进入下载模式 —— 按住 BOOT、短按 RESET、松开 BOOT，再重试烧录（见第 6 节）。
- **串口监视器乱码 / 无输出**：确认波特率为 115200；设备同时支持 UART 和 USB-Serial-JTAG（`/dev/ttyACM0`）—— 换另一个串口试试。
- **找不到 `idf.py`**：Linux 下终端未激活 IDF 环境 —— 先运行 `. ~/esp/esp-idf/export.sh`；Windows 下通过 `Terminal → ESP-IDF Terminal` 打开已激活的终端。
