from functools import wraps

from flask import session, url_for
from werkzeug.utils import redirect


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login.login_get'), 401)
    return wrapper


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('is_admin'):
            return func(*args, **kwargs)
        else:
            return '<h1>403, you are not allowed in here!</h1>', 403
    return wrapper
