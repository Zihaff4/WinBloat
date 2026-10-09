# WinBloat

A simple Windows post-installation automation tool that helps set up a fresh Windows installation.

WinBloat automatically installs commonly used applications using Windows Package Manager (`winget`) and provides access to Chris Titus Tech's WinUtil for additional Windows configuration.

> ⚠️ This tool requires Administrator privileges.

## Features

* 🔐 Automatically requests Administrator privileges
* 📦 Installs applications automatically using `winget`
* ⚡ Uses silent installation where supported
* 📜 Saves command output to a log file
* 🛠️ Launches Chris Titus Tech's WinUtil
* 🖥️ Designed for fresh Windows installations
* 🐍 Written in Python

## Applications Installed

The current version installs:

* Google Chrome
* Notepad++
* Visual Studio Code
* Microsoft PowerShell
* 7-Zip
* Discord PTB
* Steam
* VideoLAN VLC
* Git
* OpenVPN Connect
* Cloudflare WARP
* Oracle VirtualBox
* Python
* Roblox

Some Microsoft Store applications may also be included depending on their Winget package ID.

## Requirements

* Windows 10 or Windows 11
* Python 3
* Administrator privileges
* Internet connection
* Windows Package Manager (`winget`)

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/WinBloat.git
```

Go into the project folder:

```bash
cd WinBloat
```

Run the program:

```bash
python main.py
```

The program will automatically request Administrator privileges if needed.

## How It Works

1. The program checks for Administrator privileges.
2. If Administrator privileges are not available, it requests elevation.
3. The application installation process begins.
4. Applications are installed using `winget`.
5. Command output is saved to `command_output.txt`.
6. Chris Titus Tech's WinUtil is launched.
7. The program exits after completion.

## Building an EXE

You can convert the program into a standalone executable using PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile --uac-admin --name WinBloat main.py
```

The executable will be created inside the `dist` folder.

## Important Notes

* This project executes system-level commands and should be used carefully.
* Administrator privileges are required.
* Application availability depends on Winget repositories.
* Some applications may already be installed and will be skipped by Winget.
* WinUtil is downloaded and executed through PowerShell, so an active internet connection is required.

## Disclaimer

This project is intended for personal use and educational purposes. Always review scripts before running them with Administrator privileges.

This project is not affiliated with Microsoft, Winget, Chris Titus Tech, or any of the applications installed by the script.

## License

This project is licensed under the MIT License.

---

Made with Python for easier Windows setup.
