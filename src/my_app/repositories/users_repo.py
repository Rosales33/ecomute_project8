from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence

from src.my_app.db.db_models import User


async def list_users(db: AsyncSession) -> Sequence[User]:
    result = await db.execute(select(User).order_by(User.id))
    return result.scalars().all()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    user = await db.scalar(select(User).where(User.username == username))
    return cast(User | None, user)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    user = await db.scalar(select(User).where(User.email == email))
    return cast(User | None, user)


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    user = await db.scalar(select(User).where(User.id == user_id))
    return cast(User | None, user)


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    hashed_password: str,
    role: str = "rider",
) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, data: dict) -> User | None:
    user = await get_user(db, user_id)
    if not user:
        return None
    for k, v in data.items():
        setattr(user, k, v)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await get_user(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
