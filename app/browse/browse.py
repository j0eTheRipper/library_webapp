from flask import Blueprint, render_template, request
from app.shared_functions import login_required
from app.database_config.db import get_db
from app.database_config.models import Subject, Books

bp = Blueprint('browse', __name__, url_prefix='/browse')


@bp.route('/')
@login_required
def browse():
    subject_filter = request.args.get('subject')
    db = get_db()
    book_list = get_books(db, subject_filter)
    subjects = db.query(Subject).all()
    return render_template('browse/browse.html', books=book_list, subjects=subjects)


def get_books(db, subject_filter):
    if subject_filter:
        book_list = db.query(Subject).filter_by(subject=subject_filter).first().books
    else:
        book_list = db.query(Books).all()
    return book_list
