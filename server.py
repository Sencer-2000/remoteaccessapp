from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

latest_command = {"message": ""}
latest_apps = []


# -------------------------
# COMMAND SET
# -------------------------
@app.route("/set_command", methods=["POST"])
def set_command():
    global latest_command
    latest_command["message"] = request.json.get("message", "")
    return {"status": "ok"}


# -------------------------
# COMMAND GET
# -------------------------
@app.route("/get_command")
def get_command():
    return jsonify(latest_command)


# -------------------------
# APPS REPORT
# -------------------------
@app.route("/report", methods=["POST"])
def report():
    global latest_apps
    latest_apps = request.json.get("apps", [])
    return {"status": "ok"}


# -------------------------
# APPS FETCH
# -------------------------
@app.route("/apps")
def apps():
    return jsonify(latest_apps)


# -------------------------
# PANEL
# -------------------------
@app.route("/")
def panel():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
