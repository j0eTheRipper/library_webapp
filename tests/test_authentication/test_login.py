from flask import session

URL = 'http://localhost/login/'


def test_login_admin(client, authenticate):
    assert client.get(URL).status_code == 200

    response = authenticate.login('admin', 'admin')
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        response = client.get('http://localhost/')
        assert session['is_admin']

        assert b'Manage Books' in response.data
        assert b'Unreturned Books (2)' in response.data
        assert b'Borrow History' in response.data
        assert b'Manage Users' in response.data
        assert b'Logout' in response.data
        assert b'You have 2 books that need to be returned!' not in response.data


def test_login_user(client, authenticate):
    response = authenticate.login('user', 'user')
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        response = client.get('http://localhost/')
        assert not session['is_admin']

        assert b'Browse Books' in response.data
        assert b'Manage Books' not in response.data
        assert b'Unreturned Books (1)' in response.data
        assert b'Borrow History' in response.data
        assert b'Logout' in response.data


def test_wrong_password(authenticate, client):
    response = authenticate.login('admin', 'wrong_password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'Incorrect Password' in response.data


def test_unregistered_username(authenticate, client):
    response = authenticate.login('un_registered', 'password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is not registered! Please contact the admins.' in response.data


def test_incomplete_request(client):
    data_list = [{'username': '', 'password': 'abc'},
                 {'username': 'abc', 'password': ''},
                 {'username': '', 'password': ''}]

    for data in data_list:
        response = client.post(URL, data=data)
        assert response.headers['Location'] == URL

        response = client.get(URL)
        assert b'Please provide a username and a password' in response.data
