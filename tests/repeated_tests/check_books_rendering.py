def db_test(state=False):
    def pseudo_decorator(func):
        def wrapper(app, client, authenticate):
            func(app, client, authenticate)

            with app.app_context():
                from app.database_config.db import get_db
                from app.database_config.models import Borrows

                db = get_db()
                if state:
                    borrows = db.query(Borrows).all()
                    assert len(borrows) == 7
                    assert borrows[-1].book == '1984'
                else:
                    borrow = db.query(Borrows).filter_by(id=7).first()
                    assert not borrow
        return wrapper
    return pseudo_decorator


def assert_books(response, book_list, book_in_page=True):
    for book in book_list:
        if book_in_page:
            assert bytes(book.title, encoding='UTF8') in response.data
        else:
            assert not bytes(book.title, encoding='UTF8') in response.data
