from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import CreateWalletRequest, TotalBalance, WalletResponse
from app.service import wallets as wallets_service
from app.dependencies import get_async_db, get_current_user

router = APIRouter()


@router.get("/balance", response_model=TotalBalance)
async def get_balance( db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)) -> TotalBalance:
    return await wallets_service.get_total_balance(db, current_user)
    
    
@router.post("/wallets", response_model=WalletResponse)
async def create_wallet(wallet: CreateWalletRequest, 
                        db: AsyncSession = Depends(get_async_db),
                        current_user: User = Depends(get_current_user)) -> WalletResponse:
    return await wallets_service.create_wallet(db, current_user, wallet)


@router.get("/wallets", response_model=list[WalletResponse])
async def get_wallets(db: AsyncSession = Depends(get_async_db), current_user: User = Depends(get_current_user)) -> list[WalletResponse]:
    return await wallets_service.get_wallets(db, current_user)