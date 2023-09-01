from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import MYSQL_URL

DATABASE_URL = MYSQL_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()
