from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:linhtong123@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = True

db = SQLAlchemy(app=app)