import subprocess
import ctypes
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
APPS_FILE = SCRIPT_DIR / "apps.txt"
WINUTIL_CONFIG_FILE = SCRIPT_DIR / "winutil-config.json"


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
    runs = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    screen_line = []
    redrawing = False
    
    while True:
        char = runs.stdout.read(1)

        if char == "" and runs.poll() is not None:
            break

        if char:
            print(char, end="", flush=True)

            if char == "\r":
                # A carriage return redraws the current terminal line.
                redrawing = True
            elif char == "\n":
                line = "".join(screen_line)
                cmd_log.append(line + "\n")
                screen_line = []
                redrawing = False
            else:
                if redrawing:
                    # Keep CRLF text intact, but replace the previous frame
                    # as soon as the next progress redraw begins.
                    screen_line = []
                    redrawing = False
                screen_line.append(char)

    if screen_line:
        cmd_log.append("".join(screen_line))

    return_code = runs.wait()

    with open("command_output.txt", "a", encoding="utf-8") as log_file:
        log_file.writelines(cmd_log)
        
    return return_code 

def run_chris_titus():
    print("\n[+] Applying Chris Titus WinUtil configuration...")

    if not WINUTIL_CONFIG_FILE.is_file():
        print(f"[!] WinUtil config file not found: {WINUTIL_CONFIG_FILE}")
        return 1

    config_path = str(WINUTIL_CONFIG_FILE).replace("'", "''")
    winutil_cmd = (
        "& ([ScriptBlock]::Create((irm 'https://christitus.com/win'))) "
        f"-Config '{config_path}'"
    )
    return_code = run_cmd(winutil_cmd)
    if return_code == 0:
        print("[+] WinUtil configuration applied.")
    else:
        print(f"[!] WinUtil configuration failed with exit code {return_code}.")
    return return_code


def load_apps():
    if not APPS_FILE.is_file():
        raise FileNotFoundError(f"App list file not found: {APPS_FILE}")

    apps = []
    with APPS_FILE.open("r", encoding="utf-8") as app_file:
        for line in app_file:
            app = line.strip()
            if app and not app.startswith("#"):
                apps.append(app)

    if not apps:
        raise ValueError(f"No app IDs found in {APPS_FILE}")

    return apps


def app_process():
    apps_to_install = load_apps()
    print("[+] Installing Phase")
    for app in apps_to_install:
        print(f"[+]Installing {app}")
        win_cmd = f"winget install --id {app} --silent --accept-source-agreements --accept-package-agreements --exact"
        run_cmd(win_cmd)
 
