from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.repositories import bikes_repo
from src.my_app.schemas.bikes import BikeCreate, BikeUpdate, BikeResponse

router = APIRouter(prefix="/bikes", tags=["bikes"])


@router.get("/", response_model=list[BikeResponse])
async def get_bikes(
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await bikes_repo.list_bikes(db, status=status)


@router.get("/{bike_id}", response_model=BikeResponse)
async def get_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    bike = await bikes_repo.get_bike(db, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike


@router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike(payload: BikeCreate, db: AsyncSession = Depends(get_db)):
    return await bikes_repo.create_bike(db, payload.model_dump())


@router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(
    bike_id: int, payload: BikeUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await bikes_repo.update_bike(
        db, bike_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Bike not found")
    return updated


@router.delete("/{bike_id}", status_code=204)
async def delete_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    ok = await bikes_repo.delete_bike(db, bike_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Bike not found")
    return None
