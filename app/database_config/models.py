from datetime import date, timedelta
from sqlalchemy import create_engine, Column, Integer, ForeignKey, Boolean, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import current_app
from werkzeug.security import generate_password_hash

engine = create_engine(current_app.config.get('DATABASE'))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class Subject(Base):
    __tablename__ = 'subjects'

    subject = Column(String, primary_key=True)
    books = relationship('Books', backref='subjects')


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, unique=True, nullable=False)
    subject = Column(String, ForeignKey('subjects.subject'), nullable=False)
    author = Column(String, nullable=False)
    count = Column(Integer, default=1, nullable=False)
    borrows = relationship('Borrows', backref='books')

    def __repr__(self):
        return f'<Book {self.id}: {self.title}>'


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    fullname = Column(String, unique=True, nullable=False)
    class_id = Column(String, unique=False, index=True, nullable=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    borrows = relationship('Borrows', backref='users')

    @staticmethod
    def create_user(username, password, fullname, class_id, is_admin=False):
        passwd = generate_password_hash(password)
        user = Users(username=username, password=passwd, fullname=fullname, class_id=class_id, is_admin=is_admin)
        return user


class Borrows(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True)
    borrower = Column(String, ForeignKey('users.username'), nullable=False)
    book = Column(String, ForeignKey('books.title'), nullable=False)
    date_borrowed = Column(Date, default=date.today(), nullable=False)
    due_date = Column(Date, nullable=False)
    date_returned = Column(Date, nullable=True)

    @staticmethod
    def borrow_book(book: Books, user: Users):
        borrow_date = date.today()
        return_date = borrow_date + timedelta(days=7)
        borrow = Borrows(borrower=user.username, book=book.title, due_date=return_date)
        book.count -= 1
        return borrow, book

    @property
    def fullname(self):
        return self.__get_borrower_info()[0]

    @property
    def class_id(self):
        return self.__get_borrower_info()[1]

    def __get_borrower_info(self):
        username = self.borrower
        with Session() as session:
            record = session.query(Users).filter_by(username=username).first()
        return record.fullname, record.class_id

    def return_book(self, book):
        date_returned = date.today()
        self.date_returned = date_returned
        book.count += 1
        return self, book
