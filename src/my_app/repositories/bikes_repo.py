from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence

from src.my_app.db.db_models import Bike


async def list_bikes(db: AsyncSession, status: str | None = None) -> Sequence[Bike]:
    stmt = select(Bike).order_by(Bike.id)
    if status:
        stmt = stmt.where(Bike.status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_bike(db: AsyncSession, bike_id: int) -> Bike | None:
    bike = await db.scalar(select(Bike).where(Bike.id == bike_id))
    return cast(Bike | None, bike)


async def create_bike(db: AsyncSession, data: dict) -> Bike:
    bike = Bike(**data)
    db.add(bike)
    await db.commit()
    await db.refresh(bike)
    return bike


async def update_bike(db: AsyncSession, bike_id: int, data: dict) -> Bike | None:
    bike = await get_bike(db, bike_id)
    if not bike:
        return None
    for k, v in data.items():
        setattr(bike, k, v)
    await db.commit()
    await db.refresh(bike)
    return bike


async def delete_bike(db: AsyncSession, bike_id: int) -> bool:
    bike = await get_bike(db, bike_id)
    if not bike:
        return False
    await db.delete(bike)
    await db.commit()
    return True
