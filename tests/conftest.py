from pytest import fixture
from app import create_app
from sqlalchemy.sql import text


@fixture(scope='session')
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE': 'sqlite://',
        }
    )

    with app.app_context():
        from app.database_config.db import init_db
        from app.database_config.models import engine

        init_db()
        with engine.connect() as connection:
            with open(f'test.sql') as script:
                query = ''
                for line in script:
                    query += line
                    if ';' in query:
                        connection.execute(text(query))
                        query = ''

    yield app


@fixture(scope='session')
def client(app):
    return app.test_client()


@fixture(scope='session')
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

    def add_user(self, username, password, password_conf, fullname, class_id):
        data = {
            'username': username,
            'password': password,
            'password_confirmation': password_conf,
            'fullname': fullname,
            'class_id': class_id,
        }

        return self.__client.post('/manage_users/add_user/', data=data)


@fixture(scope='session')
def authenticate(client):
    return AuthActions(client)
