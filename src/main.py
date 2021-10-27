from datetime import datetime, timedelta
from flask import Flask
from flask.helpers import make_response
from flask import request, flash, redirect, url_for
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
from urllib.parse import parse_qs
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:root@localhost/pythonAssignment3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretsecretsecretsecretsecret'
db = SQLAlchemy(app)


@app.route('/login', methods=['POST', 'GET'])
def login():

    auth = request.authorization

    if auth:
        user = User.query.filter_by(login=auth.username).first()

        if not user:
            flash('Please check your login details and try again.')
            return make_response('Could not verify!', 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required'
                                 })

        userLogin = \
            User.query.filter_by(login=auth.username).first().login
        userPass = \
            User.query.filter_by(login=auth.username).first().password

        if userPass != auth.password:
            flash('Please check your login details and try again.')
            return make_response('Could not verify!', 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required'
                                 })

        token = jwt.encode({'user': auth.username,
                           'exp': datetime.utcnow()
                           + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        user.token = token
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('protected', token=user.token))

    return make_response('Could not verify!', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required'
                         })


@app.route('/protected')
def protected():

    parsed_url = urlparse(request.url)
    captured_value = parse_qs(parsed_url.query)['token'][0]
    user = User.query.filter_by(token=captured_value).first()
    if user:
        return '<h1>Hello, token which is provided is correct {}</h1>'.format(captured_value)
    return '<h1>Hello, Could not verify the token</h1>'


class User(db.Model):

    __tablename__ = 'User'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column('login', db.String(100), unique=True)
    password = db.Column('password', db.String(100))
    token = db.Column('token', db.String)

    def __init__(
        self,
        login,
        password,
        token,
        ):
        self.login = login
        self.password = password
        self.token = token


db.drop_all()
db.create_all()

testUser1 = User(login='testUser1', password='password', token='')
testUser2 = User(login='testUser2', password='password', token='')
testUser3 = User(login='testUser3', password='password', token='')
testUser4 = User(login='testUser4', password='password', token='')
testUser5 = User(login='testUser5', password='password', token='')

db.session.add(testUser1)
db.session.add(testUser2)
db.session.add(testUser3)
db.session.add(testUser4)
db.session.add(testUser5)

db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
