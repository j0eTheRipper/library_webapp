from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import current_app
from sqlalchemy.orm import relationship
from .exceptions import *
from datetime import date

engine = create_engine('sqlite:///' + current_app.config.get('DATABASE'))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

def format_input(*names):
    result = []

    for name in names:
        name = ' '.join(name.split()).title()
        result.append(name)
    
    return result[0] if len(result) == 1 else result


class Subjects(Base):
    __tablename__ = 'subjects'

    subject = Column(String, primary_key=True)
    books = relationship('Book', backref='subject', uselist=True)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(32), unique=True, index=True)
    book_subject = Column(String, ForeignKey('subjects.subject'))
    count = Column(Integer, default=1)
    borrowed = relationship('Borrows', backref='book', uselist=False)

    @staticmethod
    def add_book(title: str, count=1, subject=None):
        title = format_input(title)
        with Session() as session:
            book_exists = session.query(Book).filter_by(title=title).first()

            if not book_exists:
                subject = session.query(Subjects).filter_by(subject=subject).first()

                if subject:
                    book = Book(title=title, count=count, subject=subject)
                else:
                    raise SubjectNotFound

                session.add(book)
                session.commit()
            else:
                raise BookExists


class Borrows(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True)
    borrower = Column(String(32), unique=True, index=True)
    book_title = Column(String, ForeignKey('book.title'))
    borrow_date = Column(Date, default=date.today())
    return_date = Column(Date)

    def borrow_book(self, book: str, borrower: str, return_date: date, borrow_date: date = date.today()):
        book, borrower = format_input(book, borrower)
        with Session() as session:
            book = session.query(Book).filter_by(title=book).first()
            name_exists = session.query(Borrows).filter_by(borrower=borrower).first()

        if book and book.count and not name_exists:
            self.register_borrow(borrower, book, borrow_date, return_date)
        elif not book:
            raise BookNotFound
        elif not book.count:
            raise OutOfBooks
        elif name_exists:
            raise ReturnFirst
    
    @staticmethod
    def register_borrow(borrower, book, borrow_date, return_date):
        borrow = Borrows(
            borrower=borrower,
            book=book,
            borrow_date=borrow_date,
            return_date=return_date,
        )

        book.count -= 1

        with Session() as session:
            session.add_all([borrow, book])
            session.commit()

