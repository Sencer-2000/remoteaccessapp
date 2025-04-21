from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# En son gönderilen komutu burada tutacağız
latest_command = {"message": None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_json', methods=['POST'])
def send_json():
    global latest_command
    data = request.get_json()
    latest_command = data  # Komutu saklıyoruz
    return jsonify({"status": "success", "message": "Komut kaydedildi."})

# Receiver bu endpoint üzerinden komutları çekecek
@app.route('/get_command', methods=['GET'])
def get_command():
    global latest_command
    # Komut döndürülüp sıfırlanabilir
    command = latest_command
    latest_command = {"message": None}
    return jsonify(command)

if __name__ == '__main__':
    app.run(debug=True)
