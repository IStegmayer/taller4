from datetime import datetime

from rcity import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    replays = db.relationship('Replay', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Replay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    replayFile = db.Column(db.LargeBinary, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(1000))
    tag = db.Column(db.String(15))
    rating = db.Column(db.Float(), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


