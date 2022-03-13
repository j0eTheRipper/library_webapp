# from app.database_config.db import get_db, close_db
from os.path import isfile
from os import remove


def test_init_db_command(runner):
    db = 'testing.sqlite'

    if isfile(db):
        remove(db)

    result = runner.invoke(args=['init-db'])
    assert 'created successfully' in result.output
    assert isfile(db)
