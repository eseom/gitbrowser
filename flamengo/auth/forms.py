from wtforms import Form, StringField, PasswordField
from wtforms.validators import required


class LoginForm(Form):
    email = StringField('Text', [required()])
    password = PasswordField('Password', [required()])


class JoinForm(Form):
    email = StringField('Email', [required()])