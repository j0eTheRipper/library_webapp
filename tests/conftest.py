from os.path import isfile

from pytest import fixture
from werkzeug.security import generate_password_hash

from app import create_app
from . import db_path


@fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE': db_path,
        }
    )

    if not isfile(db_path):
        with app.app_context():
            from app.database_config.db import init_db, get_db
            from app.database_config.models import Users

            init_db()
            db = get_db()
            user = Users(username='test', password=generate_password_hash('no_thing'))
            admin = Users(
                username='test_admin',
                password=generate_password_hash('really_complex_password'),
                is_admin=True
            )
            db.add_all([user, admin])
            db.commit()

    yield app


@fixture
def client(app):
    return app.test_client()


class Authenticate:
    def __init__(self, client):
        self.cli = client

    def login(self, username='test', password='no_thing'):
        data = {
            'username': username,
            'password': password,
        }

        return self.cli.post('/login/', data=data)

    def signup(self, username, password, password_confirmation):
        data = {
            'username': username,
            'password': password,
            'password_confirmation': password_confirmation,
        }

        return self.cli.post('/signup/', data=data)


@fixture
def auth(client):
    return Authenticate(client)
