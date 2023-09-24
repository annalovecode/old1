from datetime import timedelta

from flask import Flask,render_template
from exts import db
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
app.send_file_max_age_default = timedelta(seconds=1)

from app import views

