from tests.repeated_tests.repeated_request_tests import *
from tests.repeated_tests.check_books_rendering import db_test

AVAILABLE_BOOK = '/borrow/3'
UNAVAILABLE_BOOK = '/borrow/1'
borrows_page = '/browse/'
main_page = '/'


@db_test(False)
def test_invalid_access(app, client, authenticate):
    unauthorized_access(client, AVAILABLE_BOOK)

    authenticate.login('admin', 'admin')
    response = client.get(AVAILABLE_BOOK)
    assert response.status_code == 403
    response = client.get(borrows_page)
    assert b'Admins can not borrow from their own library!' in response.data


@db_test(False)
def test_valid_but_unavailable(app, client, authenticate):
    authenticate.login('userx', 'admin')
    response = client.get(UNAVAILABLE_BOOK)
    assert response.status_code == 302
    assert response.headers['Location'] == borrows_page

    response = client.get(borrows_page)
    assert b'The book you selected is not available right now!' in response.data


@db_test(False)
def test_valid_and_available(app, client, authenticate):
    request_user_page(client, authenticate, AVAILABLE_BOOK, 'userx', 'admin')


@db_test(False)
def test_borrowing_an_unreturned_book(app, client, authenticate):
    authenticate.login('user', 'user')
    re_borrow_response = client.get('/borrow/2')
    assert re_borrow_response.status_code == 302
    assert re_borrow_response.headers['Location'] == borrows_page

    response = client.get(borrows_page)
    assert b'You already have that book!' in response.data


@db_test(False)
def test_borrowing_without_returning(app, client, authenticate):
    authenticate.login('user', 'user')
    get_response = client.get(AVAILABLE_BOOK)
    assert get_response.status_code == 302
    assert get_response.headers['Location'] == borrows_page
    redirect_response = client.get(borrows_page)
    assert b'Please return your borrows.' in redirect_response.data
