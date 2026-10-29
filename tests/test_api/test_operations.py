from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.models import User, Wallet


async def test_add_expense_succes(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Expense added!"
    assert response.json()["wallet"] == wallet.name
    
    
async def test_add_expense_negative_amount(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -50,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 422
    
    
async def test_add_expense_empty_name(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "   ",
            "amount": 100,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 422
    
    
async def test_add_expense_waller_not_exists(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.commit()
    
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 404
    
    
async def test_add_expense_unauthorized(db_session: AsyncSession, client: AsyncClient):
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer login"})
    
    assert response.status_code == 401
    
    
async def test_add_expense_not_enough_money(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    
    response = await client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 250,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 400
    
    
async def test_add_income_succes(db_session: AsyncSession, client: AsyncClient):
    user = User(login="test")
    db_session.add(user)
    await db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    
    response = await client.post(
        "/api/v1/operations/income",
        json={
            "wallet_name": "card",
            "amount": 50,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {user.login}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Income added!"
    assert response.json()["wallet"] == wallet.name