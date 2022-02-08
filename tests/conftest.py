from app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': 'db.sqlite'
    })

    yield app


@pytest.fixture
def cli(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
