URL = 'http://localhost/borrow/browse'


def test_invalid_access(client):
    response = client.get(URL)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/login/'


def test_valid_access(app, client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Books

        db = get_db()
        all_books = db.query(Books).all()

        assert_books(response, all_books)


def test_subject_filter(app, client, authenticate):
    authenticate.login('admin', 'admin')
    url = f'{URL}?subject=Story'
    response = client.get(url)
    assert response.status_code == 200

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Subject, Books

        db = get_db()
        stories = db.query(Subject).filter_by(subject='Story').first().books
        all_books = db.query(Books).filter(Books.subject != 'Story').all()

        assert_books(response, stories)
        assert_books(response, all_books, False)


def assert_books(response, book_list, book_in_page=True):
    for book in book_list:
        if book_in_page:
            assert bytes(book.title, encoding='UTF8') in response.data
        else:
            assert not bytes(book.title, encoding='UTF8') in response.data
