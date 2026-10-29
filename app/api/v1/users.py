from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserRequest, UserResponse
from app.dependencies import get_async_db, get_current_user
from app.service import users as users_service

router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user(payload: UserRequest, db: AsyncSession = Depends(get_async_db)) -> UserResponse:
    return await users_service.create_user(db, payload.login)


@router.get("users/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user