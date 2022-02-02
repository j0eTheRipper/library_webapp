from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from ...database_config.db import get_db
from ...database_config.models import Users


bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/')
def login_get():
    if not session.get('username'):
        return render_template('authentication/login.html')
    else:
        return redirect(url_for('home.home'))


@bp.route('/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    db = get_db()
    user = db.query(Users).filter_by(username=username).first()

    if user:
        password_correct = check_password_hash(user.password, password)

        if password_correct:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Incorrect Password', 'danger')
            return redirect(url_for('login.login_get'))
    else:
        flash('Incorrect Username!', 'danger')
        return redirect(url_for('login.login_get'))
