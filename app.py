from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    if request.method == "POST":
        letter = request.form.get("letter", "")
        message = f"You pasted {len(letter)} characters."
    return render_template("index.html", message=message)