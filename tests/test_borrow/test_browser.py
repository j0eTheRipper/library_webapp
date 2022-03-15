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

        for book in all_books:
            assert bytes(book.title, encoding='UTF8') in response.data
            assert bytes(book.author, encoding='UTF8') in response.data
            assert bytes(book.subject, encoding='UTF8') in response.data
            assert bytes(str(book.count), encoding='UTF8') in response.data
