from pytest import fixture
from app import create_app
from werkzeug.security import generate_password_hash


@fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE': 'testing.sqlite',
        }
    )

    with app.app_context():
        from app.database_config.db import get_db, init_db, close_db
        from app.database_config.models import Users

        init_db()
        admin = Users(username='admin', password=generate_password_hash('admin'), is_admin=True)
        normal_user = Users(username='user', password=generate_password_hash('password'), is_admin=False)

        db = get_db()
        db.add_all([admin, normal_user])
        db.commit()
        close_db()

    yield app


@fixture
def client(app):
    return app.test_client()


@fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self.__client = client

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }

        return self.__client.post('/login/', data=data)

    def logout(self):
        return self.__client.get('/login/logout')

    def signup(self, username, password, password_conf):
        data = {
            'username': username,
            'password': password,
            'password_confirmation': password_conf,
        }

        return self.__client.post('/signup/', data=data)


@fixture
def authenticate(client):
    return AuthActions(client)
