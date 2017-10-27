import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, User, Image
from api import tone_analyzer
from s3 import *

app = Flask(__name__)
CORS(app)

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
    data = request.json
    # if valid_signup(data['username'], data['email'], data['password']):
    newuser = User(data['username'], data['email'], data['password'])
    db.session.add(newuser)
    db.session.commit()
    response = {'status': 1, 'message': 'Success!'}
    return jsonify(response)
    # else:
    #     result = {'status': 0, 'message': 'Error'}
    #     return result

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    user = User.query.filter_by(username = data['username']).first()
    if user is not None and user.check_password(data['password']):
        response = {'status': 1, 'message': 'Success!'}
        return jsonify(response)
    else:
        response = {'status': 0, 'message': 'Error'}
        return jsonify(response)

@app.route('/images/<user_id>', methods=['GET', 'POST'])
def images(user_id):
    if request.method == 'GET':
        images = Image.query.filter_by(user_id = user_id)
        response = [image.serialize for image in images]
        return jsonify(response)
    elif request.method == 'POST':
        data = request.json
        newimage = Image(user_id, data['url'], data['name'], data['description'])
        db.session.add(newimage)
        db.session.commit()
        response = {'status': 1, 'message': 'Success!'}
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True)
