from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=admin123")
    cursor = conn.cursor(row_factory=dict_row)
    print('Database connection established successfully!')
except Exception as error:
    print('Connection to database failed!')
    print('Error: ', error)
