from flask import Flask, redirect, render_template, request
from werkzeug.security import generate_password_hash
from config import User


app = Flask(__name__)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
        )
        return render_template("index.html")
    return render_template("register.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
