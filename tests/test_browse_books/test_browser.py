from tests.repeated_tests.repeated_request_tests import *
from tests.repeated_tests.check_books_rendering import assert_books

URL = 'http://localhost/browse/'


def test_invalid_access(client, authenticate):
    unauthorized_access(client, URL)


def test_normal_user_access(app, client, authenticate):
    response = request_user_page(client, authenticate, URL, 'user', 'user')

    assert b'Add books' not in response.data
    assert b'Browse Books' in response.data

    check_for_books(app, response)


def test_admin_access(app, client, authenticate):
    response = request_user_page(client, authenticate, URL, 'admin', 'admin')

    assert b'Add book' in response.data

    check_for_books(app, response)


def test_subject_filter(app, client, authenticate):
    url = f'{URL}?subject=Story'
    response = request_user_page(client, authenticate, url, 'user', 'user')

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Subject, Books

        db = get_db()
        stories = db.query(Subject).filter_by(subject='Story').first().books
        all_books = db.query(Books).filter(Books.subject != 'Story').all()

        assert_books(response, stories)
        assert_books(response, all_books, False)


def check_for_books(app, response):
    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Books

        db = get_db()
        all_books = db.query(Books).all()

        assert_books(response, all_books)
