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
