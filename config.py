import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/test.db'.format(os.path.join(BASEDIR))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "SECRET"
db = SQLAlchemy(app=app)
