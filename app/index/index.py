from flask import Blueprint, render_template, session, flash, Markup, g
from ..database_config.models import Borrows, Users
from ..database_config.db import get_db, close_db
from datetime import date


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def home():
    is_logged_in = bool(session.get('username'))

    if is_logged_in:
        db = get_db()
        fullname = db.query(Users).filter_by(username=session['username']).first().fullname
        if session.get('is_admin'):
            unreturned_books = get_all_unreturned_books()
            page_to_render = 'index/admin.html'
        else:
            unreturned_books = get_user_unreturned_books(session['username'])
            notify_for_overdue_books(unreturned_books)
            unreturned_books = unreturned_books.all()
            page_to_render = 'index/user.html'

        return render_template(page_to_render, unreturned_books=len(unreturned_books), fullname=fullname)
    else:
        return render_template('index/guest.html')


def get_all_unreturned_books():
    db = g.db
    unreturned_books_query = db.query(Borrows).filter_by(date_returned=None)
    return unreturned_books_query.all()


def get_user_unreturned_books(user):
    db = g.db
    unreturned_books_query = db.query(Borrows).filter_by(date_returned=None)
    user_specific_unreturned_books_query = unreturned_books_query.filter_by(borrower=user)
    return user_specific_unreturned_books_query


def notify_for_overdue_books(unreturned_books_query):
    today = date.today()
    over_due_books = unreturned_books_query.filter(today >= Borrows.due_date).all()
    if over_due_books:
        message = Markup(
            f'You have {len(over_due_books)} books that need to be returned! Please ' +
            f'<a href="/borrows/history_unreturned">return</a>'
        )
        flash(message, 'warning')
