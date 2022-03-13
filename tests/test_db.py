from os.path import isfile
from os import remove


def test_init_db_command(runner):
    db = 'testing.sqlite'

    if isfile(db):
        remove(db)

    result = runner.invoke(args=['init-db'])
    assert 'created successfully' in result.output
    assert isfile(db)


def test_get_close_db(app):
    from app.database_config.db import get_db, close_db
    from flask import g

    with app.app_context():
        db = get_db()

        assert g.db == db
        close_db()
        assert 'db' not in g
