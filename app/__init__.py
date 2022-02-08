from flask import Flask
from flask_bootstrap import Bootstrap
from os import makedirs
from os.path import isdir, join


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    if not isdir(app.instance_path):
        makedirs(app.instance_path)

    Bootstrap(app)

    with app.app_context():
        from .database_config import db
        db.init_app(app)

    from .authentication.login import login_bp
    from .authentication.signup import signup_bp
    from .home import bp as home_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)

    return app