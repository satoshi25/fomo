from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL, echo=False)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()
