from tests.repeated_tests.check_books_rendering import db_test

AVAILABLE_BOOK = '/borrow/3'
UNAVAILABLE_BOOK = '/borrow/1'
borrows_page = '/browse/'
main_page = '/'


@db_test(False)
def test_admin_borrow(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.post(AVAILABLE_BOOK, data={'password': 'admin'})
    assert response.status_code == 403
    assert response.headers['Location'] == borrows_page
    response = client.get(borrows_page)
    assert b'Admins can not borrow from their own library!' in response.data


@db_test(False)
def test_valid_but_unavailable(app, client, authenticate):
    authenticate.login('userx', 'admin')
    response = client.post(UNAVAILABLE_BOOK, data={'password': 'admin'})
    assert response.status_code == 302
    assert response.headers['Location'] == borrows_page
    response = client.get(borrows_page)
    assert b'The book you selected is not available right now!' in response.data


@db_test(False)
def test_wrong_borrow_password(app, client, authenticate):
    authenticate.login('userx', 'admin')
    response = client.post(AVAILABLE_BOOK, data={'password': 'wrong_password'})
    assert response.status_code == 302
    redirect_location = response.headers['Location']
    redirect_response = client.get(redirect_location)
    assert b'Incorrect Password' in redirect_response.data


@db_test(False)
def test_borrowing_an_unreturned_book(app, client, authenticate):
    authenticate.login('user', 'user')
    re_borrow_response = client.post('/borrow/2', data={'password': 'user'})
    assert re_borrow_response.status_code == 302
    assert re_borrow_response.headers['Location'] == borrows_page
    response = client.get(borrows_page)
    assert b'You already have that book!' in response.data


@db_test(False)
def test_borrowing_without_returning(app, client, authenticate):
    authenticate.login('user', 'user')
    get_response = client.post(AVAILABLE_BOOK, data={'password': 'user'})
    assert get_response.status_code == 302
    assert get_response.headers['Location'] == borrows_page
    redirect_response = client.get(borrows_page)
    assert b'Please return your borrows.' in redirect_response.data


@db_test(True)
def test_borrow(app, client, authenticate):
    authenticate.login('userx', 'admin')
    response = client.post(AVAILABLE_BOOK, data={'password': 'admin'})
    assert response.status_code == 302
    assert response.headers['Location'] == main_page
    response = client.get(main_page)
    assert b'Successfully borrowed' in response.data
