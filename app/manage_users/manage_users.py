from flask import Blueprint, render_template
from app.shared_functions import login_required, admin_only


bp = Blueprint('manage_users', __name__, url_prefix='/manage_users')


@bp.route('/')
@login_required
@admin_only
def main():
    return render_template('manage_users/index.html')

