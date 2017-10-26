from flask import Flask, render_template, request, jsonify
from models import db, User, Image
import os
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/moodpix'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    # if valid_signup(data['username'], data['email'], data['password']):
    newuser = User(data['username'], data['email'], data['password'])
    db.session.add(newuser)
    db.session.commit()
    result = {'status': 1, 'message': 'Success!'}
    return jsonify(result)
    # else:
    #     result = {'status': 0, 'message': 'Error'}
    #     return result

@app.route('/signin', methods=['POST'])
def signin():
    data = request.form
    # validate signin here?
    user = User.query.filter_by(username = data['username']).first()
    if user is not None and user.check_password(data['password']):
        result = {'status': 1, 'message': 'Success!'}
        return jsonify(result)
    else:
        result = {'status': 0, 'message': 'Error'}
        return jsonify(result)

# @app.route('/images/<user_id>', methods=['GET', 'POST'])
# def images(user_id):
    # if request.method == 'GET':
        # get all songs for the user
    # elif request.method == 'POST':
        # post the song into the db


if __name__ == '__main__':
    app.run(debug=True)
