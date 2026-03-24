from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.logger import logger
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
    logger.info("Fetching all rentals")
    rentals = await rentals_repo.list_rentals(db)
    if not rentals:
        logger.warning("No rentals found")
    return rentals


@router.get("/{rental_id}", response_model=RentalRead)
async def get_rental(rental_id: int, db: AsyncSession = Depends(get_db)): #, current_user = Depends(get_current_user) para validar que el usuario autenticado solo pueda acceder a sus propios alquileres, o que un admin pueda acceder a todos los alquileres.
    rental = await rentals_repo.get_rental(db, rental_id)
    if not rental:
        logger.warning("Rental not found: rental_id=%s", rental_id)
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.post("/", response_model=RentalOutcome, status_code=201)
async def create_rental(payload: RentalCreate, db: AsyncSession = Depends(get_db)):
    logger.info(
        "Creating rental request: user_id=%s bike_id=%s",
        payload.user_id,
        payload.bike_id,
    )
    rental, bike = await create_rental_with_checks( # Delegamos la lógica de creación y validación del alquiler a un servicio separado para mantener el router limpio y enfocado en la gestión de las rutas y respuestas HTTP.
        db, user_id=payload.user_id, bike_id=payload.bike_id
    )
    logger.info(
        "Rental approved: rental_id=%s user_id=%s bike_id=%s",
        rental.id,
        payload.user_id,
        payload.bike_id,
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
            logger.warning(
                "Rental update failed: user not found for rental_id=%s user_id=%s",
                rental_id,
                data["user_id"],
            )
            raise HTTPException(status_code=404, detail="User not found")

    if "bike_id" in data:
        bike = await bikes_repo.get_bike(db, data["bike_id"])
        if not bike:
            logger.warning(
                "Rental update failed: bike not found for rental_id=%s bike_id=%s",
                rental_id,
                data["bike_id"],
            )
            raise HTTPException(status_code=404, detail="Bike not found")

    updated = await rentals_repo.update_rental(db, rental_id, data)
    if not updated:
        logger.warning("Rental update failed: rental_id=%s", rental_id)
        raise HTTPException(status_code=404, detail="Rental not found")
    logger.info("Rental updated: rental_id=%s", rental_id)
    return updated


@router.delete("/{rental_id}", status_code=204)
async def delete_rental(rental_id: int, db: AsyncSession = Depends(get_db)):
    ok = await rentals_repo.delete_rental(db, rental_id)
    if not ok:
        logger.warning("Rental delete failed: rental_id=%s", rental_id)
        raise HTTPException(status_code=404, detail="Rental not found")
    logger.info("Rental deleted: rental_id=%s", rental_id)
    return None
