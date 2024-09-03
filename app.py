from flask import Flask, render_template, request, request
from werkzeug.security import generate_password_hash
from config import User

app = Flask(__name__)


# ユーザー登録フォームの表示
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if (
            not request.form["name"]
            or not request.form["password"]
            or not request.form["email"]
            or not request.form["gender"]
        ):
            return render_template(request.url)
        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            gender=request.form["gender"],
            store=request.form["store"],
        )
        return render_template("index.html")
    return render_template("register.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
