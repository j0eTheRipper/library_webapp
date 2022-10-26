from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from app.database_config.db import get_db, close_db
from app.database_config.models import Users
from app.shared_functions import login_required, admin_only


bp = Blueprint('add_user', __name__, url_prefix='/add_user')


@bp.route('/')
@login_required
@admin_only
def add_user_get():
    return render_template('manage_users/add_user.html')


@bp.route('/', methods=['POST'])
def add_user_post():
    username = request.form.get('username')
    password = request.form.get('password')
    password_confirmation = request.form.get('password_confirmation')
    fullname = request.form.get('fullname')
    class_id = request.form.get('class_id')

    input_errors = check_for_errors(password, password_confirmation, username, fullname)

    if input_errors:
        return redirect(url_for('manage_users.add_user.add_user_get'))

    return register_user(password, username, fullname, class_id)


def check_for_errors(password, password_confirmation, username, fullname):
    if not (username and password and password_confirmation and fullname):
        flash('Please fill out all the fields.', 'danger')
        return True

    db = get_db()
    user_exists = db.query(Users).filter_by(username=username).first()
    close_db()
    error = False

    if user_exists:
        flash('This username is already registered', 'danger')
        error = True
    elif password != password_confirmation:
        flash('Passwords do not match!', 'danger')
        error = True
    elif ' ' in username:
        flash('Spaces are not allowed in usernames.', 'danger')
        error = True

    return error


def register_user(password, username, fullname, class_id):
    user = Users.create_user(username, password, fullname, class_id)
    add_to_db(user)
    flash(f'{fullname} has been added successfully!', 'success')

    return redirect(url_for('home.home'))


def add_to_db(user):
    db = get_db()
    db.add(user)
    db.commit()
