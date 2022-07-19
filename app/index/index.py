from flask import Blueprint, render_template, session, flash, Markup
from ..database_config.models import Borrows
from ..database_config.db import get_db, close_db
from datetime import date


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))
    unreturned_books = 0

    if is_logged_in:
        if session.get('is_admin'):
            unreturned_books = get_unreturned_books(True)
            page_to_render = 'index/user.html'
        else:
            unreturned_books = get_unreturned_books(False)
            page_to_render = 'index/admin.html'
    else:
        page_to_render = 'index/guest.html'

    return render_template(page_to_render, unreturned_books=len(unreturned_books))


def get_unreturned_books(is_admin):
    db = get_db()
    today = date.today()
    unreturned = db.query(Borrows).filter_by(date_returned=None)

    if not is_admin:
        unreturned = unreturned.filter_by(borrower=session['username'])

    expired = unreturned.filter(today >= Borrows.due_date).all()
    unreturned = unreturned.all()
    if expired:
        message = Markup(
            f'You have {len(expired)} books that need to be returned! Please <a '
            'href="/borrows/history_unreturned">return</a> '
        )
        flash(message, 'warning')

    close_db()
    return unreturned
