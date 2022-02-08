def test_guest(client):
    response = client.get('/')
    assert response.status_code == 200


def test_logged_in(client, auth):
    auth.login()
    response = client.get('/')

    assert response.status_code == 205
