URL = 'http://localhost/view_borrows/'


def test_user_view(app, client, authenticate):
    authenticate.login('user', 'user')
    client.post('http://localhost/borrow/2', data={'password': 'user'})

    authenticate.logout()

    authenticate.login('userx', 'abc')
    assert client.get(URL).status_code == 200
    client.post('http://localhost/borrow/3', data={'password': 'abc'})

    response = client.get(URL)
    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Users, Borrows

        db = get_db()

        user_borrows = db.query(Users).filter_by(username='userx').first().borrows
        other_borrows = db.query(Users).filter_by(username='user').first().borrows

        assert_borrows(response, user_borrows)
        assert_borrows(response, other_borrows, False)


def assert_borrows(response, borrows, borrow_in_page=True):
    for borrow in borrows:
        if borrow_in_page:
            assert bytes(borrow.book, encoding='UTF8') in response.data
        else:
            assert not bytes(borrow.book, encoding='UTF8') in response.data
