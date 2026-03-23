from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.logger import logger
from src.my_app.repositories import bikes_repo
from src.my_app.schemas.bikes import BikeCreate, BikeUpdate, BikeResponse

router = APIRouter(prefix="/bikes", tags=["bikes"])


@router.get("/", response_model=list[BikeResponse])
async def get_bikes(
    status: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db), # Endpoint dependency injection: get_db is a function that provides a database session. By using Depends(get_db), FastAPI will automatically call get_db to get a database session and pass it to the route handler. This allows us to easily access the database within our route without having to manually create a session each time.
):
    logger.info("Fetching all bikes")
    bikes = await bikes_repo.list_bikes(db, status=status)
    if not bikes:
        logger.warning("No bikes found")
    return bikes


@router.get("/{bike_id}", response_model=BikeResponse)
async def get_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    bike = await bikes_repo.get_bike(db, bike_id)
    if not bike:
        logger.warning("Bike not found: bike_id=%s", bike_id)
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike


@router.post("/", response_model=BikeResponse, status_code=201) # The status_code=201 indicates that a new resource has been successfully created. This is a standard HTTP response code for successful POST requests that result in the creation of a new resource.
async def create_bike(payload: BikeCreate, db: AsyncSession = Depends(get_db)):
    logger.info("Creating new bike: %s", payload.model)
    return await bikes_repo.create_bike(db, payload.model_dump()) # payload.model_dump() is used to convert the Pydantic model instance into a dictionary that can be easily stored in the database. This allows us to create a new bike entry in the database using the provided data.


@router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(
    bike_id: int, payload: BikeUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await bikes_repo.update_bike(
        db, bike_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        logger.warning("Bike update failed: bike_id=%s", bike_id)
        raise HTTPException(status_code=404, detail="Bike not found")
    logger.info("Bike updated: bike_id=%s", bike_id)
    return updated


@router.delete("/{bike_id}", status_code=204) # The status_code=204 indicates that the request was successful but there is no content to return. This is a standard HTTP response code for successful DELETE requests.
async def delete_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    ok = await bikes_repo.delete_bike(db, bike_id)
    if not ok:
        logger.warning("Bike delete failed: bike_id=%s", bike_id)
        raise HTTPException(status_code=404, detail="Bike not found")
    logger.info("Bike deleted: bike_id=%s", bike_id)
    return None
