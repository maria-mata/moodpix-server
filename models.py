from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    pwdhash = db.Column(db.String(54), nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text(2083), nullable = False)
    name = db.Column(db.String(100), unique = True, nullable = False)
    description = db.Column(db.Text(200), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('User', backref = db.backref('images', lazy = True))

    def __init__(self, user_id, url, name, description):
        self.user_id = user_id
        self.url = url
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'description': self.description
        }
