CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

HOST = '0.0.0.0'
PORT = '12306'
DATABASE = 'flask_test'
USERNAME = 'flask'
PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD, host=HOST,port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False