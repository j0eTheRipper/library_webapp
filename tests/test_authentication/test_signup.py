from tests.repeated_tests.repeated_request_tests import unauthorized_access


URL = 'http://localhost/signup/'


def test_signup(app, client, authenticate):
    assert client.get(URL).status_code == 401
    authenticate.login('admin', 'admin')

    assert client.get(URL).status_code == 200

    response = authenticate.signup('new_user', 'password', 'password')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Users

        db = get_db()
        new_user_db_record = db.query(Users).filter_by(username='new_user').first()
        assert new_user_db_record is not None
        assert not new_user_db_record.is_admin


def test_registered_user(app, authenticate, client):
    authenticate.login('admin', 'admin')
    response = authenticate.signup('admin', 'password', 'password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is already registered' in response.data


def test_non_matching_passwords(authenticate, client):
    authenticate.login('admin', 'admin')
    response = authenticate.signup('new_guy', 'password', 'different_password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b"Passwords do not match!" in response.data

    
def test_incomplete_request(client, authenticate):
    authenticate.login('admin', 'admin')
    data_list = [{'username': '', 'password': 'abc'},
                 {'username': 'abc', 'password': ''},
                 {'username': '', 'password': ''}]

    for data in data_list:
        response = client.post(URL, data=data)
        assert response.headers['Location'] == URL

        response = client.get(URL)
        assert b'Please provide a username and a password' in response.data


def test_normal_user_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)

    assert response.status_code == 403


def test_guest_user_access(client):
    unauthorized_access(client, URL)
