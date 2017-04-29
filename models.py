from datetime import datetime

from config import db


class Users(db.Model):
    '__users__'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(80))
    username = db.Column(db.TEXT(80), unique=True)
    email = db.Column(db.TEXT(120), unique=True)
    password = db.Column(db.TEXT(120))

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {}'.format(self.username)


class Articles(db.Model):
    '__articles__'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.TEXT, unique=True)
    body = db.Column(db.TEXT)
    author = db.Column(db.TEXT)
    create_date = db.Column(db.TIMESTAMP)

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author
        self.create_date = datetime.now()

    def __repr__(self):
        return '<Articles {}'.format(self.title)
