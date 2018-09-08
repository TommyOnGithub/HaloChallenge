#! /usr/bin/python

__author__ = "Thomas Barry"

"""
This module is a web application that allows users to interact with an
underlying SQL database. Database queries are sent via POST using the
SQLAlchemy and the WTForms libraries. This app was created with Flask.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form
from wtforms import TextField
from wtforms import validators


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dict.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Record(db.Model):
    """
    This class represents a "Record" database model object,
    an object with key and value attributes.
    params:
        key (str)
        value (str)
    attributes:
        key (str)
        value (str)
    inherits:
        SQLAlchemy.Model
    """
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(50))

    def __init__(self, key, value):
        """
        Initializes class attributes
        """
        self.key = key
        self.value = value

db.create_all()

class SetForm(Form):
    """
    This class represents a WTForms Form designed for 'setting' key-value
    pairs in the SQL database.
    attributes:
        setter_key (TextField)
        setter_value (TextField)
    inherits:
        Form    Inherits from the Forms class in wtforms
    """
    setter_key = TextField('Key:', validators=[validators.required()])
    setter_value = TextField('Value:', validators=[validators.required()])

class GetForm(Form):
    """
    This class represents a WTForms Form designed for 'getting' key-value
    pairs from the SQL database.
    attributes:
        getter_key (TextField)
    inherits:
        Form    Inherits from the Forms class in wtforms
    """
    getter_key = TextField('Key:', validators=[validators.required()])

def get_message():
    """
    This function is designed to determine and return the most suitable
    message to display to the user.
    returns:
        str: The most appropriate message for the given context.
    """
    return 'Use the forms above to interact with the SQL database.'


@app.route('/')
def index():
    """
    This function builds the view for the main page of the application.
    returns:
        str: The html represented inside the main html file.
    """
    set_form = SetForm(request.form)
    get_form = GetForm(request.form)
    message = get_message()
    return render_template('index.html', get_form=get_form, set_form=set_form, message=message)

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
        db.session.add(Record(key, value))
        db.session.commit()
    else:
        db.session.delete(Record.query.get(key))
        db.session.add(Record(key, value))
        db.session.commit()

    set_form = SetForm(request.form)
    get_form = GetForm(request.form)
    message = 'Database was successfully updated!'
    return render_template('index.html', get_form=get_form, set_form=set_form, message=message)

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

    record = Record.query.get(key)
    if record:
        message = 'The value associated with key "{}" is "{}".'.format(key, record.value)
    else:
        message = 'A record with that key does not exist.'
    
    return render_template('index.html', get_form=get_form, set_form=set_form, message=message)

app.run(debug=True, port=8000, host='0.0.0.0')
