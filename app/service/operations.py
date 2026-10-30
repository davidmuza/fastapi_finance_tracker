from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.repository import wallets as wallets_repository
from app.repository import operations as operations_repository


async def add_income(db: AsyncSession, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not await wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet '{operation.wallet_name}' not found.")
    
    wallet = await wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    operation_db = await operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type="income",
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    await db.commit()
    
    return OperationResponse.model_validate(operation_db)


async def add_expense(db: AsyncSession, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not await wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Wallet '{operation.wallet_name}' not found.")
        
    wallet = await wallets_repository.get_wallet_by_name(db, current_user.id, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Insufficient funds. Available: {wallet.balance}")
    
    wallet = await wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    operation_db = await operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type="expense",
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description
    )
    await db.commit()
    
    return OperationResponse.model_validate(operation_db)


async def get_operations_list(
    db: AsyncSession,
    current_user: User,
    wallet_id: int | None,
    date_from: datetime | None,
    date_to: datetime | None,
) -> list[OperationResponse]:
    if wallet_id:
        wallet = await wallets_repository.get_wallet_by_id(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail=f"Wallet {wallet_id} not found.")

        wallets_ids = [wallet.id]

    else:
        wallets = await wallets_repository.get_all_wallets(db, current_user.id)
        wallets_ids = [w.id for w in wallets]

    operations = await operations_repository.get_operations_list(db, wallets_ids, date_from, date_to)
    return operations