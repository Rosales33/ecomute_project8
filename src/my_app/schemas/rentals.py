from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from datetime import datetime
from typing import Optional


# Pydantic models for rentals domain
class RentalOutcome(BaseModel):
    user_id: int
    bike_id: int
    bike_battery: int
    message: str = "Rental approved"

    @field_validator(
        "bike_battery"
    )  # field_validator es para validar un campo específico, model_validator es para validar todo el modelo
    @classmethod
    def battery_must_be_enough(cls, v: int) -> int:
        if v < 20:
            raise ValueError("Bike battery too low for rental.")
        return v


class RentalProcessing(BaseModel):
    bike_battery: int
    user_id: int

    @model_validator(mode="after") # model_validator permite realizar validaciones que dependen de múltiples campos o del estado completo del modelo. En este caso, ya que tenemos el field_validator en RentalOutcome, no es estrictamente necesario tener esta validación aquí también.
    def check_battery(self):
        if self.bike_battery < 20:
            raise ValueError("Bike battery too low for rental.")
        return self


# CRUD Schemas
class RentalCreate(BaseModel):
    user_id: int
    bike_id: int


class RentalUpdate(BaseModel):
    # allow changing user/bike (optional)
    user_id: Optional[int] = None
    bike_id: Optional[int] = None


class RentalRead(BaseModel):
    id: int
    user_id: Optional[int]
    bike_id: Optional[int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
