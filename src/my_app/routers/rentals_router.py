from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.repositories import rentals_repo, bikes_repo, users_repo
from src.my_app.schemas.rentals import (
    RentalCreate,
    RentalUpdate,
    RentalRead,
    RentalOutcome,
)
from src.my_app.services.rentals_service import create_rental_with_checks

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.get("/", response_model=list[RentalRead])
async def list_rentals(db: AsyncSession = Depends(get_db)):
    return await rentals_repo.list_rentals(db)


@router.get("/{rental_id}", response_model=RentalRead)
async def get_rental(rental_id: int, db: AsyncSession = Depends(get_db)):
    rental = await rentals_repo.get_rental(db, rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.post("/", response_model=RentalOutcome, status_code=201)
async def create_rental(payload: RentalCreate, db: AsyncSession = Depends(get_db)):
    rental, bike = await create_rental_with_checks(
        db, user_id=payload.user_id, bike_id=payload.bike_id
    )

    return RentalOutcome(
        user_id=payload.user_id,
        bike_id=payload.bike_id,
        bike_battery=int(bike.battery),
        message="Rental approved",
    )


@router.put("/{rental_id}", response_model=RentalRead)
async def update_rental(
    rental_id: int, payload: RentalUpdate, db: AsyncSession = Depends(get_db)
):
    # validate if user/bike exists when changing them
    data = payload.model_dump(exclude_unset=True)

    if "user_id" in data:
        user = await users_repo.get_user(db, data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    if "bike_id" in data:
        bike = await bikes_repo.get_bike(db, data["bike_id"])
        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

    updated = await rentals_repo.update_rental(db, rental_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated


@router.delete("/{rental_id}", status_code=204)
async def delete_rental(rental_id: int, db: AsyncSession = Depends(get_db)):
    ok = await rentals_repo.delete_rental(db, rental_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rental not found")
    return None
