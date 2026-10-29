from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import OperationRequest
from app.service import operations as operations_service
from app.dependencies import get_async_db, get_current_user

router = APIRouter()


@router.post("/operations/income")
async def add_income(operation: OperationRequest, 
                     db: AsyncSession = Depends(get_async_db),
                     current_user: User = Depends(get_current_user)) -> dict:
    return await operations_service.add_income(db, current_user, operation)
     
     
@router.post("/operations/expense")
async def add_expense(operation: OperationRequest, 
                      db: AsyncSession = Depends(get_async_db),
                      current_user: User = Depends(get_current_user)) -> dict:
    return await operations_service.add_expense(db, current_user, operation)