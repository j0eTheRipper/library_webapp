from flask import Blueprint, render_template, session, flash, Markup
from ..database_config.models import Borrows
from ..database_config.db import get_db, close_db
from datetime import date


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))

    if is_logged_in:
        if session.get('is_admin'):
            unreturned_books = un_returned_books(True)
            return render_template('index/admin.html', unreturned_books=len(unreturned_books))
        else:
            unreturned_books = un_returned_books(False)
            return render_template('index/user.html', unreturned_books=len(unreturned_books))
    else:
        return render_template('index/guest.html')


def un_returned_books(is_admin):
    db = get_db()
    today = date.today()

    if is_admin:
        unreturned = db.query(Borrows).filter_by(date_returned=None)
    else:
        unreturned = db.query(Borrows).filter_by(borrower=session['username']).filter_by(date_returned=None)

    expired = unreturned.filter(today >= Borrows.due_date).all()
    unreturned = unreturned.all()
    if expired:
        message = Markup(
            f'You have {len(expired)} books that need to be returned! Please <a href="/view_borrowed">return</a>'
        )
        flash(message, 'warning')

    close_db()
    return unreturned
