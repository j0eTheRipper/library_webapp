from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from ...database_config.db import get_db
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

    return validate_user_input(password, password_confirmation, username)


def validate_user_input(password, password_confirmation, username):
    db = get_db()
    user_exists = db.query(Users).filter_by(username=username).first()
    db.close()

    if user_exists:
        flash('This username is already taken, please try another one.', 'danger')
        return redirect(url_for('signup.signup_get'))
    elif password != password_confirmation:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('signup.signup_get'))

    return register_user(password, username)


def register_user(password, username):
    passwd = generate_password_hash(password)
    user = Users(username=username, password=passwd)
    session['username'] = username

    add_to_db(user)

    flash(f'Welcome, {username}, here you are!', 'success')
    return redirect(url_for('home.home'))


def add_to_db(user):
    db = get_db()
    db.add(user)
    db.commit()
    db.close()

