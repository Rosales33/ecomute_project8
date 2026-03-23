from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from src.my_app.logger import logger
from src.my_app.schemas.predictions import TripInput, TripPredictionResponse

router = APIRouter(prefix="/predict", tags=["predictions"])

MODEL_PATH = Path(__file__).resolve().parents[2] / "ml" / "trip_predictor.joblib"
model = None


def load_model(): # This function loads the trained machine learning model from disk. It uses a global variable to cache the loaded model so that it is only loaded once during the application's lifetime. If the model file is not found, it logs an error and raises a FileNotFoundError.
    global model
    if model is None:
        if not MODEL_PATH.exists():
            logger.error("Prediction model file not found at %s", MODEL_PATH) # Log an error if the model file is missing
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        logger.info("Loading prediction model from %s", MODEL_PATH) # Log an info message when the model is being loaded
        model = joblib.load(MODEL_PATH)
    return model


@router.post("/", response_model=TripPredictionResponse)
async def predict_trip_time(payload: TripInput):
    logger.info(
        "Prediction requested: distance_km=%s battery_level=%s",
        payload.distance_km,
        payload.battery_level,
    )
    try:
        loaded_model = load_model()
    except FileNotFoundError as exc:
        logger.error("Prediction failed: model unavailable")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    features = pd.DataFrame(
        [
            {
                "distance_km": payload.distance_km,
                "battery_level": payload.battery_level,
            }
        ]
    )

    try:
        prediction = loaded_model.predict(features)[0] # The predict method of the loaded model is called with the input features to generate a prediction. The [0] is used to extract the single predicted value from the array returned by the predict method, since we are only making one prediction at a time.
    except Exception as exc:
        logger.error("Prediction inference failed: %s", exc)
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    estimated_minutes = round(max(0.0, float(prediction)), 2)
    logger.info("Prediction completed: estimated_minutes=%s", estimated_minutes)

    return TripPredictionResponse(estimated_minutes=estimated_minutes)
