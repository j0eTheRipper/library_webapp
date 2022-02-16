from flask import Blueprint, render_template
from ..database_config.db import get_db, close_db
from ..database_config.models import Books

bp = Blueprint('borrow', __name__, url_prefix='/borrow')


@bp.route('/browse')
def browse():
    db = get_db()
    book_list = db.query(Books).all()
    close_db()
    return render_template('borrow/browse.html', books=book_list)
