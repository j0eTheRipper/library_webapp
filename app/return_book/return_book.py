from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from werkzeug.security import check_password_hash
from app.shared_functions import login_required
from app.database_config.db import get_db
from app.database_config.models import Borrows, Users, Books

bp = Blueprint('return_book', __name__, url_prefix='/return')


@bp.route('/<int:borrow_id>')
@login_required
def get_return_book(borrow_id):
    if session.get('is_admin'):
        return redirect(url_for('borrows.view_unreturned_borrows'))
    else:
        db = get_db()
        title = db.query(Borrows).filter_by(id=borrow_id).first().book
        return render_template('return_book/return_book.html', title=title)


@bp.route('/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    db = get_db()
    correct_passwd = db.query(Users).filter_by(username=session.get('username')).first().password
    password_input = request.form['password']
    password_is_correct = check_password_hash(correct_passwd, password_input)

    if password_is_correct:
        return_borrowed_book(borrow_id, db)
        flash('Returned Successfully', 'success')
        return redirect(url_for('borrows.view_unreturned_borrows'))
    else:
        flash('Incorrect password, please retry.', 'danger')
        return redirect(url_for('return_book.get_return_book', borrow_id=borrow_id))


def return_borrowed_book(borrow_id, db):
    borrow = db.query(Borrows).filter_by(id=borrow_id).first()
    book = db.query(Books).filter_by(title=borrow.book).first()
    edits = borrow.return_book(book)
    db.add_all(edits)
    db.commit()
