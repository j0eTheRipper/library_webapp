from flask import Blueprint, render_template, session


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))
    status_code = 205 if is_logged_in else 200
    return render_template('index/index.html', is_logged_in=is_logged_in), status_code

