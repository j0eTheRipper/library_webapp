def test_login(client, auth):
    auth.login()
    response = client.get('/')

    assert response.status_code == 205


def test_invalid_login(client, auth):
    none_existing_user = auth.login('jack', 'some_password')
    wrong_password = auth.login('test', 'some_thing')

    assert none_existing_user.status_code == 305
    assert wrong_password.status_code == 305


def test_signup(client, auth, app):
    auth.signup('j0e', 'mpkfa', 'mpkfa')
    with app.app_context():
        from app.database_config.db import get_db, close_db
        from app.database_config.models import Users
        db = get_db()
        user_record = db.query(Users).filter_by(username='j0e').first()
        close_db()

    assert user_record


def test_invalid_signup(auth):
    exists_response = auth.signup('j0e', 'mpkfa', 'mpkfa')
    passwords_not_matching_response = auth.signup('jack', 'mpkaa', 'mpkfa')
    invalid_username_response = auth.signup('jack the ripper', 'mkkffa', 'mkkffa')

    assert exists_response.status_code == 300
    assert passwords_not_matching_response.status_code == 300
    assert invalid_username_response.status_code == 300