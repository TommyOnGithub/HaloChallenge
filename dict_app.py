#! /usr/bin/python

"""
This module is a web application that allows users to interact with an
underlying SQL database. Database queries are sent via POST using the
SQLAlchemy and the WTForms libraries. This app was created with Flask.
"""

from flask import (Flask, render_template, request, session,
    redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form
from wtforms import StringField
from wtforms import validators
from werkzeug import generate_password_hash
from werkzeug import check_password_hash
import os


# from models import db
# from models import Record
# from models import User
from forms import SetForm
from forms import GetForm
from forms import SignupForm
from forms import LoginForm

__author__ = "Thomas Barry"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tommy/halo_challenge_app/dict.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.init_app(app)
# db.create_all()

class User(db.Model):
    """
    This model represents a user of the application and handles
    authentication.
    params:
        first_name (str)
        last_name (str)
        email (str)
        password (str)
    attributes:
        uid (SQLAlchemy.Column)
        first_name (SQLAlchemy.Column)
        last_name (SQLAlchemy.Column)
        email (SQLAlchemy.Column)
        pwdhash (SQLAlchemy.Column)
    inherits:
        SQLAlchemy.Model
    """
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.uid

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Record(db.Model):
    """
    This class represents a "Record" database model object,
    an object with key and value attributes.
    params:
        key (str)
        value (str)
    attributes:
        key (SQLAlchemy.Column)
        value (SQLAlchemy.Column)
    inherits:
        SQLAlchemy.Model
    """
    # __tablename__ = 'records'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(50))

    user_email = db.Column(db.String(120), db.ForeignKey('users.email'),
        nullable=False)
    user = db.relationship('User', backref=db.backref('records', lazy=True))

    def __init__(self, key, value, user):
        self.key = key
        self.value = value
        self.user = user


    def __repr__(self):
        return '<Record %r>' % self.key


@app.route('/')
def index():
    """
    This function builds the view for the main page of the application.
    returns:
        str: The html represented inside the main html file.
    """
    if 'email' not in session:
        return redirect(url_for('login'))
    set_form = SetForm(request.form)
    get_form = GetForm(request.form)
    message = 'Use the forms above to interact with the SQL database.'
    return render_template('index.html',
                            get_form=get_form,
                            set_form=set_form,
                            essage=message)

@app.route('/setter_saved', methods=['POST'])
def setter_save():
    """
    This function handles saving user input to the database when the "SET"
    button is pressed.
    returns:
        str: The html represented inside the appropriate html file.
    """
    setter_input = dict(request.form.items())
    key = setter_input['setter_key']
    value = setter_input['setter_value']

    if not Record.query.get(key):
        db.session.add(Record(key, value, User.query.filter_by(email=session['email']).first()))
        db.session.commit()
    else:
        db.session.delete(Record.query.get(key))
        db.session.add(Record(key, value, User.query.filter_by(email=session['email']).first()))
        db.session.commit()

    set_form = SetForm(request.form)
    get_form = GetForm(request.form)
    message = 'Database was successfully updated!'
    return render_template('index.html',
                            get_form=get_form,
                            set_form=set_form,
                            message=message)

@app.route('/get_pressed', methods=['POST'])
def get_pressed():
    """
    This function handles retrieving a value from the database when the "GET"
    button is pressed. Reads in the entered key and re-renders the home page
    with an updated message containing the queried data.
    returns:
        str: The html represented inside the appropriate html file.
    """
    key = dict(request.form.items())['getter_key']
    set_form = SetForm(request.form)
    get_form = GetForm(request.form)
    message = None
    # try:
    record_index = User.query.filter_by(email=session['email']).first().records.index(Record.query.get(key))
    value = User.query.filter_by(email=session['email']).first().records[record_index].value
    message = 'The value for "{}" is "{}".'.format(key, value)
    # except:
    #      message = 'The database is missing or has been renamed.'
    
    if not message:
        message = 'A record with that key does not exist.'
    return render_template('index.html',
                            get_form=get_form,
                            set_form=set_form,
                            message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('index'))
    form = SignupForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data,
                form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('index'))
    form = LoginForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(16)   # '3sf8472910ksgl2894j3jf2j989k2i463'
    db.create_all()
    app.run(debug=True, port=8000, host='0.0.0.0')
