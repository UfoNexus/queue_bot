from peewee import BooleanField, Model, SqliteDatabase

db = SqliteDatabase('queue.db')


class Session(Model):
    is_active = BooleanField(default=True)

    class Meta:
        database = db
