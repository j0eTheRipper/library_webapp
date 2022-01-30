from flask import Blueprint, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from ...database_config.db import get_db


bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('/')
def login_get():
    if not session.get('username'):
        return render_template('authentication/login.html')
    else:
        return redirect(url_for('/'))

@bp.route('/', methods=['POST'])
def login_post():
    pass
