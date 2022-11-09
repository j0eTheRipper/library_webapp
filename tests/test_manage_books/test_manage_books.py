from tests.repeated_tests.repeated_request_tests import unauthorized_access

URL = '/manage_books/'


def test_unauthorized_access(client):
    unauthorized_access(client, URL)


def test_user_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)
    assert response.status_code == 403


def test_admin_access(client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)
    assert response.status_code == 302
    assert response.headers['Location'] == '/browse/'
