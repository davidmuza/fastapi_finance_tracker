from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import users as users_repository
from app.schemas import UserResponse


async def create_user(db: AsyncSession, login: str) -> UserResponse:
    if await users_repository.get_user(db, login=login):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!")
    
    user = await users_repository.create_user(db, login=login)
    await db.commit()
    return user