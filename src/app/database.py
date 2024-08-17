from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://postgres:password@postgres:5433/card_app")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
new_session = sessionmaker(engine, expire_on_commit=False)

def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
