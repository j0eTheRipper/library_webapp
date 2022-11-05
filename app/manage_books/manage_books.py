from flask import Blueprint, redirect, url_for


bp = Blueprint('manage_books', __name__, url_prefix='/manage_books')


@bp.route('/')
def index(): return redirect(url_for('browse.browse'))
