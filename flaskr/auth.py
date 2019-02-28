import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
# this creates a Blueprint named auth
# __name__ is passed as the second arg b/c it has to know where it is being defined
bp = Blueprint('auth', __name__, url_prefix='/auth')
# URL prefix is prepended to all other associated URL's


# Once the user visits /auth/register they will have an HTML form
# to fill out. Once submitted it will vallidate input and either
# error, or create the new user

# @bp.route associates the URL /register with the register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # validating the request from form submission
    if request.method == 'POST':
        # request.form is a special dict mapping
        # users put in the info into username and password field
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        # Once validation is successful the password is stored with a hash
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            #  required after querys are modifying the data
            db.commit()
            # After user is stored they are redirected to the login page
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


#  majority is the same from registration
#  minor differences
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        #  checking if hashed password from registration matches the one inputed
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is a dict that stores data across requests
            session.clear()
            # when validation is a success the user's id is stored in a new session
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    # Once id is stored in the session, it is available on subsequent requests
    # once logged in there information should be loaded
    return render_template('auth/login.html')
