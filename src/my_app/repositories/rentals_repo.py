from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence

from src.my_app.db.db_models import Rental


async def list_rentals(db: AsyncSession) -> Sequence[Rental]:
    result = await db.execute(select(Rental).order_by(Rental.id))
    return result.scalars().all()


async def get_rental(db: AsyncSession, rental_id: int) -> Rental | None:
    rental = await db.scalar(select(Rental).where(Rental.id == rental_id))
    return cast(Rental | None, rental)


async def create_rental(db: AsyncSession, user_id: int, bike_id: int) -> Rental:
    rental = Rental(user_id=user_id, bike_id=bike_id)
    db.add(rental)
    await db.commit()
    await db.refresh(rental)
    return rental


async def update_rental(db: AsyncSession, rental_id: int, data: dict) -> Rental | None:
    rental = await get_rental(db, rental_id)
    if not rental:
        return None
    for k, v in data.items():
        setattr(rental, k, v)
    await db.commit()
    await db.refresh(rental)
    return rental


async def delete_rental(db: AsyncSession, rental_id: int) -> bool:
    rental = await get_rental(db, rental_id)
    if not rental:
        return False
    await db.delete(rental)
    await db.commit()
    return True
