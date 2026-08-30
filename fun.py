import subprocess
import ctypes
import sys
import os
import time


def check_admin() -> bool:
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

    if not is_admin:
        print("[+] Trying to get admin permissions...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        time.sleep(1)
        return False  
            
    print("[+] You have admin permissions. Starting the script...")
    return True 

def run_cmd(cmd_list):
    cmd_log = []
    cmd = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", cmd_list]
    runs = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    current_line = []
    while True:
        char = runs.stdout.read(1)
        
        if char == "" and runs.poll() is not None:
            break
            
        if char:
            print(char, end="", flush=True) 
            current_line.append(char)
            
            if char in ("\n", "\r"):
                cmd_log.append("".join(current_line))
                current_line = []

    if current_line:
        cmd_log.append("".join(current_line))

    return_code = runs.wait()

    with open("command_output.txt", "a", encoding="utf-8") as log_file:
        log_file.writelines(cmd_log)
        
    return return_code

def run_chris_titus():
    print("\n[+] Launching Chris Titus WinUtil GUI...")
    subprocess.run(["powershell.exe", "-Command", "irm christitus.com/win | iex"])
    print("[+] WinUtil closed. Continuing script...")

def app_process():
    apps_to_isntall = [
        "Google.Chrome",
        "Notepad++.Notepad++",
        "Microsoft.VisualStudioCode",
        "Microsoft.PowerShell",
        "7zip.7zip",
        "Discord.Discord.PTB",
        "Valve.Steam",
        "9P8LTPGCBZXD",
        "VideoLAN.VLC",
        "Git.Git",
        "OpenVPNTechnologies.OpenVPNConnect",
        "Cloudflare.Warp",
        "Oracle.VirtualBox",
        "Python.Python.3",
        "Roblox.Roblox"
    ]
    print("[+]Installing Phase")
    for app in apps_to_isntall:
        print(f"[+]Installing {app}")
        win_cmd = f"winget install --id {app} --silent --accept-source-agreements --accept-package-agreements --exact"
        run_cmd(win_cmd)
 
