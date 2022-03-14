from datetime import date

AVAILABLE_BOOK = 'http://localhost/borrow/2'
UNAVAILABLE_BOOK = 'http://localhost/borrow/1'


def db_test(func):
    def wrapper(app, client, authenticate):
        func(app, client, authenticate)

        with app.app_context():
            from app.database_config.db import get_db
            from app.database_config.models import Borrows

            db = get_db()
            borrow = db.query(Borrows).first()
            assert not borrow
    return wrapper


@db_test
def test_invalid_access(app, client, authenticate):
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/login/'


@db_test
def test_valid_but_unavailable(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(UNAVAILABLE_BOOK)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/borrow/browse'

    response = client.get('http://localhost/borrow/browse')
    assert b'The book you selected is not available right now!' in response.data


@db_test
def test_valid_and_available(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 200


@db_test
def test_wrong_borrow_password(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.post(AVAILABLE_BOOK, data={'password': 'wrong_password'})
    assert response.status_code == 302
    assert response.headers['Location'] == AVAILABLE_BOOK


def test_borrow(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.post(AVAILABLE_BOOK, data={'password': 'admin'})
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        borrow = db.query(Borrows).all()
        assert len(borrow) == 1
        assert borrow[0].date_borrowed == date.today()

