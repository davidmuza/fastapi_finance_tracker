from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


async def add_income(db: AsyncSession, current_user: User, operation: OperationRequest) -> dict:
    if not await wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet '{operation.wallet_name}' not found.")
    
    wallet = await wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    await db.commit()
    
    return {
        "message": "Income added!",
        "wallet": wallet.name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }


async def add_expense(db: AsyncSession, current_user: User, operation: OperationRequest) -> dict:
    if not await wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet '{operation.wallet_name}' not found.")
        
    wallet = await wallets_repository.get_wallet_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient funds. Available: {wallet.balance}")
    
    wallet = await wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    await db.commit()
    
    return {
        "message": "Expense added!",
        "wallet": wallet.name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }