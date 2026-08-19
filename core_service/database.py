import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# init engine
engine = create_engine(DATABASE_URL)

# init SessionLocal & Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# get_db()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
