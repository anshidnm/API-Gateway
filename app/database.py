from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os


DRIVER = os.getenv("DB_DRIVER")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
NAME = os.getenv("DB_NAME")


SQL_DB_URL =  f"{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_engine(SQL_DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()