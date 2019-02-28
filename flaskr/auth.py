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
