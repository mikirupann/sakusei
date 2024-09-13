from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import IntegrityError
from config import User, Message, Prefecture
import requests
from dotenv import load_dotenv
import os
from translate import Translator

load_dotenv()
api_key = os.getenv("API_key")


app = Flask(__name__)
app.secret_key = "secret"  # 秘密鍵
login_manager = LoginManager()
login_manager.init_app(app)


# Flask-Loginがユーザー情報を取得するためのメソッド
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# ログインしていないとアクセスできないページにアクセスがあった場合の処理
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


# ユーザー登録フォームの表示・登録処理
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # データの検証
        if not request.form["name"] or not request.form["password"] or not request.form["email"]:
            flash("※未入力の項目があります※")
            return redirect(request.url)
        if User.select().where(User.name == request.form["name"]):
            flash("※その名前はすでに使われています※")
            return redirect(request.url)
        if User.select().where(User.email == request.form["email"]):
            flash("※そのメールアドレスはすでに使われています※")
            return redirect(request.url)
        # ユーザー登録
        try:
            User.create(
                name=request.form["name"],
                email=request.form["email"],
                password=generate_password_hash(request.form["password"]),
                gender=request.form["gender"],
                store=request.form["store"],
            )
            flash("登録完了しました！！")
            return render_template("index.html")
        except IndentationError as e:
            flash(f"{e}")
    return render_template("register.html")


# ログインフォームの表示
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form["password"] or not request.form["email"]:
            flash("※未入力の項目があります※")
            return redirect(request.url)
        # ここでユーザーを認証し、OKならログインする
        user = User.select().where(User.email == request.form["email"]).first()
        if user is not None and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash(f"{user.name} さん ログイン中")
            return redirect(url_for("index"))

    return render_template("login.html")


# ログアウト処理
@app.route("/logout")
@login_required
def logout():
    # ログインしていない場合の処理
    if not current_user.is_authenticated:
        return "ログインしていません"
    logout_user()
    flash("ログアウトしました！")
    return redirect(url_for("index"))


# ユーザー削除処理
@app.route("/unregister")
@login_required
def unregister():
    current_user.delete_instance()
    logout_user()
    return redirect(url_for("index"))


# メッセージ登録フォームの表示・投稿・一覧表示
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and current_user.is_authenticated:
        if not request.form["content"]:
            flash("Message を入力してください")
            return redirect(request.url)
        Message.create(user=current_user, content=request.form["content"])
    messages = (
        Message.select()
        .where(Message.reply_to.is_null(True))
        .order_by(Message.pub_date.desc(), Message.id.desc())
    )
    return render_template("index.html", messages=messages)


# メッセージ削除
@app.route("/messages/<message_id>/delete/", methods=["POST"])
@login_required
def delete(message_id):
    if Message.select().where((Message.id == message_id) & (Message.user == current_user)).first():
        Message.delete_by_id(message_id)
    else:
        flash("無効な操作です")
    return redirect(request.referrer)


# 返信表示
@app.route("/messages/<message_id>/")
def show(message_id):
    messages = (
        Message.select()
        .where((Message.id == message_id) | (Message.reply_to == message_id))
        .order_by(Message.pub_date.desc())
    )
    if messages.count() == 0:
        return redirect(url_for("index"))
    return render_template("show.html", messages=messages, message_id=message_id)


# 返信登録
@app.route("/messages/<message_id>/", methods=["POST"])
@login_required
def reply(message_id):
    Message.create(user=current_user, content=request.form["content"], reply_to=message_id)
    return redirect(url_for("show", message_id=message_id))


def translate_text(text, target_lang="ja"):
    translator = Translator(to_lang=target_lang)
    return translator.translate(text)


@app.route("/select", methods=["GET", "POST"])
def select():
    prefectures = Prefecture.select()  # 全都道府県を取得
    weather_data = None
    if request.method == "POST":
        prefecture = request.form["prefecture"]

        prefecture = Prefecture.get(Prefecture.name == prefecture)
        code = prefecture.area_code

        url = f"https://api.openweathermap.org/data/2.5/weather?zip={code}&units=metric&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        jsondata = response.json()

        # 必要な天気データの抽出
        weather_data = {
            "weather": translate_text(jsondata["weather"][0]["main"]),
            "description": translate_text(jsondata["weather"][0]["description"]),
            "city": translate_text(jsondata["name"]),
            "temp": jsondata["main"]["temp"],
        }

    return render_template("select.html", prefectures=prefectures, weather_data=weather_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
