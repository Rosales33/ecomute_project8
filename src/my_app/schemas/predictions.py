from pydantic import BaseModel, Field


class TripInput(BaseModel):
    distance_km: float = Field(..., gt=0)
    battery_level: int = Field(..., ge=0, le=100)


class TripPredictionResponse(BaseModel):
    estimated_minutes: float
