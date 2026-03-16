from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.repositories import stations_repo
from src.my_app.schemas.stations import StationCreate, StationResponse
from src.my_app.dependencies.auth import require_admin

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/", response_model=list[StationResponse])
async def list_stations(db: AsyncSession = Depends(get_db)):
    return await stations_repo.list_stations(db)


@router.post("/", response_model=StationResponse, status_code=201)
async def create_station(
    payload: StationCreate,
    db: AsyncSession = Depends(get_db),
    _admin=Depends(require_admin),  # only admin can pass
):
    return await stations_repo.create_station(db, payload.name)
