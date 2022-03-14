URL = 'http://localhost/borrow/browse'


def test_invalid_access(client):
    response = client.get(URL)
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/login/'


def test_valid_access(client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 200
