import os, json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, User, Image
from api import tone_analyzer
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)

app = Flask(__name__)
CORS(app)

secret = os.environ['SECRET_KEY']
app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/moodpix'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mood', methods=['POST'])
def analyze_tone():
    data = request.json
    response = json.dumps(tone_analyzer.tone(text = data['text']), indent = 2)
    return jsonify(response)

@app.route('/signup', methods=['POST'])
def signup():
    # need to add validation
    data = request.json
    user = User.query.filter_by(username = data['username']).first()
    email = User.query.filter_by(email = data['email']).first()
    if user is not None or email is not None:
        response = {'error': 'Username or email already in use.'}
        return jsonify(response)
    else:
        newuser = User(data['username'], data['email'], data['password'])
        db.session.add(newuser)
        db.session.commit()
        token = newuser.generate_auth_token(secret)
        response = {'message': 'Success!', 'token': token}
        return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    # need to add validation
    data = request.json
    user = User.query.filter_by(username = data['username']).first()
    if user is not None and user.check_password(data['password']):
        token = user.generate_auth_token(secret)
        response = {'message': 'Success!', 'token': token}
        return jsonify(response)
    else:
        response = {'error': 'Incorrect username or password.'}
        return jsonify(response)

@app.route('/images/<token>', methods=['GET', 'POST'])
def images(token):
    # need to add validation
    user_id = User.verify_auth_token(token, secret)
    if user_id is not None:
        if request.method == 'GET':
            images = Image.query.filter_by(user_id = user_id)
            response = [image.serialize for image in images]
            return jsonify(response)
        elif request.method == 'POST':
            data = request.json
            newimage = Image(user_id, data['url'], data['name'], data['description'])
            db.session.add(newimage)
            db.session.commit()
            response = {'message': 'Success!'}
            return jsonify(response)
    else:
        response = {'error': 'Cannot verify token.'}
        return jsonify(response)

@app.route('/images/<token>/<id>', methods=['DELETE'])
def delete_image(token, id):
    # need to add validation
    user_id = User.verify_auth_token(token, secret)
    if user_id is not None:
        data = request.form
        image = Image.query.filter_by(id = data['id'])
        db.session.delete(image)
        db.session.commit()
        response = {'message': 'Success!'}
        return jsonify(response)
    else:
        response = {'error': 'Cannot verify token.'}
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True)
