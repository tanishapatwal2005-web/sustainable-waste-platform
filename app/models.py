from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')
    points = db.Column(db.Integer, default=0)

    def is_admin(self):
        return self.role == 'admin'


class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    video = db.Column(db.String(500))
    user = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)