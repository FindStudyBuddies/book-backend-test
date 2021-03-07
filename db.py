import flask
import logging
import sqlalchemy 
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_pass = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

Base = declarative_base()

class Book(Base):  
    __tablename__ = 'books'

    
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    first_sentence = Column(String)
    published = Column(Integer)
    # TODO: create a __repr__ function

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
    url = "postgresql+pg8000://" + db_user + ":" + db_pass + "@35.230.182.58/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name+ "/.s.PGSQL.5432"
    urlMySQL = "mysql://" + db_user + ":" + db_pass + "@35.245.6.29/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name
    localUrl3 = "postgresql+pg8000://" + db_user + ":" + db_pass + "@127.0.0.1:5432/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name+ "/.s.PGSQL.5432"
    localUrl = "postgresql+pg8000://" + db_user + ":" + "@127.0.0.1:5432/" + db_name
    localUrl2 = "postgresql+pg8000://localhost:5432"
    print(url)
    #engine = sqlalchemy.create_engine(url)
    engine = sqlalchemy.create_engine(localUrl)
    engine.dialect.description_encoding = None
    Session = sessionmaker(bind=engine)
    print(db_user)
    print(db_pass)
    print(db_name)
    print(db_connection_name)
    print(db_socket_dir)
    return Session 
    #unix_socket = '/cloudsql/{}'.format(db_connection_name)
                #host='localhost',
    #try:
    #    print("in try block")
    #    conn = pymysql.connect(
    #            host='35.245.6.29', 
    #            unix_socket=unix_socket, 
    #            user=db_user, 
    #            passwd=db_password,
    #            db=db_name,
    #            cursorclass=pymysql.cursors.DictCursor
    #    )
    #    print()
    #    print(conn)
    #    print()
    #    return conn
    #except pymysql.MySQLError as e:
    #    print(e)

    #return None


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

    with conn.connect() as cursor:
        result = cursor.execute('SELECT * FROM books;')
        result2 = cursor.execute('SELECT json_agg(books) FROM books;')

        books = result.fetchall()
        books2 = result2.fetchall()
        temp = []
        temp2 = []
        print(result)
        print(books)
        for row in books:
            print(row)
            row = list(row)
            temp.append(row)

        for row in books2:
            print(row)
            row = list(row)
            temp2.append(row)

        return { 'result1': temp, 'result2': temp2 }

        return flask.jsonify(temp)
        if len(books) > 0:
            got_books = flask.jsonify(books)
        else:
            got_books = 'No Songs in DB'
    conn.close()
    return got_books

def add_books(book):
    print(book)
    Session = open_connection()
    session = Session()
    logging.debug("made it past connection")
    print("past connection")
    newBook = Book(title=book['title'], author=book['author'], first_sentence=book['first_sentence'], published=book['published'])
    session.add(newBook)
    session.commit()
    return {'status_code': 200, 'book': book } 
    with conn.connect() as cursor:
        try:
            cursor.execute('INSERT INTO books (title, author, first_sentence, published) VALUES(%s, %s, %s, %s)', (book["title"], book["author"], book["first_sentence"], book["published"]))
        except Exception as e:
            logging.debug("adding book failed")
            logging.debug(e)
            print(e)
            return e
    logging.debug("made it passed committing")
    print("past committing")
