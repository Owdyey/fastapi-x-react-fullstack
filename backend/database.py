from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

SQLALCHEMY_DB_URL = "sqlite:///sqlite.db"

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)

session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()