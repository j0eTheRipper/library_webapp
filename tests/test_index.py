def test_guest(client):
    response = client.get('/')
    assert response.status_code == 200
