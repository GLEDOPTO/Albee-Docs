# Firmware Compilation Tutorial
> Firmware: Albee v2.0.5 ｜ Audience: Developer


This document describes how to compile and flash the GLEDOPTO Robot (ESP32-S3 desktop robot) firmware from source, and how to use the common build configurations and helper scripts.

## 1. Environment Requirements

| Item | Requirement |
| ---- | ------------------------------------------------------------ |
| Operating system | Linux (command line / VSCode) or Windows 10/11 (VSCode + ESP-IDF extension) |
| ESP-IDF | **v5.4.3** (`dependencies.lock` requires >= 5.3; the current `sdkconfig` is based on 5.4.3) |
| Python | >= 3.8 (officially required by ESP-IDF; also needed by the build scripts) |
| CMake | >= 3.16 |
| Network | The first build requires internet access to pull `managed_components/` dependencies from the ESP Component Registry |

## 2. Setting Up the ESP-IDF Environment

Choose either method below. If v5.4.x is already installed, skip this section.

> **Official tutorials** (English, v5.4.4, same series as the v5.4.x used by this project; to switch version or language, replace `en/v5.4.4` in the URL — e.g., the Chinese version is `zh_CN/v5.4.3`):
>
> - [ESP32-S3 Get Started (How to Get ESP-IDF)](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/index.html)
> - [Standard Toolchain Setup for Linux and macOS](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/linux-macos-setup.html)
> - [Standard Toolchain Setup for Windows](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/windows-setup.html)
> - [Establish Serial Connection with ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/establish-serial-connection.html)
> - [Flashing Troubleshooting](https://docs.espressif.com/projects/esp-idf/en/v5.4.4/esp32s3/get-started/flashing-troubleshooting.html)

### 2.1 Linux (Command Line)

**Step 1: Install system dependencies** (Ubuntu / Debian):

```bash
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv \
    cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

For CentOS / Arch and other distributions, see the commands in the official "Standard Setup" documentation.

**Step 2: Get ESP-IDF and install the toolchain**:

```bash
mkdir -p ~/esp && cd ~/esp
git clone -b v5.4.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32s3        # install only the esp32s3 target to save time
```

If GitHub is slow from your network (e.g., mainland China), switch to Espressif's mirror download server before installing (this only affects tool downloads; the git repository URL stays the same):

```bash
export IDF_GITHUB_ASSETS="dl.espressif.cn/github_assets"
./install.sh esp32s3
```

**Step 3: Activate the environment.** Every time you open a new terminal, activate the IDF environment first:

```bash
. ~/esp/esp-idf/export.sh
```

Commands such as `idf.py` and `esptool` are only available after activation. If you use it often, add an alias to `~/.bashrc`; afterwards typing `get_idf` in any terminal activates the environment:

```bash
alias get_idf='. $HOME/esp/esp-idf/export.sh'
```

> Note: The ESP-IDF build system does not support spaces in the ESP-IDF installation path or in the project path.

### 2.2 Windows (VSCode + ESP-IDF Extension)

The recommended way is Espressif's official VSCode extension, which downloads and configures ESP-IDF, the cross-compilation toolchain, and the Python virtual environment for you. For detailed steps, see the [official extension documentation](https://docs.espressif.com/projects/vscode-esp-idf-extension/en/latest/installation.html).

1. **Install VSCode**: download and install from [code.visualstudio.com](https://code.visualstudio.com/).
2. **Install the ESP-IDF extension**: in the extensions panel on the left (`Ctrl+Shift+X`), search for "ESP-IDF" (publisher: Espressif Systems) and install it.
3. **Install the ESP-IDF toolchain**: from the command palette (`Ctrl+Shift+P`), run `ESP-IDF: Open ESP-IDF Installation Manager` (the EIM graphical installer):
   - Choose `Download` (Espressif's server, faster in mainland China) or `GitHub` as the download source;
   - Select version **v5.4.3**;
   - Wait for ESP-IDF and the whole toolchain to download automatically (several GB, depending on your network).
   - In older extension versions the entry is named `ESP-IDF: Configure ESP-IDF Extension` → **EXPRESS**, which does the same thing.
4. **Select the IDF version**: from the command palette, run `ESP-IDF: Select Current ESP-IDF Version` and pick v5.4.3; if anything looks wrong, use `ESP-IDF: Doctor Command` to self-check the environment.
5. **Open the project**: `File → Open Folder` and select the repository root (the folder containing `CMakeLists.txt`).
6. **Daily development**: use the icons in the bottom status bar — select the serial port (the device shows up as USB-Serial-JTAG, displayed as `COMx`), the flame icon to set the target chip to `esp32s3` (the repository ships a `sdkconfig`, usually already set), the cylinder icon to build, the lightning icon to flash (ESP32-S3 supports both UART and DFU; this project uses UART), and the screen icon for the serial monitor. You can also open `Terminal → ESP-IDF Terminal` for a terminal with the environment already activated, and run commands like `idf.py build` directly.

> Note for Windows: `robot_flash.sh` and `robot_bin.sh` in the repository are bash scripts and cannot run directly in PowerShell/CMD. For daily flashing, use the extension buttons or `idf.py flash`; to merge firmware, use `python scripts/release.py` (a cross-platform Python script); to organize the `firmware/` directory, run `robot_bin.sh` from Git Bash / WSL.

## 3. Project Overview

| Path | Description |
| ---------------------------------- | ------------------------------------------------------------ |
| `CMakeLists.txt` | Project name `Albee`, version `PROJECT_VER` (currently 2.0.5; the merge script reads the version from here) |
| `main/` | Application source code; `main/Kconfig.projbuild` defines the project-specific build options |
| `main/boards/gledopto-robot/` | The only supported board code (light control / alarm clock / foot sensor / web control, etc.) |
| `partitions/v2/16m.csv` | Partition table (16 MB flash, dual OTA + assets partitions) |
| `sdkconfig` / `sdkconfig.defaults` | Current active configuration / default baseline |
| `scripts/` | Build helper scripts (language generation, assets packing, etc.) |
| `extracted_emojis/` | Emoji assets (`normal/` ≈ 444 KB; `large/` ≈ 752 KB with 26 GIFs — recompressed in v2.0.5 with a new `power-on.gif`) |
| `managed_components/` | Third-party components downloaded automatically by the component manager — do not modify them manually |

Partition table layout (`partitions/v2/16m.csv`):

| Partition | Type | Offset | Size |
| -------- | ----------- | -------- | -------- |
| nvs | data/nvs | 0x9000 | 0x4000 |
| otadata | data/ota | 0xd000 | 0x2000 |
| phy_init | data/phy | 0xf000 | 0x1000 |
| ota_0 | app | 0x20000 | 0x3f0000 |
| ota_1 | app | auto | 0x3f0000 |
| assets | data/spiffs | 0x800000 | 8M |

## 4. Building

The repository already ships a complete `sdkconfig` (target esp32s3, board gledopto-robot, Chinese language, and default assets are all configured), so you can build directly:

```bash
cd /path/to/gledopto-robot
idf.py build
```

Two project-specific generation steps run automatically during the build:

1. **Language configuration generation**: `scripts/gen_lang.py` generates `main/assets/lang_config.h` from `CONFIG_LANGUAGE_*` and embeds the selected language's prompt sounds (`.ogg`) into the firmware (missing items fall back to en-US).
2. **Assets partition image generation**: `scripts/build_default_assets.py` packs the emoji set, fonts, and the wake-word model into `build/generated_assets.bin`. The emoji set is taken from `extracted_emojis/normal` or `large` (depending on `CONFIG_FULL_EMOJIS_DISPLAY`).

Key artifacts after a successful build (all under `build/`):

| File | Description |
| ------------------------------------- | --------------------------------- |
| `Albee.bin` | Application firmware |
| `bootloader/bootloader.bin` | Bootloader |
| `partition_table/partition-table.bin` | Partition table |
| `ota_data_initial.bin` | Initial OTA data |
| `generated_assets.bin` | Assets partition image (emojis / fonts / models) |

### Common idf.py Commands

| Command | Purpose |
| ----------------------------------- | ------------------------------------------------------------ |
| `idf.py build` | Build |
| `idf.py menuconfig` | Graphical configuration |
| `idf.py set-target esp32s3` | Set the target chip (clears build artifacts and resets `sdkconfig` — do not run it casually) |
| `idf.py -p PORT flash` | Build and flash |
| `idf.py -p PORT monitor` | Serial monitor; exit with `Ctrl+]` (`Ctrl+T` opens the tool menu) |
| `idf.py -p PORT flash monitor` | Build + flash + monitor in one command |
| `idf.py clean` / `idf.py fullclean` | Clean incremental artifacts / delete the entire build directory |
| `idf.py -p PORT erase-flash` | Erase the whole flash (including provisioning and other config in NVS — factory reset) |
| `idf.py -p PORT erase-otadata` | Erase only the OTA data partition (for abnormal OTA upgrades or switching the boot partition) |

Common parameters: `-p` selects the serial port; `-b` sets the flashing baud rate (default 460800); `-j N` sets the number of parallel build jobs.

## 5. Common Build Options (menuconfig)

```bash
idf.py menuconfig
```

The project-specific options are under the **Albee** menu (defined in `main/Kconfig.projbuild`):

| Option | Default | Description |
| -------------------------- | --------------------- | ------------------------------------------------------------ |
| `Board Type` | gledopto-robot | The only supported board — do not change |
| `Language` | Chinese (Simplified) | Voice / prompt-sound language; 30+ languages available (server-side options) |
| `Assets` | Generate default assets at build time | Can also select a custom `assets.bin` or skip flashing assets |
| `full emojis display` | **y** | Pack the large emoji set (`large/`) and enable the full-screen emoji display style; uses more flash |
| `sleep show clock` | **y** | Alternate emoji and clock display during power-saving sleep (depends on the option above) |
| `emojis status gifs` | **y** | New status emoji hooks (low battery / WiFi / charging GIF) |
| `enable web robot control` | **y** | The built-in web page includes the robot motion control panel (otherwise only the light control page) |
| `robot low power limit` | y | Limit gait speed at low battery; recommended to keep enabled |
| `foot sensor cfg download` | **y** | Compile in the foot LTR-553 register configuration download (enable only when tuning sensor parameters) |
| `enable debug log` | y | Master switch for all module logs |

> Note: `USE_ENGLISH_ENABLE` (which switches the output language of MCP tool descriptions, etc.) is not a Kconfig option — it is a macro in `main/boards/gledopto-robot/config.h`. Modify it there and rebuild.

After changing the configuration, just run `idf.py build` again. Deleting `sdkconfig` and rebuilding regenerates it from `sdkconfig.defaults` — **all current custom configuration will be lost**, so be careful before deleting it.

## 6. Flashing

### Method 1: idf.py (recommended for daily development)

```bash
idf.py flash monitor    # flash and open the serial monitor; exit with Ctrl+]
idf.py -p /dev/ttyACM0 flash monitor   # specify the serial port
```

When `CONFIG_FLASH_DEFAULT_ASSETS=y`, `idf.py flash` also **flashes the assets partition** (firmware + emojis in one step).

Confirm the serial port before flashing:

- **Windows**: Device Manager → "Ports (COM & LPT)" shows `COMx`;
- **Linux**: `ls /dev/tty*` — the USB-Serial-JTAG port is `/dev/ttyACM0`; an external USB-UART bridge is `/dev/ttyUSB0`.

If flashing repeatedly prints `Connecting........_____` and never connects, enter download mode manually: **hold down BOOT, short-press RESET once, then release BOOT**, and flash again. The ESP32-S3's native USB usually resets into download mode automatically; the manual procedure is only needed when that fails.

### Method 2: robot_flash.sh (standalone full-device flashing without the IDF environment)

```bash
./robot_flash.sh              # default serial port /dev/ttyACM0
./robot_flash.sh /dev/ttyUSB0 # specify the serial port
```

This script calls esptool directly and flashes at fixed addresses (16 MB flash, DIO, 80 MHz):

| Image | Flash address |
| -------------------- | -------- |
| bootloader.bin | 0x0 |
| partition-table.bin | 0x8000 |
| ota_data_initial.bin | 0xd000 |
| Albee.bin | 0x20000 |
| generated_assets.bin | 0x800000 |

If `generated_assets.bin` is missing, the script warns that "the device will boot without emojis" and asks for confirmation.

## 7. Firmware Organizing and Merging

| Tool | Purpose |
| --------------------------- | ------------------------------------------------------------ |
| `./robot_bin.sh` | Sync the 5 firmware artifacts from `build/` to `firmware/` (clears the directory first, then copies; errors out if any file is missing) |
| `idf.py ota` (`scripts/make_ota.py`) | Produces the web-upload firmware package `OTA/Albee_<version>.ota` plus a `<build_time>.txt` in the same directory (build date/time + git tag + first 8 hex chars of the app elf sha256, matching the `build_time` in the device's `/api/system/info` — used to tell apart different builds of the same version); each run first clears the `OTA/` directory, keeping only the latest output |
| `python scripts/release.py` | Calls `idf.py merge-bin` to merge the bootloader / partition table / OTA data / firmware / assets into a single file, automatically output to `releases/Albee_all_<version>.bin` (the version comes from `PROJECT_VER` in `CMakeLists.txt`); suitable for production flashing or distribution |

`release.py` must be run with the ESP-IDF environment activated (it calls `idf.py` internally). Without arguments it runs in "package the current build directory" mode:

```bash
python scripts/release.py
```

Release flow reference: modify `PROJECT_VER` in `CMakeLists.txt` → `idf.py build` → `python scripts/release.py` → the artifact is output to `releases/Albee_all_<version>.bin` automatically.

`release.py` also supports one-click building and packaging per board configuration: it reads the variant definitions from `main/boards/<board>/config.json`, and for each variant runs `set-target`, appends the `sdkconfig_append` options, builds with `-DBOARD_NAME=<variant>`, merges, and outputs.

```bash
python scripts/release.py --list-boards                        # list all boards and variants
python scripts/release.py gledopto-robot                       # build all variants of this board
python scripts/release.py gledopto-robot --name gledopto-robot # build only the specified variant
```

> Note: Board mode resets and appends configuration according to `config.json` (gledopto-robot variants append `CONFIG_USE_DEVICE_AEC=y`, `CONFIG_USE_WAKE_WORD_DETECT=n`, etc.), so the result may differ from your daily build artifacts after manually editing `sdkconfig`.

## 8. FAQ

- **First build stuck downloading components**: the component manager needs access to the ESP Component Registry; make sure the network is reachable. Dependencies are locked in `dependencies.lock`.
- **Device shows no emojis**: the assets partition was not flashed. Re-flash with `idf.py flash` (which includes assets) or `./robot_flash.sh`.
- **Firmware size close to the partition limit**: turn off `full emojis display` and use the `normal` emoji set.
- **Serial port permission denied**: on Linux, add your user to the `dialout` group (`sudo usermod -aG dialout $USER`; on Arch-based distributions the group is `uucp`), then log out and log back in.
- **Flashing reports the serial port is busy**: another program is occupying the port — close any running monitor (`Ctrl+]`), PuTTY, serial assistant, etc.
- **Repeated `Connecting...` without success**: enter download mode manually — hold BOOT, short-press RESET, release BOOT, then retry flashing (see Section 6).
- **Garbled text / no output in the serial monitor**: confirm the baud rate is 115200; the device supports both UART and USB-Serial-JTAG (`/dev/ttyACM0`) — try the other serial port.
- **`idf.py` not found**: on Linux, the terminal has not activated the IDF environment — run `. ~/esp/esp-idf/export.sh` first; on Windows, open the pre-activated terminal via `Terminal → ESP-IDF Terminal`.

---

**Last modified:** 2026-10-16
