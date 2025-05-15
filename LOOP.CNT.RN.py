import subprocess
import time
import os

PYTHON_PATH = r"C:\Users\admin\selenium\venv\Scripts\python.exe"

SCRIPTS = {
    "MAIN.BETA.BIE.py": None,
    "MAIN.BETA.EM.py": None,
    "MAIN.BETA.HAS.py": None,
    "MAIN.BETA.FIW.py": None,
}

def launch_script(script_name):
    print(f"🚀 Launching {script_name}")
    return subprocess.Popen([PYTHON_PATH, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def monitor_scripts():
    while True:
        for script_name in SCRIPTS:
            proc = SCRIPTS[script_name]
            # If process isn't running or has exited
            if proc is None or proc.poll() is not None:
                if proc and proc.poll() is not None:
                    print(f"❌ {script_name} exited with code {proc.returncode}. Restarting...")
                    # Optional: print errors
                    stderr = proc.stderr.read().decode()
                    if stderr:
                        print(f"🔴 Error output from {script_name}:\n{stderr}")
                # Relaunch
                SCRIPTS[script_name] = launch_script(script_name)
        time.sleep(2)

if __name__ == "__main__":
    print("🔁 Auto-restarting loop started.\n")
    monitor_scripts()
