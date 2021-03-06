AVAILABLE_BOOK = 'http://localhost/borrow/3'
UNAVAILABLE_BOOK = 'http://localhost/borrow/1'


def db_test(state=False):
    def pseudo_decorator(func):
        def wrapper(app, client, authenticate):
            func(app, client, authenticate)

            with app.app_context():
                from app.database_config.db import get_db
                from app.database_config.models import Borrows

                db = get_db()
                if state:
                    borrows = db.query(Borrows).all()
                    assert len(borrows) == 7
                    assert borrows[-1].book == '1984'
                else:
                    borrow = db.query(Borrows).filter_by(id=7).first()
                    assert not borrow
        return wrapper
    return pseudo_decorator


@db_test(False)
def test_invalid_access(app, client, authenticate):
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 401
    assert response.headers['Location'] == 'http://localhost/login/'

    authenticate.login('admin', 'admin')
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 403
    assert b'Admins can not borrow from their own library!' in response.data


@db_test(False)
def test_valid_but_unavailable(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(UNAVAILABLE_BOOK)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/borrow/browse'

    response = client.get('http://localhost/borrow/browse')
    assert b'The book you selected is not available right now!' in response.data


@db_test(False)
def test_valid_and_available(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 200


@db_test(False)
def test_wrong_borrow_password(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.post(AVAILABLE_BOOK, data={'password': 'wrong_password'})
    assert response.status_code == 302
    assert response.headers['Location'] == AVAILABLE_BOOK


@db_test(False)
def test_borrowing_an_unreturned_book(app, client, authenticate):
    authenticate.login('user', 'user')
    re_borrow_response = client.get('http://localhost/borrow/2')
    assert re_borrow_response.status_code == 302
    assert re_borrow_response.headers['Location'] == 'http://localhost/borrow/browse'

    response = client.get('http://localhost/borrow/browse')
    assert b'You already have that book!' in response.data


@db_test(True)
def test_borrow(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.post(AVAILABLE_BOOK, data={'password': 'user'})
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
