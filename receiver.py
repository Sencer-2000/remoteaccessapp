import time
import requests
import subprocess
import logging
import webbrowser
import psutil
import threading

logging.basicConfig(level=logging.INFO)

SERVER = "http://127.0.0.1:5000"

COMMAND_URL = SERVER + "/get_command"
REPORT_URL = SERVER + "/report"


# -------------------------
# PROCESS LIST
# -------------------------
def get_running_apps():
    apps = []
    for p in psutil.process_iter(['pid', 'name']):
        try:
            apps.append({
                "pid": p.info['pid'],
                "name": p.info['name']
            })
        except:
            pass
    return apps


# -------------------------
# KILL PROCESS
# -------------------------
def kill_process(identifier):
    for p in psutil.process_iter(['pid', 'name']):
        try:
            if str(p.info['pid']) == identifier or p.info['name'] == identifier:
                p.kill()
                logging.info(f"Killed: {identifier}")
        except:
            pass


# -------------------------
# COMMAND HANDLER
# -------------------------
def process_command(cmd):
    if not cmd:
        return

    if cmd == "pc-kapat":
        subprocess.run("shutdown -s -t 1", shell=True)

    elif cmd.startswith("link:"):
        webbrowser.open_new_tab(cmd[5:].strip())

    elif cmd.startswith("kill:"):
        kill_process(cmd[5:].strip())


# -------------------------
# AUTO REPORT LOOP
# -------------------------
def report_loop():
    while True:
        try:
            apps = get_running_apps()
            requests.post(REPORT_URL, json={"apps": apps}, timeout=3)
        except Exception as e:
            logging.error(f"report error: {e}")

        time.sleep(2)


# -------------------------
# COMMAND LOOP
# -------------------------
def command_loop():
    last_cmd = None

    while True:
        try:
            r = requests.get(COMMAND_URL, timeout=3)
            cmd = r.json().get("message")

            if cmd != last_cmd:
                logging.info(f"CMD: {cmd}")
                process_command(cmd)
                last_cmd = cmd

        except Exception as e:
            logging.error(f"cmd error: {e}")

        time.sleep(2)


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    threading.Thread(target=report_loop, daemon=True).start()
    command_loop()
