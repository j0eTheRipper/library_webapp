from tests.repeated_tests.repeated_request_tests import *
from datetime import date

URL = '/return/1'
URL_returned = '/return/2'


def test_guest_access(client, authenticate):
    unauthorized_access(client, URL)


def test_admin_access(client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 302
    assert response.headers['Location'] == '/borrows/history_unreturned'


def test_user_access(client, authenticate):
    request_user_page(client, authenticate, URL, 'user', 'user')


def test_invalid_credentials(client, authenticate, app):
    authenticate.login('user', 'user')
    response = client.post(URL, data={'password': 'wrong_passwd'})
    assert response.status_code == 302
    assert response.headers['Location'] == URL
    assert b'Incorrect password, please retry.' in client.get(URL).data

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()

        user_borrows = db.query(Borrows).filter_by(borrower='user')
        first_borrow = user_borrows.filter_by(id=1).first()
        assert not first_borrow.date_returned


def test_returning_a_returned_borrow(client, authenticate, app):
    authenticate.login('user', 'user')
    response = client.post(URL_returned, data={'password': 'user'})
    assert response.headers['Location'] == '/'
    assert b'Sneaky, I like that! ;)'

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows, Books

        db = get_db()

        user_borrows = db.query(Borrows).filter_by(borrower='user')
        first_borrow = user_borrows.filter_by(id=1).first()
        book = db.query(Books).filter_by(title=first_borrow.book).first()
        assert first_borrow.date_returned != date.today()
        assert book.count == 2


def test_valid_credentials(client, authenticate, app):
    authenticate.login('user', 'user')
    response = client.post(URL, data={'password': 'user'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/borrows/history_unreturned'
    assert b'Returned Successfully' in client.get(response.headers["Location"]).data

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows, Books

        db = get_db()

        user_borrows = db.query(Borrows).filter_by(borrower='user')
        first_borrow = user_borrows.filter_by(id=1).first()
        book = db.query(Books).filter_by(title=first_borrow.book).first()
        assert first_borrow.date_returned == date.today()
        assert book.count == 3
