import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def all_post(db: AsyncSession):
    # Use selectinload so the 'author' data is ready for the HTML
    query = select(models.Post).options(selectinload(models.Post.author))
    result = await db.execute(query)
    return result.scalars().all()
    
async def get_user(db: AsyncSession, user_id: int = None, username: str = None, email: str = None):

    query = select(models.User).options(
        selectinload(models.User.posts).selectinload(models.Post.author)
    )
    
    if user_id:
        query = query.where(models.User.id == user_id)
    if username:
        query = query.where(models.User.username == username)
    if email:
        query = query.where(models.User.email == email)
        
    result = await db.execute(query)
    return result.scalars().first()

async def get_post(db: AsyncSession, user_id: int = None, post_id: int = None):

    query = select(models.Post).options(selectinload(models.Post.author))
    if user_id:
        query = query.where(models.Post.user_id == user_id)
    if post_id:
        query = query.where(models.Post.id == post_id)
    result = await db.execute(query)
    return result.scalars().first() 

async def get_user_posts(db: AsyncSession, user_id: int = None):
    query = select(models.Post).options(selectinload(models.Post.author))
    if user_id:
            query = query.where(models.Post.user_id == user_id)
            result = await db.execute(query)
            return result.scalars().all()
    return []