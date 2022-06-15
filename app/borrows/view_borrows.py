from flask import Blueprint, render_template, request, session, url_for
from datetime import date
from ..database_config.db import get_db
from ..database_config.models import Borrows


bp = Blueprint('borrows', __name__, url_prefix='/borrows')


@bp.route('/history')
def view_borrows():
    db = get_db()
    borrow_state_filter = request.args.get('filter')
    borrows = db.query(Borrows)

    if borrow_state_filter == 'returned':
        borrows = borrows.filter(Borrows.date_returned)
        print(len(borrows.all()))
    elif borrow_state_filter == 'unreturned':
        borrows = borrows.filter_by(date_returned=None)

    if session['is_admin']:
        borrows = borrows.all()
    else:
        borrows = borrows.filter_by(borrower=session['username']).all()

    return render_template('borrows/borrow_history.html', borrows=borrows, today=date.today())
