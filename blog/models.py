from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from sqlalchemy.orm import backref

login=LoginManager()
db=SQLAlchemy()

class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(60),unique=True)
    username=db.Column(db.String(60),unique=False)
    password=db.Column(db.String(),unique=False)
    posts=db.relationship('Posts',backref='users')
    def check_password(self,password):
        if self.password==password:
            return True

        else:
             return False   

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    title=db.Column(db.Text)
    text=db.Column(db.Text,nullable=False)



