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
        return '<Users {}'.format(self.username)


class Videos(db.Model):
    '__videos__'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.TEXT, unique=True)
    link = db.Column(db.String)
    author = db.Column(db.TEXT)
    create_date = db.Column(db.TIMESTAMP)
    comments = db.relationship('Comments', backref='title', lazy='dynamic')

    @staticmethod
    def get_comments():
        return Query.query.filter_by(video_id=videos.id).order_by(Comments.timestamp.desc())

    def __init__(self, title, link, author):
        self.title = title
        self.link = link
        self.author = author
        self.create_date = datetime.now()

    def __repr__(self):
        return '<Videos {}>'.format(self.title)


class Comments(db.Model):
    '__comments__'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.TIMESTAMP)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))

    def __repr__(self):
        return 'Comments {}>'.format(self.body)
