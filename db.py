import flask
import logging
import sqlalchemy 
import os


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
    url = "postgresql+pg8000://" + db_user + ":" + db_pass + "@35.230.182.58/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name+ "/.s.PGSQL.5432"
    urlMySQL = "mysql://" + db_user + ":" + db_pass + "@35.245.6.29/" + db_name + "?unix_sock=" + db_socket_dir + "/" + db_connection_name
    print(url)
    pool = sqlalchemy.create_engine(url)
    pool.dialect.description_encoding = None
    print(db_user)
    print(db_pass)
    print(db_name)
    print(db_connection_name)
    print(db_socket_dir)
    return pool
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
    conn = open_connection()
    with conn.connect() as cursor:
        result = cursor.execute('SELECT * FROM books;')
        books = result.fetchall()
        temp = []
        print(result)
        print(books)
        for row in result:
            print(row)
            print(row['title'])
            temp.append(row)

        return flask.jsonify(temp)
        if len(books) > 0:
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
