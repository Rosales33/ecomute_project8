from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

BikeStatus = Literal["available", "rented", "maintenance"]


class BikeBase(BaseModel):
    """Base schema for Bike with common fields"""

    model: str
    battery: int = Field(
        ..., ge=0, le=100, description="Battery level percentage (0-100)"
    )  # Validation for battery level
    status: Literal["available", "rented", "maintenance"]
    station_id: Optional[int] = None


class BikeCreate(BikeBase):
    """Schema for creating a new bike"""

    pass


class BikeUpdate(BaseModel):
    model: str | None = None
    battery: int | None = Field(default=None, ge=0, le=100)
    status: BikeStatus | None = None


class BikeResponse(BikeBase):
    """Schema for bike response with ID"""

    id: int
    model_config = ConfigDict(from_attributes=True)  # Allow parsing from ORM objects
