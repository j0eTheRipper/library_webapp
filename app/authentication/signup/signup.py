from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from ...database_config.db import get_db
from ...database_config.models import Users


bp = Blueprint('signup', __name__, url_prefix='/signup')


@bp.route('/')
def signup_get():
    return render_template('authentication/signup.html')
