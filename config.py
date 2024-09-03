from peewee import SqliteDatabase, Model, IntegerField, CharField, TextField

db = SqliteDatabase("db.sqlite")


class User(Model):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = TextField()
    gender = CharField()
    store = CharField()

    class Meta:
        database = db
        table_name = "users"


db.create_tables([User])
