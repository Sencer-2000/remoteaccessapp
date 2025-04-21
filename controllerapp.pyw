import sys
import webbrowser
import subprocess

if sys.argv[1] == "kapat":
        print("kapatılıyor")
        subprocess.run("shutdown -s -t 1")
if sys.argv[1] == "yaz":
    print(sys.argv[2])
if sys.argv[1] == "isim":
    subprocess.run(f"konfeti.exe {sys.argv[2]}",shell=True)
if sys.argv[1] == "link":
    webbrowser.open_new_tab(sys.argv[2])