<<<<<<< HEAD
# -*- coding: utf-8 -*-

=======
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
from flask import Flask, request, jsonify, render_template
from netmiko import ConnectHandler
import json

app = Flask(__name__)

<<<<<<< HEAD
# -------------------------
# Utility
# -------------------------
def load_json(path):
    with open(path, "r") as f:
=======
# -----------------------------
# Utility
# -----------------------------
def load_json(path):
    with open(path) as f:
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

<<<<<<< HEAD
# -------------------------
# Pages
# -------------------------
=======
# -----------------------------
# Pages
# -----------------------------
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

<<<<<<< HEAD
# -------------------------
# APIs
# -------------------------
=======
# -----------------------------
# APIs
# -----------------------------
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
@app.route("/api/bngs")
def get_bngs():
    return jsonify(load_json("data/bngs.json"))

@app.route("/api/settings", methods=["GET", "POST"])
def settings_api():
    if request.method == "GET":
        return jsonify({
            "bngs": load_json("data/bngs.json"),
            "credentials": load_json("data/credentials.json"),
            "commands": load_json("data/commands.json")
        })

    data = request.json
    save_json("data/bngs.json", data["bngs"])
    save_json("data/credentials.json", data["credentials"])
    save_json("data/commands.json", data["commands"])
<<<<<<< HEAD
    return jsonify({"status": "saved"})

# -------------------------
# VALIDATION (FIXED)
# -------------------------
=======

    return jsonify({"status": "saved"})

# -----------------------------
# VALIDATION (NETMIKO CORE)
# -----------------------------
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
@app.route("/api/validate", methods=["POST"])
def validate():
    req = request.json
    selected_bngs = req.get("bngs", [])

    if not selected_bngs:
        return jsonify([])

<<<<<<< HEAD
    bngs = load_json("data/bngs.json")
=======
    all_bngs = load_json("data/bngs.json")
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
    creds = load_json("data/credentials.json")
    commands = load_json("data/commands.json")

    results = []

<<<<<<< HEAD
    for bng in bngs:
=======
    for bng in all_bngs:
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
        if bng["name"] not in selected_bngs:
            continue

        try:
            device = {
                "device_type": "juniper_junos",
                "host": bng["ip"],
                "username": creds["username"],
                "password": creds["password"],
<<<<<<< HEAD
                "timeout": 15,
                "conn_timeout": 15,
                "auth_timeout": 15,
                "banner_timeout": 15,
=======
                "timeout": 20,
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
            }

            conn = ConnectHandler(**device)

            for cmd in commands:
<<<<<<< HEAD
                # 🔑 KEY FIX: timing-based command
                output = conn.send_command_timing(
                    cmd,
                    strip_prompt=True,
                    strip_command=True
=======
                output = conn.send_command(
                    cmd,
                    expect_string=r"#",
                    strip_prompt=False,
                    strip_command=False
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
                )

                results.append({
                    "bng": bng["name"],
                    "command": cmd,
                    "status": "PASS" if output.strip() else "FAIL",
                    "output": output.strip() or "No output"
                })

            conn.disconnect()

        except Exception as e:
            results.append({
                "bng": bng["name"],
<<<<<<< HEAD
                "command": "ERROR",
=======
                "command": "CONNECTION ERROR",
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
                "status": "FAIL",
                "output": str(e)
            })

    return jsonify(results)

<<<<<<< HEAD
# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
=======
# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
>>>>>>> fea08afaff694b15e8d9d1aa3ed50c49ef291eb9
