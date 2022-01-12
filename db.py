from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date
from app import app

engine = create_engine(app.config.get('SQLALCHEMY_DATABASE_URI'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class BookExists(BaseException):
    pass


class SubjectNotFound(BaseException):
    pass


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
        title = ' '.join(title.split()).title()
        book_exists = session.query(Book).filter_by(Book.title=title).first()

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
