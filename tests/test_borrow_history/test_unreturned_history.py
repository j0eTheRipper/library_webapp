from datetime import date
from tests.repeated_tests.repeated_request_tests import *

from .assert_borrows import assert_borrows
URL = 'http://localhost/borrows/history_unreturned'


def test_unauthorized_accesses(client):
    unauthorized_access(client, URL)


def test_user_view(app, client, authenticate):
    response = request_user_page(client, authenticate, URL, 'user', 'user')

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()

        user_borrows = db.query(Borrows).filter_by(borrower='user')
        returned_borrows = user_borrows.filter(Borrows.date_returned).all()
        unreturned_borrows = user_borrows.filter_by(date_returned=None).all()
        other_borrows = db.query(Borrows).filter(Borrows.borrower != 'user').all()

        assert_borrows(response, unreturned_borrows)
        assert_borrows(response, returned_borrows, False)
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

        assert_borrows(response, unreturned_borrows)
        assert_borrows(response, returned_borrows, False)


def test_filters(app, client, authenticate):
    authenticate.login('user', 'user')
    overdue_filter_response = client.get(f'{URL}?filter=overdue')
    on_time_filter_response = client.get(f'{URL}?filter=on_time')

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Borrows

        db = get_db()
        user_borrows_query = db.query(Borrows).filter_by(borrower='user').filter_by(date_returned=None)
        overdue = user_borrows_query.filter(date.today() > Borrows.due_date).all()
        on_time = user_borrows_query.filter(date.today() <= Borrows.due_date).all()

        assert_borrows(overdue_filter_response, overdue)
        assert_borrows(overdue_filter_response, on_time, False)
        assert_borrows(on_time_filter_response, on_time)
        assert_borrows(on_time_filter_response, overdue, False)
