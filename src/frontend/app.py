import requests
import streamlit as st

st.set_page_config(page_title="Trip Time Predictor", page_icon="🚲")

st.title("EcoMute Trip Time Predictor")

distance = st.slider(
    "Distance (km)", min_value=1.0, max_value=20.0, value=5.0, step=0.5
)
battery = st.slider("Battery Level (%)", min_value=0, max_value=100, value=80, step=1)

api_url = st.text_input("FastAPI URL", value="http://127.0.0.1:8000/predict/")

if st.button("Estimate trip time"):
    try:
        response = requests.post(
            api_url,
            json={"distance_km": distance, "battery_level": battery},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        st.metric("Estimated Minutes", data["estimated_minutes"])
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
