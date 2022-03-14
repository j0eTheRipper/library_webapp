URL = 'http://localhost/login/'


def test_login(client, authenticate):
    assert client.get(URL).status_code == 200

    response = authenticate.login('admin', 'admin')
    assert response.headers['Location'] == 'http://localhost/'


def test_wrong_password(authenticate, client):
    response = authenticate.login('admin', 'wrong_password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'Incorrect Password' in response.data


def test_unregistered_username(authenticate, client):
    response = authenticate.login('un_registered', 'password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is not registered' in response.data
