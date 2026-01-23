from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)
clicker_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fast_autoclicker.py")

if __name__ == "__main__" and os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    subprocess.Popen(["python", clicker_script])
    print("fast_autoclicker.py launched!")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
