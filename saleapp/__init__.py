from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'ff53435###okmdfkjg^*#djfds'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:linhtong123@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

admin = Admin(app=app, name="Quan ly nha sach",template_mode="bootstrap4")