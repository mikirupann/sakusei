import datetime
from flask_login import UserMixin
from peewee import SqliteDatabase, Model, IntegerField, CharField, TextField, TimestampField, ForeignKeyField

db = SqliteDatabase("db.sqlite")


class User(UserMixin, Model):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = TextField()
    gender = CharField()
    store = CharField()

    class Meta:
        database = db
        table_name = "users"


class Message(Model):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(User, backref="messages", on_delete="CASCADE")  # 参照先が削除された場合は削除する
    content = TextField()
    pub_date = TimestampField(default=datetime.datetime.now)
    reply_to = ForeignKeyField(
        "self", backref="messages", on_delete="CASCADE", null=True
    )  # 参照先が削除された場合は削除する nullを許容する

    class Meta:
        database = db
        table_name = "messages"


# 都道府県モデルの定義
class Prefecture(Model):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)  # 都道府県名
    area_code = CharField(unique=True)  # 気象庁のエリアコード

    class Meta:
        database = db
        table_name = "prefectures"


db.create_tables([User, Message, Prefecture])
db.pragma("foreign_keys", 1, permanent=True)  # on_deleteを動作させるオプション設定を追加
