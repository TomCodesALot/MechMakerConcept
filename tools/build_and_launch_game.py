#!/usr/bin/env python3
import subprocess
import time
import os
import sys

def main():
    # Kill any old Runner or Igor
    subprocess.run("pkill -9 -f 'Runner.exe' || true", shell=True)
    subprocess.run("pkill -9 -f 'Igor.exe' || true", shell=True)
    subprocess.run("pkill -9 -f 'conhost.exe' || true", shell=True)
    time.sleep(1)

    cmd = [
        "/home/tom/.local/share/Steam/steamapps/common/Proton - Experimental/proton",
        "run",
        "/home/tom/.local/share/Steam/steamapps/compatdata/1670460/pfx/drive_c/ProgramData/GameMakerStudio2-LTS2026/Cache/runtimes/runtime-2026.0.0.23/bin/igor/windows/x64/Igor.exe",
        "-options=C:\\users\\steamuser\\AppData\\Local\\GameMakerStudio2-LTS2026\\GMS2TEMP\\build.bff",
        "-v",
        "--",
        "Windows",
        "Run"
    ]

    env = dict(os.environ)
    env["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = "/home/tom/.local/share/Steam"
    env["STEAM_COMPAT_DATA_PATH"] = "/home/tom/.local/share/Steam/steamapps/compatdata/1670460"
    env["DISPLAY"] = ":0"
    import glob
    xauth_files = glob.glob("/run/user/1000/xauth*")
    if os.environ.get("XAUTHORITY") and os.path.exists(os.environ["XAUTHORITY"]):
        env["XAUTHORITY"] = os.environ["XAUTHORITY"]
    elif xauth_files:
        env["XAUTHORITY"] = max(xauth_files, key=os.path.getmtime)
    elif os.path.exists("/home/tom/.Xauthority"):
        env["XAUTHORITY"] = "/home/tom/.Xauthority" 

    print("[BUILD] Launching Igor compiler via Proton...")
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    start_time = time.time()
    game_window_found = False

    while time.time() - start_time < 90:
        line = proc.stdout.readline()
        if line:
            clean = line.strip()
            if any(k in clean.lower() for k in ["error", "fatal", "compile", "writing", "igor", "saving", "runner", "options"]):
                print(f"[IGOR] {clean}")
        
        # Check if window is open (must have PID != 12332 and match MechMakerConcept)
        res = subprocess.run("wmctrl -l -p", shell=True, stdout=subprocess.PIPE, text=True)
        for l in res.stdout.splitlines():
            parts = l.split()
            if len(parts) >= 4 and "MechMakerConcept" in l and "GameMaker-LTS" not in l:
                pid = parts[2]
                if pid != "12332":
                    print(f"[SUCCESS] Game window detected: {l}")
                    game_window_found = True
                    break
        if game_window_found:
            break
        
        if proc.poll() is not None:
            print(f"[EXIT] Igor process exited with code {proc.returncode}")
            # Igor finished compiling; wait up to 15s for Runner.exe window to manifest
            for wait_i in range(15):
                time.sleep(1)
                res2 = subprocess.run("wmctrl -l -p", shell=True, stdout=subprocess.PIPE, text=True)
                for l in res2.stdout.splitlines():
                    parts = l.split()
                    if len(parts) >= 4 and "MechMakerConcept" in l and "GameMaker-LTS" not in l:
                        pid = parts[2]
                        if pid != "12332":
                            print(f"[SUCCESS] Game window detected post-Igor: {l}")
                            game_window_found = True
                            break
                if game_window_found:
                    break
            break
        time.sleep(0.5)

    if not game_window_found:
        print("[FAIL] Game window was not detected within timeout.")
        sys.exit(1)
    else:
        print("[READY] MechMakerConcept running!")
        sys.exit(0)

if __name__ == "__main__":
    main()
