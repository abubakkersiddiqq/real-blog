import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine

Base.metadata.create_all(bind= engine)

def all_post(db : Session):
    query = select(models.Post)
    return db.execute(query).scalars().all()
    

def get_user(db: Session, user_id: int = None, username: str = None, email: str = None):
    query = select(models.User)
    if user_id:
        query = query.where(models.User.id == user_id)
    if username:
        query = query.where(models.User.username == username)
    if email:
        query = query.where(models.User.email == email)
    return db.execute(query).scalars().first()

def get_post(db: Session, user_id: int = None, post_id: int = None):
    query = select(models.Post)
    if user_id:
        query = query.where(models.Post.user_id == user_id)
    if post_id:
        query = query.where(models.Post.id == post_id)
    
    return db.execute(query).scalars().first()

def get_user_posts(db : Session, user_id: int = None):
    query = select(models.Post)
    if user_id:
            query = query.where(models.Post.user_id == user_id)
            return db.execute(query).scalars().all()