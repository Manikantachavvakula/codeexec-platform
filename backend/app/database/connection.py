import os
from pymongo import MongoClient
import motor.motor_asyncio
from typing import Any, Dict

from app.config import DATABASE_TYPE, DATABASE_URL

# MongoDB Connection
async def get_mongodb_connection():
    """Create and return an async MongoDB connection"""
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    return client

# PostgreSQL Connection (alternative)
async def get_postgres_connection():
    """PostgreSQL connection using SQLAlchemy"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    DATABASE_URL_ASYNC = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
    engine = create_async_engine(DATABASE_URL_ASYNC)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session()

# Database connection factory
async def get_db_connection():
    """Return appropriate database connection based on configuration"""
    if DATABASE_TYPE.lower() == "mongodb":
        return await get_mongodb_connection()
    else:
        return await get_postgres_connection()