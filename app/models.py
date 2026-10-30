from datetime import datetime
from locale import currency
from turtle import back
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, String, ForeignKey, func
from decimal import Decimal
from app.database import Base
from app.enum import CurrencyEnum


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    
    wallets: Mapped[list["Wallet"]] = relationship("Wallet", back_populates="user")


class Wallet(Base):
    __tablename__ = "wallets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    balance: Mapped[Decimal]
    currency: Mapped[CurrencyEnum] 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="wallets")

    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="wallet")



class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    type: Mapped[str]
    amount: Mapped[Decimal]
    currency: Mapped[CurrencyEnum]
    category: Mapped[str] = mapped_column(nullable=True, default=None)
    subcategory: Mapped[str] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)


    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="operations")