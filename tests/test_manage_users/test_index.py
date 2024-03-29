from tests.repeated_tests.repeated_request_tests import unauthorized_access, request_user_page


URL = 'http://localhost/manage_users/'


def test_unauthorized_access(client):
    unauthorized_access(client, URL)


def test_normal_user_access(client, authenticate):
    authenticate.login('user', 'user')
    response = client.get(URL)

    assert response.status_code == 403


def test_valid_access(client, authenticate):
    authenticate.login('admin', 'admin')
    response = client.get(URL)

    assert response.status_code == 200
