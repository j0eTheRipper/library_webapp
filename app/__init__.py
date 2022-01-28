from flask import Flask, render_template, session
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

    @app.route('/')
    def _(): 
        is_logged_in = bool(session.get('user'))
        return render_template('home.html', is_logged_in=is_logged_in)
    

    with app.app_context():
        from .database_config import db
        db.init_app(app)
    

    from .authentication.login import login_bp
    app.register_blueprint(login_bp)

    return app
