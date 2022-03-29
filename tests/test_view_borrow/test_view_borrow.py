URL = 'http://localhost/borrows/history'


def test_user_view(app, client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()

        user_borrows = db.query(Borrows).filter_by(borrower='user')
        returned_borrows = user_borrows.filter(Borrows.date_returned).all()
        unreturned_borrows = user_borrows.filter_by(date_returned=None).all()
        other_borrows = db.query(Borrows).filter(Borrows.borrower != 'user').all()

        assert_borrows(response, returned_borrows)
        assert_borrows(response, unreturned_borrows, False)
        assert_borrows(response, other_borrows, False)


def test_admin_view(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        all_borrows = db.query(Borrows)
        returned_borrows = all_borrows.filter(Borrows.date_returned).all()
        unreturned_borrows = all_borrows.filter_by(date_returned=None).all()

        assert_borrows(response, returned_borrows)
        assert_borrows(response, unreturned_borrows, False)


# def test_filters(app, client, authenticate):
#     authenticate.login('user', 'user')
#     returned_response = client.get(f'{URL}?filter=overdue')
#     unreturned_response = client.get(f'{URL}?filter=on_time')
#
#     with app.app_context():
#         from app.database_config.db import get_db
#         from app.database_config.models import Borrows
#
#         db = get_db()
#         user_borrows_query = db.query(Borrows).filter_by(borrower='user')
#         overdue = user_borrows_query.filter(Borrows.date_returned).all()
#         unreturned = user_borrows_query.filter_by(date_returned=None).all()
#
#         assert_borrows(returned_response, returned)
#         assert_borrows(unreturned_response, unreturned)
#         assert_borrows(returned_response, unreturned, False)
#         assert_borrows(unreturned_response, returned, False)


def assert_borrows(response, borrows, borrow_in_page=True):
    for borrow in borrows:
        if borrow_in_page:
            assert bytes(borrow.book, encoding='UTF8') in response.data
        else:
            assert not bytes(borrow.book, encoding='UTF8') in response.data
