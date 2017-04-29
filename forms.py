from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, TextAreaField


# TODO: RegisterForm
class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[validators.Length(min=1, max=80)])
    username = StringField(label='Username', validators=[validators.Length(min=1, max=80)])
    email = StringField(label='Email', validators=[validators.Length(min=1, max=120)])
    password = PasswordField(label='Password',
                             validators=[
                                 validators.DataRequired(),
                                 validators.EqualTo('confirm', 'Passwords do not match')
                             ])
    confirm = PasswordField('Confirm Password')


# TODO: ArticleForm
class ArticleForm(FlaskForm):
    title = StringField(label='Title', validators=[validators.Length(min=1, max=200)])
    body = TextAreaField(label='Body', validators=[validators.Length(min=30)])
