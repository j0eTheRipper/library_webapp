from pytest import fixture
from app import create_app
from sqlite3 import connect
from os import remove


@fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE': 'testing.sqlite',
        }
    )

    with app.app_context():
        from app.database_config.db import init_db

        init_db()
        with connect('testing.sqlite') as connection:
            with open(f'test.sql') as script:
                connection.executescript(script.read())

    yield app
    remove('testing.sqlite')


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
