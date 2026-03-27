import models
from sqlalchemy import select, func
from database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def list_posts(db: AsyncSession, ):
    # Use selectinload so the 'author' data is ready for the HTML
    query = select(models.Post).options(selectinload(models.Post.author)).order_by(models.Post.date_posted.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_user_by_id(db, user_id: int):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    return result.scalars().first()
    
async def get_user_with_posts(db: AsyncSession, user_id: int = None, username: str = None, email: str = None):

    query = select(models.User).options(
        selectinload(models.User.posts).selectinload(models.Post.author)
    )
    
    if user_id is not None:
        query = query.where(models.User.id == user_id)
    if username:
        query = query.where(func.lower(models.User.username) == username.lower())
    if email:
        query = query.where(func.lower(models.User.email) == email.lower())
        
    result = await db.execute(query)
    return result.scalars().first()


# user verification (token)  
from sqlalchemy import or_, func

async def get_user_for_auth(db: AsyncSession, identifier: str):
    query = select(models.User).where(
        or_(
            func.lower(models.User.username) == identifier.lower(),
            func.lower(models.User.email) == identifier.lower()
        )
    )
    result = await db.execute(query)
    return result.scalars().first()

#verfication of username (database) and email
async def get_user_by_username_or_email(db: AsyncSession, username : str = None, email: str = None): # Formdata.username.lower
    query = select(models.User)
    
    if username:
        query = query.where(func.lower(models.User.username) == username.lower())

    if email:
        query = query.where(func.lower(models.User.email) == email.lower())
        
    result = await db.execute(query)
    return result.scalars().first()

#-------------POST--------------

async def get_post_by_id(db: AsyncSession, user_id: int = None, post_id: int = None):
    query = select(models.Post).options(selectinload(models.Post.author))
    if user_id is not None:
        query = query.where(models.Post.user_id == user_id)
    if post_id:
        query = query.where(models.Post.id == post_id)
    result = await db.execute(query)
    return result.scalars().first() 

async def get_posts_by_user(db: AsyncSession, user_id: int = None):
    query = select(models.Post).options(selectinload(models.Post.author)).order_by(models.Post.date_posted.desc())
    if user_id is not None:
            query = query.where(models.Post.user_id == user_id)
            result = await db.execute(query)
            return result.scalars().all()
    return []