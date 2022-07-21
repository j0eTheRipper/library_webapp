from flask import Blueprint, render_template, request, session
from datetime import date
from ..database_config.db import get_db
from ..database_config.models import Borrows
from ..shared_functions import login_required


bp = Blueprint('borrows', __name__, url_prefix='/borrows')


@bp.route('/history_returned')
@login_required
def view_returned_borrows():
    db = get_db()
    borrows = db.query(Borrows).filter(Borrows.date_returned)
    filters = request.args.get('filter')

    borrows = process_borrows(borrows, filters)

    return render_template('view_borrows/view_borrows.html', borrows=borrows, today=date.today())


@bp.route('/history_unreturned')
@login_required
def view_unreturned_borrows():
    db = get_db()
    borrows = db.query(Borrows).filter_by(date_returned=None)
    filters = request.args.get('filter')
    # print(filters)

    borrows = process_borrows(borrows, filters)

    return render_template('view_borrows/view_unreturned_borrows.html', borrows=borrows, today=date.today())


def process_borrows(borrows, filters=None):
    if filters:
        if filters == 'overdue':
            borrows = borrows.filter(date.today() > Borrows.due_date)
        elif filters == 'on_time':
            borrows = borrows.filter(Borrows.date_returned <= Borrows.due_date)

    if session.get('is_admin'):
        borrows = borrows.all()
    else:
        borrows = borrows.filter_by(borrower=session.get('username')).all()

    return borrows
