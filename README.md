# HaloChallenge
Coding Challenge from Halo

This app was developed with python 2.7 on MacBook running macOS High
  Sierra.

To run, cd to halo_challenge_app/ and use the command:
  
  $ python dict_app.py

The application runs on localhost:8000

#####################################################################
  Create a New User:
#####################################################################

1. From the Login form, click "Sign Up" at the top of the page.
2. Fill out the form and click "Sign Up" to be logged in.

#####################################################################
  Using the app:
#####################################################################
  
  Users can add key-value pairs to the database with the "Setter" form.
1. Enter a key and a value under "Setter" and click "SET"

  Users can query values using the "Getter" form.
2. Enter a key that exists in the database and click "GET"

  Key-value pairs are separated by user, so one user cannot view or
    modify another user's key-value pairs.

#####################################################################
  Testing the app:
#####################################################################

  Some very minimal test cases live in test_dict_app.py. To run them,
  simply cd to halo_challenge_app and run:

    $ python test_dict_app.py
