from tests.repeated_tests.repeated_request_tests import unauthorized_access


URL = '/manage_users/add_user/'


def test_add_user(app, client, authenticate):
    assert client.get(URL).status_code == 401
    authenticate.login('admin', 'admin')

    assert client.get(URL).status_code == 200

    response = authenticate.add_user('new_user', 'password', 'password', 'joe guage', '12D')
    assert response.headers['Location'] == '/'

    with app.app_context():
        from app.database_config.db import get_db
        from app.database_config.models import Users

        db = get_db()
        new_user_db_record = db.query(Users).filter_by(username='new_user').first()
        assert new_user_db_record is not None
        assert not new_user_db_record.is_admin


def test_registered_user(app, authenticate, client):
    authenticate.login('admin', 'admin')
    response = authenticate.add_user('admin', 'password', 'password', 'john ruth', '')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is already registered' in response.data


def test_non_matching_passwords(authenticate, client):
    authenticate.login('admin', 'admin')
    response = authenticate.add_user('new_guy', 'password', 'different_password', 'oswaldo mobray', '9C')
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
        assert b'Please fill out all the fields' in response.data


def test_normal_user_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)

    assert response.status_code == 403


def test_guest_user_access(client):
    unauthorized_access(client, URL)
