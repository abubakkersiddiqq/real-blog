import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine 
from sqlalchemy.orm import DeclarativeBase



load_dotenv()
# 1. Changed to +asyncpg
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"statement_cache_size": 0},
    echo=True,
)

class Base(DeclarativeBase):
    pass

# Setup for session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session