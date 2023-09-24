from flask import session

from app import app
from exts import db
from app.model import User
from datetime import timedelta


def userLogin(data):
    username_data = data['username']
    password = data['password']

    imgCode = data['vercode'].lower()
    # 比较验证码
    if imgCode != session.get('imageCode').lower():
        return '201'
    user = User.query.filter_by(username=username_data).first()
    email = User.query.filter_by(emailAddress=username_data).first()
    if (user or email) is None:
        return 'false'
    elif user is None:
        if email.password == password:
            session['username'] = email.username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=10)
            return 'success'
        else:
            return 'false'
    elif email is None:
        if user.password == password:
            session['username'] = user.username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=10)
            return 'success'
        else:
            return 'false'
    else:
        return 'false'
