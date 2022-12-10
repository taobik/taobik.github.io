from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'ff53435###okmdfkjg^*#djfds'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:linhtong123@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(
    cloud_name='dascseee2',
    api_key='199886655632112',
    api_secret='I8MAIrtBmIK2pm1-eM45i3U4Ew0'
)
