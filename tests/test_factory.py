from app import create_app
from flask import render_template


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_main_page(cli):
    response = cli.get('/')
    assert response.status_code == 200
