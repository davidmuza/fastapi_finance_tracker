from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import CreateWalletRequest, WalletResponse
from app.repository import wallets as wallets_repository


async def get_balance(db: AsyncSession, current_user: User, wallet_name: str | None = None) -> WalletResponse:
    if wallet_name is None:
        wallets = await wallets_repository.get_all_wallets(db, current_user.id)
        return {"total": sum(float(w.balance) for w in wallets)}
    
    if not await wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet '{wallet_name}' not found.")
        
    wallet = await wallets_repository.get_wallet_by_name(db, current_user.id, wallet_name)
    return WalletResponse.model_validate(wallet)


async def create_wallet(db: AsyncSession, current_user: User, wallet: CreateWalletRequest) -> WalletResponse:
    if await wallets_repository.is_wallet_exist(db, current_user.id, wallet.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Wallet '{wallet.name}' already exists.")
        
    wallet_db = await wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    await db.commit()
        
    return WalletResponse.model_validate(wallet_db)