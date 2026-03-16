from pydantic import BaseModel, ConfigDict


class StationCreate(BaseModel):
    name: str


class StationResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
