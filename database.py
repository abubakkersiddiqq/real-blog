from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine 
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "postgresql+psycopg2://postgres:123@127.0.0.1:5432/blog_db"

engine = create_async_engine(
    DATABASE_URL,
    connect_args ={"check_same_thread": False},  
    echo=True
    )

class Base(DeclarativeBase):
    pass

#setup for session 
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db():
    async with AsyncSessionLocal as session:
        yield session
