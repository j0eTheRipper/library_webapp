from tests.repeated_tests.repeated_request_tests import *
from tests.test_manage_books.shared_tests import assert_book_in_db

URL = '/manage_books/add_book/'


def test_invalid_access(client, authenticate):
    unauthorized_access(client, URL)


def test_unauthorized_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)
    assert response.status_code == 403


def test_valid_get(client, authenticate):
    request_user_page(client, authenticate, URL, 'admin', 'admin')


def test_add_new_book(client, authenticate, app):
    authenticate.login('admin', 'admin')
    new_book = {
        'title': 'Tom Sawyer',
        'author': 'Mark Twain',
        'subject': 'Story',
        'count': 5,
    }
    response = client.post(URL, data=new_book)
    assert response.headers['Location'] == '/browse/'
    response = client.get('/browse/')
    assert b'Book added successfully!' in response.data
    with app.app_context():
        assert_book_in_db(new_book)


def test_add_existing_book(client, authenticate, app):
    authenticate.login('admin', 'admin')
    new_book = {
        'title': '1984',
        'author': 'George Orwell',
        'subject': 'Story',
        'count': '5',
    }
    response = client.post(URL, data=new_book)
    assert response.headers['Location'] == URL
    response = client.get('/browse/')
    assert b'This book already exists!' in response.data
    with app.app_context():
        books = assert_book_in_db(new_book)
        assert books[0].count != 5


def test_add_book_guest(app, authenticate, client):
    __test_invalid_add_request(app, client)


def __test_invalid_add_request(app, client):
    new_book = {
        'title': 'laks',
        'author': 'some guy',
        'subject': 'Story',
        'count': '5',
    }
    response = client.post(URL, data=new_book)
    assert response.headers['Location'] == '/login/'
    with app.app_context():
        assert_book_in_db(new_book, 0)
