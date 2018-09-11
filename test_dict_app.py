#! /usr/bin/python

import os
import dict_app
import unittest
import tempfile


__author__ = 'Thomas Barry'

class DictAppTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, dict_app.app.config['DATABASE'] = tempfile.mkstemp()
		dict_app.app.testing = True
		self.app = dict_app.app.test_client()
		with dict_app.app.app_context():
			dict_app.init_db()
		dict_app.app.secret_key = os.urandom(16)

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(dict_app.app.config['DATABASE'])

	def test_homepage_redirect(self):
		"""
		This method ensures that when there is no valid session, '/index'
		will redirect back to the log-in page.
		"""
		rv = self.app.get('/')
		assert b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to target URL: <a href="/login">/login</a>.  If not click the link.' in rv.data

	def login(self, email, password):
		"""
		Helper method for logging in
		params:
			email (str): User email address
			password (str): User password
		"""
		return self.app.post('/login', data=dict(
			email=email,
			password=password
		), follow_redirects=True)

	def logout(self):
		"""
		Helper method for logging out
		"""
		return self.app.get('/logout', follow_redirects=True)

	def test_login_logout(self):
		"""
		This method ensures that logging in and logging out works, and that it's
		not possible to log in with invalid credentials.
		"""
		rv = self.login('test@example.com', 'password')
		assert b'<p>Enter a key-value pair and press "SET" to commit.</p>\n' in rv.data
		rv = self.logout()
		assert b'<form method="POST" action="/login">\n\n' in rv.data
		rv = self.login('tast@example.com', 'password')
		assert b'<form method="POST" action="/login">' in rv.data
		rv = self.login('test@example.com', 'possword')
		assert b'<form method="POST" action="/login">' in rv.data

	def test_setter_getter(self):
		"""
		This method ensures that Key, Value pairs are persisted and updated 
		properly via the Setter form and returned properly via the Getter form.
		"""
		self.login('test@example.com', 'password')
		rv = self.app.post('/setter_saved', data=dict(
			setter_key='TestKey',
			setter_value='TestValue'
		), follow_redirects=True)
		assert b'Database was successfully updated!' in rv.data
		rv = self.app.post('/get_pressed', data=dict(
			getter_key='TestKey',
		), follow_redirects=True)
		assert b'The value for &#34;TestKey&#34; is &#34;TestValue&#34;.' in rv.data
		rv = self.app.post('/setter_saved', data=dict(
			setter_key='TestKey',
			setter_value='TestValueUpdate'
		), follow_redirects=True)
		assert b'Database was successfully updated!' in rv.data
		rv = self.app.post('/get_pressed', data=dict(
			getter_key='TestKey',
		), follow_redirects=True)
		assert b'The value for &#34;TestKey&#34; is &#34;TestValueUpdate&#34;.' in rv.data


if __name__ == "__main__":
	unittest.main()
