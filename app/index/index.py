from flask import Blueprint, render_template, session, flash
from ..database_config.models import Borrows
from ..database_config.db import get_db, close_db
from datetime import date


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))

    if is_logged_in:
        un_returned_books()

        if session.get('is_admin'):
            return render_template('index/admin.html')
        else:
            return render_template('index/user.html')
    else:
        return render_template('index/guest.html')


def un_returned_books():
    db = get_db()
    today = date.today()
    all_borrows = db.query(Borrows).filter_by(borrower=session['username']).filter_by(is_returned=False)
    expired = all_borrows.filter(today >= Borrows.date_returned).all()
    un_returned = all_borrows.filter(today <= Borrows.date_returned).all()
    if expired:
        flash(f'You have {len(expired)} books that need to be returned! Please return', 'warning')
    if un_returned:
        flash(f'You have {len(un_returned)} unreturned books. Remember to return them on time!', 'success')
