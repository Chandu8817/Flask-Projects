from . import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20),unique=True,nullable =False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50),nullable =False)
    password = db.Column(db.String(25),nullable = False)

    def __repr__(self):
        return '<User %r>' % self.username


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return '<Author %r>' % self.name


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    desciption = db.Column(db.String(1000), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.title



