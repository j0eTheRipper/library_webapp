URL = 'http://localhost/signup/'


def test_signup(client, authenticate):
    assert client.get(URL).status_code == 200

    response = authenticate.signup('new_user', 'password', 'password')
    assert response.headers['Location'] == 'http://localhost/'

    test_registered_user(authenticate, client)


def test_registered_user(authenticate, client):
    response = authenticate.signup('new_user', 'password', 'password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b'This username is already registered' in response.data


def test_non_matching_passwords(authenticate, client):
    response = authenticate.signup('new_guy', 'password', 'different_password')
    assert response.headers['Location'] == URL

    response = client.get(URL)
    assert b"The passwords don't match" in response.data
