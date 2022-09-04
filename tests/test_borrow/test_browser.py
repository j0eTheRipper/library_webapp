from tests.repeated_tests.repeated_request_tests import *
from tests.test_borrow.testing_functions import assert_books

URL = 'http://localhost/borrow/browse'


def test_invalid_access(client, authenticate):
    unauthorized_access(client, URL)

    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 403
    assert b'Admins can not borrow from their own library!' in response.data


def test_valid_access(app, client, authenticate):
    response = request_user_page(client, authenticate, URL, 'user', 'user')

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Books

        db = get_db()
        all_books = db.query(Books).all()

        assert_books(response, all_books)


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
