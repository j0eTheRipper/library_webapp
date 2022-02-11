from flask import Blueprint, render_template, session, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash
from ...database_config.db import get_db, close_db
from ...database_config.models import Users


bp = Blueprint('signup', __name__, url_prefix='/signup')


@bp.route('/')
def signup_get():
    return render_template('authentication/signup.html')


@bp.route('/', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')

    if check_for_errors(password, password_confirmation, username):
        return redirect(url_for('signup.signup_get'), 300)
    else:
        return register_user(password, username)


def check_for_errors(password, password_confirmation, username):
    db = get_db()
    user_exists = db.query(Users).filter_by(username=username).first()
    close_db()
    error = False

    if user_exists:
        message = Markup(
            'This username is already registered. <a href="/login">Login</a> if you already have an account or try '
            'another username.')
        flash(message, 'danger')
        error = True
    elif password != password_confirmation:
        flash('Passwords do not match!', 'danger')
        error = True
    elif ' ' in username:
        flash('Spaces are not allowed in usernames.', 'danger')
        error = True

    return error


def register_user(password, username):
    passwd = generate_password_hash(password)
    user = Users(username=username, password=passwd)
    session['username'] = username
    session['is_admin'] = False

    add_to_db(user)

    return redirect(url_for('home.home'))


def add_to_db(user):
    db = get_db()
    db.add(user)
    db.commit()
    close_db()

