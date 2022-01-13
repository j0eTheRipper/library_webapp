from flask import Flask
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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    with app.app_context():
        from .import db
        db.init_app(app)

    return app
