from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from src.my_app.schemas.predictions import TripInput, TripPredictionResponse

router = APIRouter(prefix="/predict", tags=["predictions"])

MODEL_PATH = Path(__file__).resolve().parents[2] / "ml" / "trip_predictor.joblib"
model = None


def load_model():
    global model
    if model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
    return model


@router.post("/", response_model=TripPredictionResponse)
async def predict_trip_time(payload: TripInput):
    try:
        loaded_model = load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    features = pd.DataFrame(
        [
            {
                "distance_km": payload.distance_km,
                "battery_level": payload.battery_level,
            }
        ]
    )

    prediction = loaded_model.predict(features)[0]
    estimated_minutes = round(max(0.0, float(prediction)), 2)

    return TripPredictionResponse(estimated_minutes=estimated_minutes)
