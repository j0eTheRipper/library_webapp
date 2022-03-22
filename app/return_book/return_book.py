from flask import Blueprint, render_template, session
from ..database_config.db import get_db
from ..database_config.models import Borrows, Users


bp = Blueprint('return', __name__, url_prefix='/return')


@bp.route('/view_borrows')
def view_borrows():
    db = get_db()

    if session.get('is_admin'):
        borrows = db.query(Borrows).all()
    else:
        borrows = db.query(Users).filter_by(username=session['username']).first().borrows

    return render_template('return_book/view_borrows.html', borrows=borrows)
