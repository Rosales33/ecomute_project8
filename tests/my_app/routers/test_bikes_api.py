import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.db_models import Bike


@pytest.mark.asyncio
async def test_get_bikes_empty(client):
    resp = await client.get("/bikes/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_bikes_returns_one_bike(client, test_db_session: AsyncSession):
    bike = Bike(model="Test Bike", battery=80, status="available", station_id=None)
    test_db_session.add(bike)
    await test_db_session.commit()
    await test_db_session.refresh(bike)

    resp = await client.get("/bikes/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["model"] == "Test Bike"
