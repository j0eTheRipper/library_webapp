from flask import Flask
from os import makedirs
from os.path import isdir, join


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='postgresql://postgres@localhost:5432/library',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    if not isdir(app.instance_path):
        makedirs(app.instance_path)

    with app.app_context():
        from .database_config import db
        db.init_app(app)

    from app.authentication.login import login_bp
    app.register_blueprint(login_bp)

    from app.index import index_bp
    app.register_blueprint(index_bp)

    from app.borrow import borrow_bp
    app.register_blueprint(borrow_bp)

    from app.borrow_history import borrows_bp
    app.register_blueprint(borrows_bp)

    from app.return_book import return_book_bp
    app.register_blueprint(return_book_bp)

    from app.browse import browse_bp
    app.register_blueprint(browse_bp)

    from app.manage_users import manage_users_bp
    from app.manage_users.add_user import add_user_bp
    manage_users_bp.register_blueprint(add_user_bp)
    app.register_blueprint(manage_users_bp)

    from app.manage_books import manage_books_index_bp
    from app.manage_books.add_book import add_book_bp
    manage_books_index_bp.register_blueprint(add_book_bp)
    app.register_blueprint(manage_books_index_bp)

    return app
