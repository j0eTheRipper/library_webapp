from flask import g
from flask.cli import with_appcontext
import click
from .models import Session, Base



def get_db():
    if 'db' not in g:
        g.db = Session()
        return g.db


def close_db(e=None):
    if 'db' in g:
        g.db.close()
        del g.db


def init_db():
    Base.metadata.drop_all()
    Base.metadata.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('created successfuly')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

