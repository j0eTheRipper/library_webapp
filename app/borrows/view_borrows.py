from flask import Blueprint, render_template, request, session, url_for
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
    if filters == 'overdue':
        borrows = borrows.filter(Borrows.date_returned > Borrows.due_date)
    elif filters == 'on_time':
        borrows = borrows.filter(Borrows.date_returned <= Borrows.due_date)

    if session.get('is_admin'):
        borrows = borrows.all()
    else:
        borrows = borrows.filter_by(borrower=session.get('username')).all()

    return render_template('view_borrows/view_borrows.html', borrows=borrows, today=date.today())
