from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATABASE.db'
app.config['UPLOAD_FOLDER'] = './server/static/uploads/'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import sharespace.views
import server.database
