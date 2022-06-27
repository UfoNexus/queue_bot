from peewee import BooleanField, Model, SqliteDatabase

db = SqliteDatabase('queue.db')


class Session(Model):
    is_active = BooleanField(default=False)

    class Meta:
        database = db
