from flask import Flask, render_template, request, jsonify
from models import db, User
# from cerberus import Validator
# schema = {
#     'username': {'type': 'string'},
#     'email': {'type': 'string'},
#     'password': {'type': 'string'}
# }

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

# @app.route('/signin', methods=['POST'])

# @app.route('/gallery/<user_id>', methods=['GET', 'PUT', 'DELETE']) ??? where to put the auth?

# Helper functions
# def valid_signup(username, email, password):
# how to do this????

if __name__ == '__main__':
    app.run(debug=True)
