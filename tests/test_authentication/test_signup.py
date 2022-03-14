URL = 'http://localhost/signup/'


def test_signup(app, client, authenticate):
    assert client.get(URL).status_code == 200

    response = authenticate.signup('new_user', 'password', 'password')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Users

        db = get_db()
        assert db.query(Users).filter_by(username='new_user').first() is not None


def test_registered_user(app, authenticate, client):
    response = authenticate.signup('admin', 'password', 'password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is already registered' in response.data


def test_non_matching_passwords(authenticate, client):
    response = authenticate.signup('new_guy', 'password', 'different_password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b"Passwords do not match!" in response.data
