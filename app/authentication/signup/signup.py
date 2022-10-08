from flask import Blueprint, render_template, session, redirect, url_for, request, flash, Markup
from app.database_config.db import get_db, close_db
from app.database_config.models import Users
from app.shared_functions import login_required, admin_only


bp = Blueprint('signup', __name__, url_prefix='/signup')


@bp.route('/')
@login_required
@admin_only
def signup_get():
    return render_template('authentication/signup.html')


@bp.route('/', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')

    input_errors = check_for_errors(password, password_confirmation, username)

    if input_errors:
        return redirect(url_for('signup.signup_get'))

    return register_user(password, username)


def check_for_errors(password, password_confirmation, username):
    if not (username and password and password_confirmation):
        flash('Please provide a username and a password')
        return True

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
    user = Users.create_user(username, password)
    add_to_db(user)
    register_user_to_session(user)

    return redirect(url_for('home.home'))


def register_user_to_session(user: Users):
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    flash(f'Welcome, {user.username}, you made it!', 'success')


def add_to_db(user):
    db = get_db()
    db.add(user)
    db.commit()
