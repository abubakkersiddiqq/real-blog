import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine

Base.metadata.create_all(bind= engine)

def all_post(db : Session):
    query = select(models.Post)
    result = db.execute(query)
    return result.scalars().all()

def get_user_by_username(db : Session, username: str):
    query = select(models.User).where(models.User.username == username)
    result = db.execute(query)
    return result.scalars().first()

def get_email_by_username(db : Session, email: str):
    query = select(models.User).where(models.User.email == email)
    result = db.execute(query)
    return result.scalars().first()

def get_user_by_user_id(db : Session, user_id : int):#also post id
    query = select(models.User).where(models.User.id == user_id)
    result = db.execute(query)
    return result.scalars().first()

def get_user_posts(db: Session, user_id : int):
    query = select(models.Post).where(models.Post.user_id == user_id)
    result = db.execute(query)
    return result.scalars().all()

def get_post_by_post_id(db: Session, post_id: int):
    query = select(models.Post).where(models.Post.id == post_id)
    result = db.execute(query)
    return result.scalars().first()