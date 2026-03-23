from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.db_models import Bike, User
from src.my_app.repositories import bikes_repo, users_repo, rentals_repo
from src.my_app.schemas.rentals import RentalProcessing


async def create_rental_with_checks(db: AsyncSession, user_id: int, bike_id: int):
    user: User | None = await users_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bike: Bike | None = await bikes_repo.get_bike(db, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    try:
        RentalProcessing(bike_battery=int(bike.battery), user_id=user_id) # Aquí es donde se realiza la validación de la batería. Si la batería es menor a 20, se lanzará una excepción y se devolverá un error 422 al cliente.
    except ValidationError:
        raise HTTPException(status_code=422, detail="Bike battery too low for rental.")

    rental = await rentals_repo.create_rental(db, user_id=user_id, bike_id=bike_id)
    return rental, bike
