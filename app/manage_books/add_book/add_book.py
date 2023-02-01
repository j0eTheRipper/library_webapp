from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.shared_functions import admin_only, login_required
from app.database_config.db import get_db
from app.database_config.models import Subject, Books
from app.database_config.exceptions import BookExists


bp = Blueprint('add_books', __name__, url_prefix='/add_book')


@bp.route('/')
@login_required
@admin_only
def get_add_book():
    db = get_db()
    subjects = db.query(Subject).all()
    return render_template('manage_books/add_book/add_book.html', subjects=subjects)


@bp.route('/', methods=['POST'])
@login_required
@admin_only
def post_add_book():
    book_data = request.form.to_dict()

    if None in book_data.values():
        flash('Please fill all the fields.', 'danger')
        return redirect(url_for('manage_books.add_books.get_add_book'))

    return add_book(book_data)


def add_book(book_data):
    db = get_db()
    try:
        new_book = Books.add_book(book_data)
    except BookExists:
        flash('This book already exists!', 'danger')
        return redirect(url_for('manage_books.add_books.get_add_book'))
    else:
        db.add(new_book)
        db.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('browse.browse'))
