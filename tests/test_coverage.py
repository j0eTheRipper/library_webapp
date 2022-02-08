import os
from sqlite3 import connect
from app import create_app
from app.database_config.db import init_db
from tempfile import mkstemp
from os.path import join, dirname
import pytest


with open(join(dirname(__file__), 'data.sql'), 'rb') as script_file:
    sql = script_file.read().decode('utf8')


@pytest.fixture
def app():
    db_d, db_path = mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        db = connect(app.config['DATABASE'])

        cursor = db.cursor()
        cursor.executescript(sql)

        cursor.close()
        db.close()

    yield app

    os.close(db_d)
    os.unlink(db_path)


@pytest.fixture
def cli(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
