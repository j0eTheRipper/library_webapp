from os.path import isfile
from os import remove


def test_get_close_db(app):
    from app.database_config.db import get_db, close_db
    from flask import g

    with app.app_context():
        db = get_db()

        assert g.db == db
        close_db()
        assert 'db' not in g
