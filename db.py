import flask
import logging
import sqlalchemy 
import os
from sqlalchemy.orm import sessionmaker, relationship
from dao_author import Author
from dao_book import Book
from base import Base


db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_pass = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    # Equivalent URL:
    #sqlalchemy.engine.url.URL(
        #    drivername="postgresql+pg8000",
        #    username=db_user,  # e.g. "my-database-user"
        #    password=db_pass,  # e.g. "my-database-password"
        #    database=db_name,  # e.g. "my-database-name"
        #    query={
        #        "unix_sock": "{}/{}/.s.PGSQL.5432".format(
        #            db_socket_dir,  # e.g. "/cloudsql"
        #            db_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
        #    }
        #)
    #url = "postgresql+pg8000://" + db_user + ":" + db_pass + "@35.230.182.58/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name+ "/.s.PGSQL.5432"
    #urlMySQL = "mysql://" + db_user + ":" + db_pass + "@35.245.6.29/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name
    localUrl = "postgresql+pg8000://" + db_user + ":" + "@127.0.0.1:5432/" + db_name
    #engine = sqlalchemy.create_engine(url)
    engine = sqlalchemy.create_engine(localUrl, echo=True)
    engine.dialect.description_encoding = None
    Session = sessionmaker(bind=engine)
    #Base.metadata.create_all(engine)
    print(db_user)
    print(db_pass)
    print(db_name)
    print(db_connection_name)
    print(db_socket_dir)
    return Session 
    #unix_socket = '/cloudsql/{}'.format(db_connection_name)
                #host='localhost',

def get_books():
    Session = open_connection()
    session = Session()
    temp = []
    for instance in session.query(Book).order_by(Book.book_id):
        obj = {
                'id': instance.book_id,
                'title': instance.title,
                'author': instance.author,
                'published': instance.published,
                'first_sentence': instance.first_sentence
                }
        temp.append(obj)

    return {'result': temp }

def add_book(book):
    print(book)
    Session = open_connection()
    session = Session()
    logging.debug("made it past connection")
    print("past connection")
    if (not book['author_first_name'] or not book['author_last_name']):
        return {'status_code': 400, 'message': "author first name or last name not given" }
    author = session.query(Author).filter(Author.author_first_name == book['author_first_name'], Author.author_last_name == book['author_last_name']).one()
    newBook = Book(title=book['title'], author_id=author.author_id, first_sentence=book['first_sentence'], published=book['published'])
    #newBook.author = author
    print("Author books: ")
    print(author.books)
    print("Book author: ")
    print(newBook.author)
    session.add(newBook)
    session.commit()
    return {'status_code': 200, 'book': book } 

def add_author(author):
    print(author)
    Session = open_connection()
    session = Session()
    newAuthor = Author(author_first_name=author['author_first_name'], author_last_name=author['author_last_name'])
    session.add(newAuthor)
    session.commit()
    return {'status_code': 200, 'author': author }

def get_books_of_author(author):
    print(author)
    Session = open_connection()
    session = Session()
    auth = session.query(Author).filter(Author.author_first_name == author['author_first_name'], Author.author_last_name == author['author_last_name']).one()
    books = session.query(Author, Book).filter(auth.author_id == Book.author_id).all()
    return {'status_code': 200, 'result': books }
