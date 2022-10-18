from flask import g
from flask.cli import with_appcontext
import click
from .models import Session, Base, Subject, Users


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

    subjects = {'Math', 'Physics', 'Computer', 'Story', 'Biology', 'Engineering', 'SAT', 'English', 'Chemistry',
                'General Knowledge', 'Arabic', 'philosophy', 'psychology', 'business'}
    subject_db = [Subject(subject=subject) for subject in subjects]

    admin_user = Users.create_user('moisadmin', 'admin1984', 'Mohammed Nasr', class_id=None, is_admin=True)

    with Session() as session:
        session.add_all(subject_db)
        session.add(admin_user)
        session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('created successfully')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
