from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal

from app.enum import CurrencyEnum


class OperationRequest(BaseModel):
    wallet_name: str = Field(max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)
    
    # Валидатор для проверки, что сумма положительна
    @field_validator("amount")
    def amount_must_be_positive(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Amount must be positive!")
        
        return value
    
    # Валидатор для проверки, что имя не пустое
    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        
        if not value:
            raise ValueError("Wallet name cannot be empty!")
        
        return value
    

class CreateWalletRequest(BaseModel):
    name: str = Field(max_length=127)
    initial_balance: Decimal = 0
    currency: CurrencyEnum = CurrencyEnum.RUB
    
    # Валидатор для проверки, что баланс не отрицателен
    @field_validator("initial_balance")
    def balance_not_negative(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Initial balance cannot be negative!")
        
        return value
    
    # Валидатор для проверки, что имя не пустое
    @field_validator("name")
    def wallet_name_not_empty(cls, value: str) -> str:
        value = value.strip()
        
        if not value:
            raise ValueError("Wallet name cannot be empty!")
        
        return value


class WalletResponse(BaseModel):
    id: int
    name: str
    balance: float
    currency: CurrencyEnum

    model_config = ConfigDict(from_attributes=True)
    
    
class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    

class UserResponse(UserRequest):
    id: int
    
    model_config = ConfigDict(from_attributes=True)