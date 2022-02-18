from datetime import date

from sqlalchemy import create_engine, Column, Integer, ForeignKey, Boolean, Date, String
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import current_app


engine = create_engine('sqlite:///' + current_app.config.get('DATABASE'))
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
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    borrows = relationship('Borrows', backref='users')


class Borrows(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True)
    borrower = Column(String, ForeignKey('users.username'), nullable=False)
    book = Column(String, ForeignKey('books.title'), nullable=False)
    date_borrowed = Column(Date, default=date.today(), nullable=False)
    date_returned = Column(Date, nullable=False)
    is_returned = Column(Boolean, default=False, nullable=False)
