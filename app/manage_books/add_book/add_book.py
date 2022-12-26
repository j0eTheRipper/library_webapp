from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.shared_functions import admin_only, login_required
from app.database_config.db import get_db
from app.database_config.models import Subject, Books


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

    db = get_db()
    book_exists = db.query(Books).filter_by(title=book_data['title']).first()

    if book_exists:
        flash('This book already exists!', 'danger')
        return redirect(url_for('manage_books.add_books.get_add_book'))
    else:
        new_book = Books(
            title=book_data['title'].title(),
            subject=book_data['subject'],
            author=book_data['author'].title(),
            count=book_data['count'],
        )
        db.add(new_book)
        db.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('browse.browse'))
