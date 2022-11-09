from flask import Blueprint, redirect, url_for
from app.shared_functions import admin_only, login_required


bp = Blueprint('manage_books', __name__, url_prefix='/manage_books')


@bp.route('/')
@login_required
@admin_only
def index():
    return redirect(url_for('browse.browse'))
