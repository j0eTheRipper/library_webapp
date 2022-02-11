from flask import Blueprint, render_template, session


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))

    if is_logged_in:
        if session.get('is_admin'):
            return render_template('index/admin.html')
        else:
            return render_template('index/user.html')
    else:
        return render_template('index/guest.html')

