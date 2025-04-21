import time
import requests
import subprocess
import logging
import webbrowser

logging.basicConfig(level=logging.INFO)

# Server.py'nin adresi (IP adresini veya hostname yazmalısın)
SERVER_URL = "http://127.0.0.1:5000/get_command"  # BURAYI server.py'nin çalıştığı bilgisayara göre düzenle

def process_command(message):
    if message == 'pc-kapat':
        logging.info("PC kapatılıyor...")
        subprocess.run("shutdown -s", shell=True)
    elif message.startswith("link:"):
        link = message[5:].strip()
        logging.info(f"Link açılıyor: {link}")
        webbrowser.open_new_tab(link)
    elif message.startswith("isim:"):
        name = message[5:].strip()
        logging.info(f"İsim alındı: {name}")
        subprocess.run(f"konfeti.exe {name}", shell=True)
    else:
        logging.info("Yeni komut yok veya geçersiz.")

def main():
    while True:
        try:
            response = requests.get(SERVER_URL)
            data = response.json()
            message = data.get("message")
            if message:
                process_command(message)
        except Exception as e:
            logging.error(f"Komut alınamadı: {e}")
        
        time.sleep(5)  # Her 5 saniyede bir komut kontrol et

if __name__ == "__main__":
    main()
