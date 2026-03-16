from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.db_models import Station


async def create_station(db: AsyncSession, name: str) -> Station:
    station = Station(name=name)
    db.add(station)
    await db.commit()
    await db.refresh(station)
    return station


async def list_stations(db: AsyncSession) -> list[Station]:
    result = await db.execute(select(Station).order_by(Station.id))
    return list(result.scalars().all())
