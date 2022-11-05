from tests.repeated_tests.repeated_request_tests import *

URL = '/manage_books/add_book'


def test_invalid_access(client, authenticate):
    unauthorized_access(client, URL)


def test_unauthorized_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)
    assert response.status_code == 403


def test_valid_get(client, authenticate):
    request_user_page(client, authenticate, URL, 'admin', 'admin')

