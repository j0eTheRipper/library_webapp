from flask import Blueprint, render_template, redirect, session, url_for
from ..database_config.db import get_db, close_db
from ..database_config.models import Borrows, Users


bp = Blueprint('view_borrows', __name__, url_prefix='/view_borrows')


@bp.route('/')
def view_borrows():
    db = get_db()

    if session.get('is_admin'):
        borrows = db.query(Borrows).all()
    else:
        borrows = db.query(Users).filter_by(username=session['username']).first().borrows

    return render_template('view_borrows/view_borrows.html', borrows=borrows)
