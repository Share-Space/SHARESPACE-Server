from flask_login import UserMixin
from server import db, login_manager
from datetime import datetime

@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False) # email
    name = db.Column(db.String, unique=True, nullable=False) # name
    password = db.Column(db.String, unique=False, nullable=False) # password

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False) # title
    article = db.Column(db.String, unique=False, nullable=False) # article
    author = db.Column(db.String, unique=False, nullable=False) # author
    image_url = db.Column(db.String, unique=False, nullable=False) # url for image
    time = db.Column(db.DateTime, nullable=False, default=db.func.now()) # timestamp
    tags = db.Column(db.PickleType()) # tags

    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()
