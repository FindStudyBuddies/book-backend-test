import flask
import logging
import pymysql
import os

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
                #host='localhost',
    try:
        print("in try block")
        conn = pymysql.connect(
                host='35.245.6.29', 
                unix_socket=unix_socket, 
                user=db_user, 
                passwd=db_password,
                db=db_name,
                cursorclass=pymysql.cursors.DictCursor
        )
        print()
        print(conn)
        print()
        return conn
    except pymysql.MySQLError as e:
        print(e)

    return None


def get_books():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM books;')
        books = cursor.fetchall()
        if result > 0:
            got_books = flask.jsonify(books)
        else:
            got_books = 'No Songs in DB'
    conn.close()
    return got_books

def add_books(book):
    print(book)
    conn = open_connection()
    logging.debug("made it past connection")
    print("past connection")
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO books (title, author, first_sentence, published) VALUES(%s, %s, %s, %s)', (book["title"], book["author"], book["first_sentence"], book["published"]))
        except Exception as e:
            logging.debug("adding book failed")
            logging.debug(e)
            print(e)
            return e
    conn.commit()
    logging.debug("made it passed committing")
    print("past committing")
    conn.close()
