def assert_book_in_db(new_book, required_len=1):
    from app.database_config.db import get_db
    from app.database_config.models import Books

    db = get_db()
    books = db.query(Books).filter_by(title=new_book['title']).all()
    assert len(books) == required_len
    return books
