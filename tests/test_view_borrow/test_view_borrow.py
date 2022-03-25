URL = 'http://localhost/view_borrows/'


def test_user_view(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Users, Borrows

        db = get_db()

        user_borrows = db.query(Users).filter_by(username='user').first().borrows
        other_borrows = db.query(Borrows).filter(Borrows.borrower != 'user').all()

        assert_borrows(response, user_borrows)
        assert_borrows(response, other_borrows, False)


def test_admin_view(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        all_borrows = db.query(Borrows).all()

        for borrow in all_borrows:
            assert bytes(borrow.book, encoding='UTF8') in response.data
            assert bytes(borrow.borrower, encoding='UTF8') in response.data


def test_filters(app, client, authenticate):
    authenticate.login('user', 'user')
    returned_response = client.get(f'{URL}?filter=returned')
    unreturned_response = client.get(f'{URL}?filter=unreturned')
    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        user_borrows_query = db.query(Borrows).filter_by(borrower='user')
        returned = user_borrows_query.filter(Borrows.date_returned).all()
        unreturned = user_borrows_query.filter_by(date_returned=None).all()

        assert_borrows(returned_response, returned)
        assert_borrows(unreturned_response, unreturned)
        assert_borrows(returned_response, unreturned, False)
        assert_borrows(unreturned_response, returned, False)


def assert_borrows(response, borrows, borrow_in_page=True):
    for borrow in borrows:
        if borrow_in_page:
            assert bytes(borrow.book, encoding='UTF8') in response.data
        else:
            assert not bytes(borrow.book, encoding='UTF8') in response.data
