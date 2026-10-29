from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.models import User, Wallet


async def test_create_user_succes(db_session: AsyncSession, client: AsyncClient):
    response = await client.post(
        "/api/v1/users",
        json={"login": "user"})
    
    assert response.status_code == 200
    

async def test_create_user_already_exists(db_session: AsyncSession, client: AsyncClient):
    user = User(login="user")
    db_session.add(user)
    await db_session.commit()
    
    response = await client.post(
        "/api/v1/users",
        json={"login": "user"})
    
    assert response.status_code == 400