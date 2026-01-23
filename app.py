from flask import Flask, render_template, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

clicker_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clicker/start", methods=["POST"])
def start_clicker():
    global clicker_process

    if clicker_process is None:
        clicker_process = subprocess.Popen(
            ["python", "fast_autoclicker.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        return jsonify(status="STARTED")

    return jsonify(status="ALREADY RUNNING")

@app.route("/clicker/stop", methods=["POST"])
def stop_clicker():
    global clicker_process

    if clicker_process:
        clicker_process.send_signal(signal.SIGTERM)
        clicker_process = None
        return jsonify(status="STOPPED")

    return jsonify(status="NOT RUNNING")

if __name__ == "__main__":
    app.run(debug=True)
