from tests.test_view_borrow.assert_borrows import assert_borrows

URL = 'http://localhost/borrows/history_returned'


def test_unauthorized_accesses(client):
    pre_login_response = client.get(URL)
    assert pre_login_response.status_code == 401
    assert pre_login_response.headers['Location'] == 'http://localhost/login/'


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


def test_filters(app, client, authenticate):
    authenticate.login('user', 'user')
    overdue_filter_response = client.get(f'{URL}?filter=overdue')
    on_time_filter_response = client.get(f'{URL}?filter=on_time')

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        user_borrows_query = db.query(Borrows).filter_by(borrower='user').filter(Borrows.date_returned)
        overdue = user_borrows_query.filter(Borrows.date_returned > Borrows.due_date).all()
        on_time = user_borrows_query.filter(Borrows.date_returned <= Borrows.due_date).all()

        assert_borrows(overdue_filter_response, overdue)
        assert_borrows(overdue_filter_response, on_time, False)
        assert_borrows(on_time_filter_response, on_time)
        assert_borrows(on_time_filter_response, overdue, False)
