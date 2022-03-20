from datetime import date, timedelta
from flask import Blueprint, render_template, request, session, url_for, flash, redirect, abort
from werkzeug.security import check_password_hash
from ..database_config.db import get_db
from ..database_config.models import Books, Users, Borrows, Subject
from ..shared_functions import login_required

bp = Blueprint('borrow', __name__, url_prefix='/borrow')


@bp.route('/browse')
@login_required
def browse():
    if session['is_admin']:
        abort(403, 'Admins can not borrow from their own library!')

    subject_filter = request.args.get('subject')
    db = get_db()

    if subject_filter:
        book_list = db.query(Subject).filter_by(subject=subject_filter).first().books
    else:
        book_list = db.query(Books).all()

    subjects = db.query(Subject).all()
    return render_template('borrow/browse.html', books=book_list, subjects=subjects)


@bp.route('/<int:book>', methods=['GET', 'POST'])
@login_required
def borrow_get(book):
    if session['is_admin']:
        abort(403, 'Admins can not borrow from their own library!')

    db = get_db()
    book = db.query(Books).filter_by(id=book).first()

    if request.method == 'GET':
        if book.count <= 0:
            flash('The book you selected is not available right now!', 'danger')
            return redirect(url_for('borrow.browse'))
        else:
            return render_template('borrow/borrow.html', title=book.title)
    else:
        user = db.query(Users).filter_by(username=session['username']).first()
        return borrow_post(book, user, db)


def borrow_post(book, user, db):
    passwd_correct = check_password_hash(user.password, request.form['password'])
    if passwd_correct:
        return_date = borrow_book(book, db, user)
        flash(f'Successfully borrowed {book.title}, please return by {return_date}', 'success')
        return redirect(url_for('home.home'))
    else:
        flash(f'Incorrect Password', 'danger')
        return redirect(url_for('borrow.borrow_get', book=book.id))


def borrow_book(book, db, user):
    borrow_date = date.today()
    return_date = borrow_date + timedelta(days=7)
    borrow = Borrows(borrower=user.username, book=book.title, due_date=return_date)
    book.count -= 1
    db.add_all([borrow, book])
    db.commit()
    return return_date
