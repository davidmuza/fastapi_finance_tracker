from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import CreateWalletRequest, WalletResponse
from app.service import wallets as wallets_service
from app.dependencies import get_async_db, get_current_user

router = APIRouter()


@router.get("/balance", response_model=WalletResponse)
async def get_balance(wallet_name: str | None = None, 
                      db: AsyncSession = Depends(get_async_db),
                      current_user: User = Depends(get_current_user)) -> dict:
    return await wallets_service.get_balance(db, current_user, wallet_name)
    
    
@router.post("/wallets", response_model=WalletResponse)
async def create_wallet(wallet: CreateWalletRequest, 
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_user)) -> dict:
    return await wallets_service.create_wallet(db, current_user, wallet)