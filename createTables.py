import flask
import logging
import sqlalchemy 
import os
from sqlalchemy.orm import sessionmaker, relationship
from dao_author import Author
from dao_book import Book
from dao_test import Test
from base import Base


db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_pass = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

localUrl = "postgresql+pg8000://" + db_user + ":" + "@127.0.0.1:5432/" + db_name
#engine = sqlalchemy.create_engine(url)
engine = sqlalchemy.create_engine(localUrl, echo=True)
engine.dialect.description_encoding = None
Base.metadata.create_all(engine)
