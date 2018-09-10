from wtforms import (Form, validators, StringField,
	PasswordField, SubmitField)



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
    setter_key = StringField('Key:', validators=[validators.DataRequired("You must specify a key!")])
    setter_value = StringField('Value:', validators=[validators.DataRequired("You must specify a value!")])

class GetForm(Form):
    """
    This class represents a WTForms Form designed for 'getting' key-value
    pairs from the SQL database.
    attributes:
        getter_key (TextField)
    inherits:
        Form    from wtforms
    """
    getter_key = StringField('Key:', validators=[validators.DataRequired("You must specify a key!")])

class SignupForm(Form):
	"""
	This class defines a user sign-up form. Users must create an account
	before they may interact with the application.
	attributes:
		first_name (StringField)
		last_name (StringField)
		email (StringField)
		password (PasswordField)
		submit (SubmitField)
	inherits:
		Form 	from wtforms
	"""
	first_name = StringField('First name:', validators=[validators.DataRequired("Please enter your first name.")])
	last_name = StringField('Last name:', validators=[validators.DataRequired("Please enter your last name.")])
	email = StringField('Email:', validators=[validators.DataRequired("Please enter an email address."),
		validators.Email("Email address must be valid.")])
	password = PasswordField('Password:', validators=[validators.DataRequired("Please enter a password."),
		validators.Length(min=8, message="Password must be a minimum of 8 characters.")])
	submit = SubmitField('Create account')

class LoginForm(Form):
	email = StringField('Email:', validators=[validators.DataRequired("Please enter your email address"),
		validators.Email("Please enter a valid email address.")])
	password = PasswordField('Password:', validators=[validators.DataRequired("Please enter a password.")])
	submit = SubmitField("Sign in")

