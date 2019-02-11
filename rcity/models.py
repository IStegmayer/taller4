from datetime import datetime
from time import strftime

from rcity import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from rcity import db 


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    #TODO: poner largos de los campos correspondientes a los de  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    replays = db.relationship('Replay', backref='author', lazy='dynamic')
    likedReplays(db.Column())
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Replay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    replayFile = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(1000))
    tag = db.Column(db.String(15))
    likes = db.Column(db.Integer, default=0)
    user_name = db.Column(db.String(80), db.ForeignKey('user.username'))


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name':          self.replayFile[:-7],
           'timeStamp':      self.date.strftime('%m/%d/%Y'),
           'authorName':    self.user_name,
           'description':   self.description,
           'tag':           self.tag,
           'likes':         self.likes
       }

    @staticmethod
    def newest(num):
        return Replay.query.order_by(Replay.date.desc()).limit(num)

    def __repr__(self):
        return "<Replay '{}': '{}'>".format(self.description, self.replayFile)