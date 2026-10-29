from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Wallet


async def is_wallet_exist(db: AsyncSession, user_id: int, wallet_name: str) -> bool:
    result = await db.scalars(select(Wallet).filter_by(user_id=user_id, name=wallet_name))
    return result.first() is not None

async def get_wallet_by_name(db: AsyncSession, user_id: int, wallet_name: str) -> Wallet:
    result = await db.scalars(select(Wallet).filter_by(user_id=user_id, name=wallet_name))
    return result.first()

async def add_income(db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    result = await db.scalars(select(Wallet).filter_by(name=wallet_name, user_id=user_id))
    wallet = result.first()
    wallet.balance += amount
    await db.flush()
    return wallet

async def add_expense(db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    result = await db.scalars(select(Wallet).filter_by(name=wallet_name, user_id=user_id))
    wallet = result.first()
    wallet.balance -= amount
    await db.flush()
    return wallet

async def get_all_wallets(db: AsyncSession, user_id: int) -> list[Wallet]:
    result = await db.scalars(select(Wallet).filter_by(user_id=user_id))
    return result.all()

async def create_wallet(db: AsyncSession, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)
    db.add(wallet)
    await db.flush()
    await db.refresh(wallet)
    return wallet