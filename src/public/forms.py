__author__ = 'student'


import re


from wtforms.fields import BooleanField, TextField, PasswordField, StringField,HiddenField, IntegerField
from wtforms.validators import EqualTo, Email, InputRequired, Length
from flask.ext.wtf import Form
from ..data.models import User,Device_List
from ..fields import Predicate
from wtforms.ext.sqlalchemy.orm import model_form
def email_is_available(email):
    if not email:
        return True
    return not User.find_by_email(email)

def username_is_available(username):
    if not username:
        return True
    return not User.find_by_username(username)

def safe_characters(s):
    " Only letters (a-z) and  numbers are allowed for usernames and passwords. Based off Google username validator "
    if not s:
        return True
    return re.match(r'^[\w]+$', s) is not None

class DeviceFormNew(Form):
    popisek = TextField('Device', validators=[
        Predicate(safe_characters, message="Please use only letters (a-z) and numbers"),
        Length(min=6, max=30, message="Please use between 6 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])
    value = StringField('Hash device')
    user_id = HiddenField()



class EmailForm(Form):
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        InputRequired(message="You can't leave this empty")
    ])

class LoginForm(EmailForm):
    password = PasswordField('Password', validators=[
        InputRequired(message="You can't leave this empty")
    ])

    remember_me = BooleanField('Keep me logged in')

class ResetPasswordForm(Form):
    password = PasswordField('New password', validators=[
        EqualTo('confirm', message='Passwords must match'),
        Predicate(safe_characters, message="Please use only letters (a-z) and numbers"),
        Length(min=6, max=30, message="Please use between 6 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])

    confirm = PasswordField('Repeat password')

class Formular(Form):
    cislo1 = IntegerField('Zadej  cislo 1', validators=[Predicate(safe_characters, message="Please use only numbers"),
        Length(min=1, max=20, message="Please use between 1 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])

    cislo2 = IntegerField('Zadej cislo 2', validators=[
        Predicate(safe_characters, message="Please use only numbers"),
        Length(min=1, max=20, message="Please use between 1 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])























