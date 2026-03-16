from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


def build_fake_dataset() -> pd.DataFrame:
    data = [
        {"distance_km": 1, "battery_level": 100, "minutes": 4},
        {"distance_km": 2, "battery_level": 95, "minutes": 7},
        {"distance_km": 3, "battery_level": 90, "minutes": 10},
        {"distance_km": 5, "battery_level": 85, "minutes": 16},
        {"distance_km": 7, "battery_level": 80, "minutes": 22},
        {"distance_km": 10, "battery_level": 75, "minutes": 30},
        {"distance_km": 12, "battery_level": 70, "minutes": 36},
        {"distance_km": 15, "battery_level": 65, "minutes": 45},
        {"distance_km": 4, "battery_level": 50, "minutes": 14},
        {"distance_km": 8, "battery_level": 40, "minutes": 27},
        {"distance_km": 6, "battery_level": 30, "minutes": 21},
        {"distance_km": 9, "battery_level": 20, "minutes": 34},
    ]
    return pd.DataFrame(data)


def train_and_save_model() -> Path:
    df = build_fake_dataset()

    x = df[["distance_km", "battery_level"]]
    y = df["minutes"]

    model = LinearRegression()
    model.fit(x, y)

    output_path = Path(__file__).resolve().parent / "trip_predictor.joblib"
    joblib.dump(model, output_path)
    return output_path


if __name__ == "__main__":
    model_path = train_and_save_model()
    print(f"Model saved to: {model_path}")
