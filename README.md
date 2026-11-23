# WinBloat

A post-installation Windows 11 setup, debloating, and application deployment tool written in Python.

## Overview

`WinBloat` streamlines setting up a fresh Windows 11 environment by automatically requesting administrator privileges, installing applications defined in a customizable list via `winget`, and applying pre-configured system tweaks through Chris Titus Tech's Windows Utility (`winutil`).

### What's New in v2.0.0
* **Dynamic App List (`apps.txt`):** Add or remove `winget` package IDs directly inside `apps.txt` without modifying the Python source code. Comment lines starting with `#` and blank lines are ignored.
* **Pre-Saved WinUtil Configuration (`winutil-config.json`):** Automatically passes a local configuration file (`-Config`) to Chris Titus WinUtil so system optimization settings are applied consistently.
* **Terminal Output Logging:** Captures command execution output to `command_output.txt` while handling carriage-return progress redraws cleanly in the console.

---

## Repository Structure

* `fun.py` — Main Python script handling UAC elevation, `winget` package installation, and Chris Titus WinUtil execution.
* `apps.txt` — Line-delimited list of `winget` package IDs to install (supports `#` comments).
* `winutil-config.json` — Pre-saved configuration file passed to Chris Titus WinUtil (place alongside `fun.py` and `apps.txt`).
* `command_output.txt` — Generated automatically when commands run to log PowerShell/`winget`/WinUtil output.
* Compiled executable / release artifacts — Built for standalone execution on Windows.

---

## Prerequisites

* **OS:** Windows 11
* **Package Manager:** `winget` (App Installer) available in PowerShell
* **Privileges:** Administrator rights (the script attempts automatic UAC elevation via `ShellExecuteW(..., "runas", ...)` if not already elevated)
* **Network Access:** Required to fetch `winget` packages and run `https://christitus.com/win`
* **For running from source:** Python 3

---

## Usage

### 1. Customize Applications (`apps.txt`)
Edit `apps.txt` and list one `winget` package ID per line. Example entries include:

```text
# One Winget package ID per line.
# Lines beginning with # are ignored.
Google.Chrome
Notepad++.Notepad++
Microsoft.VisualStudioCode
Microsoft.PowerShell
7zip.7zip
Discord.Discord.PTB
Valve.Steam
9P8LTPGCBZXD
VideoLAN.VLC
Git.Git
OpenVPNTechnologies.OpenVPNConnect
Cloudflare.Warp
Oracle.VirtualBox
Python.Python.3
Roblox.Roblox
```

### 2. Add Your WinUtil Config (`winutil-config.json`)
Place your exported/pre-saved `winutil-config.json` file in the same directory as the script or executable.
* If `winutil-config.json` is missing, `run_chris_titus()` reports that the file was not found and exits with code `1`.

### 3. Run the Tool
Run the compiled executable or run the Python script from the project directory:

```powershell
python .\fun.py
```

If the current session is not elevated, Windows will prompt for administrator approval and relaunch the process.

---

## How It Works

1. **Admin Check (`check_admin`):** Uses `ctypes.windll.shell32.IsUserAnAdmin()` to verify elevation. If not running as administrator, it triggers `ShellExecuteW` with `"runas"`.
2. **App Installation (`load_apps` & `app_process`):** Reads `apps.txt` using UTF-8 encoding, skips blank and `#`-prefixed lines, and executes:
   ```powershell
   winget install --id <PackageID> --silent --accept-source-agreements --accept-package-agreements --exact
   ```
   for each package.
3. **System Optimization (`run_chris_titus`):** Verifies `winutil-config.json` exists in the script directory and runs:
   ```powershell
   & ([ScriptBlock]::Create((irm 'https://christitus.com/win'))) -Config '<path-to-winutil-config.json>'
   ```
   via PowerShell (`-NoProfile -NonInteractive`).

---

## Notes & Troubleshooting

* **Keep config files in the same folder:** Both `apps.txt` and `winutil-config.json` are resolved relative to the script/executable directory (`Path(__file__).resolve().parent`).
* **Review tweaks before applying:** Chris Titus WinUtil modifies Windows services, privacy/telemetry settings, and system behavior—always inspect your `winutil-config.json` before running it on a production or primary machine.
* **Logs:** Check `command_output.txt` in the working directory for detailed output from `winget` and PowerShell commands.

## Author & Links

* **GitHub:** [Zihaff4/WinBloat](https://github.com/Zihaff4/WinBloat)