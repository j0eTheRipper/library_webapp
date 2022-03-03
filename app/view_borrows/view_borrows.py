from flask import Blueprint, render_template, redirect, session, url_for
from ..database_config.db import get_db, close_db
from ..database_config.models import Borrows, Users


bp = Blueprint('view_borrows', __name__, url_prefix='/view_borrows')


@bp.route('/')
def view_borrows():
    pass
