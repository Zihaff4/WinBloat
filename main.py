import os
import time
import subprocess
import ctypes
import sys
from fun import check_admin, app_process, run_chris_titus
print("-------Welcome to Post-isntaller tool-------")

print("[+]Checking the Perm lavel")
admin_check_status = check_admin()
if not admin_check_status:
    sys.exit(0)
    

script_status = True
try:
    while script_status:
        print("[+]Script has started ")

        app_process()
        run_chris_titus()
        time.sleep(2)
        script_status = False   
except KeyboardInterrupt:
    print("Exiting....")
    sys.exit(0)

script_status = False    