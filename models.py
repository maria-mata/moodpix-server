import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)

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

    def generate_auth_token(self, secret):
        s = Serializer(secret, expires_in = 600)
        response = s.dumps({ 'id': self.id })
        return json.dumps(response.decode('utf-8'))

    @staticmethod
    def verify_auth_token(token, secret):
        s = Serializer(secret)
        try:
            decoded = json.loads(token).encode('utf8')
            user = s.loads(decoded)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return user['id']


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
