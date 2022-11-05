def unauthorized_access(client, url):
    pre_login_response = client.get(url)
    assert pre_login_response.status_code == 401
    assert pre_login_response.headers['Location'] == '/login/'


def request_user_page(client, authenticate, url, username, passwd):
    authenticate.login(username, passwd)
    response = client.get(url)
    assert response.status_code == 200
    return response
