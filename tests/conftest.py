import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient
from collections.abc import AsyncGenerator

from app.main import app
from app.models import Base
from app.dependencies import get_async_db


TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test.sqlite3"

test_async_engine = create_async_engine(TEST_DATABASE_URL, 
                                        connect_args={"check_same_thread": False},)

test_async_session_maker = async_sessionmaker(test_async_engine, 
                                              expire_on_commit=False, 
                                              class_=AsyncSession)


async def get_test_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session
        
        
app.dependency_overrides[get_async_db] = get_test_async_db


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    
@pytest.fixture(autouse=True)
async def setup_db():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
        
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
        
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session