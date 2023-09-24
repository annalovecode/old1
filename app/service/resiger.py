from exts import db
from app.model import User


def addUser(data):
    username = data['username']
    password = data['password']
    password_re = data['password_re']
    if password != password_re:
        return '103'
    email = data['email']
    age = data['age']
    if age is '':
        age = '0';
    user = User.query.filter_by(username=username).first()
    if user is None:
        try:
            user_add = User(username=username, password=password, age=int(age), emailAddress=email)
            db.session.add(user_add)
            db.session.commit()
        except Exception as e:
            print(e)
            return '101'
        else:
            return '200'
    else:
        return '100'
