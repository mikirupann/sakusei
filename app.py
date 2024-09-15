from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import IntegrityError
from config import User, Message, Prefecture
import requests
from dotenv import load_dotenv
import os
from translate import Translator
import googlemaps
import geocoder
import math

load_dotenv()
weather_api_key = os.getenv("weather_API_key")
map_api_key = os.getenv("map_API_key")


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
    prefectures = Prefecture.select()
    if request.method == "POST":
        prefecture = request.form["prefecture"]
        prefecture = Prefecture.get(Prefecture.name == prefecture)
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
    return render_template("index.html", messages=messages, prefectures=prefectures)


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
    prefectures = Prefecture.select()  # 全都道府県テーブル取得
    weather_data = None
    distance = None
    address = None
    if request.method == "POST":
        prefecture = request.form["prefecture"]
        prefecture = Prefecture.get(Prefecture.name == prefecture)
        code = prefecture.area_code
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?zip={code}&units=metric&appid={weather_api_key}"
        )
        response = requests.get(url)
        # response.raise_for_status()
        jsondata = response.json()

        # 天気データ
        weather_data = {
            "weather": translate_text(jsondata["weather"][0]["main"]),
            "city": (jsondata["name"]),
            "temp": jsondata["main"]["temp"],
        }

        # GoogleMapsAPIキーを設定APIキー
        gmaps = googlemaps.Client(key=map_api_key)
        # 緯度経度を取得
        address = f"ラーメン二郎 {prefecture.name}"
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            koko = [lat, lng]
        else:
            flash(f"住所が見つかりませんでした。")

        # IPアドレスから位置情報を取得
        g = geocoder.ip("me")
        me = [g.latlng[0], g.latlng[1]]
        pole_radius = 6356752.314245  # 極半径
        equator_radius = 6378137.0  # 赤道半径
        lat_me = math.radians(me[0])
        lon_me = math.radians(me[1])
        lat_koko = math.radians(koko[0])
        lon_koko = math.radians(koko[1])
        lat_difference = lat_me - lat_koko  # 緯度差
        lon_difference = lon_me - lon_koko  # 経度差
        lat_average = (lat_me + lat_koko) / 2  # 平均緯度
        e2 = (math.pow(equator_radius, 2) - math.pow(pole_radius, 2)) / math.pow(
            equator_radius, 2
        )  # 第一離心率^2

        w = math.sqrt(1 - e2 * math.pow(math.sin(lat_average), 2))
        m = equator_radius * (1 - e2) / math.pow(w, 3)  # 子午線曲率半径
        n = equator_radius / w  # 卯酉線曲半径
        distance = math.sqrt(
            math.pow(m * lat_difference, 2) + math.pow(n * lon_difference * math.cos(lat_average), 2)
        )  # 距離計測
        distance = round(distance / 1000, 1)

    return render_template(
        "select.html", prefectures=prefectures, weather_data=weather_data, distance=distance, address=address
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
