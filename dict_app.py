#! /usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dict.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Record(db.Model):
	key = db.Column(db.String(50), primary_key=True)
	value = db.Column(db.String(50))

	def __init__(self, key, value):
		self.key = key
		self.value = value

db.create_all()

@app.route('/get/<key>')
def get(key=None):
	# TODO
	# Polish return strings
	if key:
		r = Record.query.get(key)
		if r:
			return r.value
		else:
			return 'A record with that key does not exist'
	else:
		return 'key must not be None'

@app.route('/set/<key>/<value>')
def set(key=None, value=None):
	# TODO
	# Test what happens when you try to add an entry that already exists.
	# Polish return strings
	if key and value:
		if not Record.query.get(key):
			db.session.add(Record(key, value))
			db.session.commit()
		else:
			db.session.delete(Record.query.get(key))
			db.session.add(Record(key, value))
			db.session.commit()
		return 'Record successfully added'
	else:
		return 'key and value must not be None'


app.run(debug=True, port=8000, host='0.0.0.0')
