from flask import Flask, request, jsonify, render_template
from netmiko import ConnectHandler
import json

app = Flask(__name__)

# -----------------------------
# Utility
# -----------------------------
def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# Pages
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

# -----------------------------
# APIs
# -----------------------------
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

    return jsonify({"status": "saved"})

# -----------------------------
# VALIDATION (NETMIKO CORE)
# -----------------------------
@app.route("/api/validate", methods=["POST"])
def validate():
    req = request.json
    selected_bngs = req.get("bngs", [])

    if not selected_bngs:
        return jsonify([])

    all_bngs = load_json("data/bngs.json")
    creds = load_json("data/credentials.json")
    commands = load_json("data/commands.json")

    results = []

    for bng in all_bngs:
        if bng["name"] not in selected_bngs:
            continue

        try:
            device = {
                "device_type": "juniper_junos",
                "host": bng["ip"],
                "username": creds["username"],
                "password": creds["password"],
                "timeout": 20,
            }

            conn = ConnectHandler(**device)

            for cmd in commands:
                output = conn.send_command(
                    cmd,
                    expect_string=r"#",
                    strip_prompt=False,
                    strip_command=False
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
                "command": "CONNECTION ERROR",
                "status": "FAIL",
                "output": str(e)
            })

    return jsonify(results)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
