from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:123@127.0.0.1:5432/blog_db"

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

#setup for session 
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind= engine)
def get_db():
    db = SessionLocal()
    try:
       yield db

    finally:
        db.close()

