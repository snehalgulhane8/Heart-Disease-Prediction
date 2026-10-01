import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "heart_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "model",
    "scaler.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "model",
    "features.pkl"
)


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
features = joblib.load(FEATURE_PATH)


def predict_heart_disease(data: dict):

    input_df = pd.DataFrame([data])

    # Convert categorical data
    input_df = pd.get_dummies(
        input_df,
        drop_first=True
    )

    # Match training features
    input_df = input_df.reindex(
        columns=features,
        fill_value=0
    )

    # Scale
    input_scaled = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # Probability
    probability = model.predict_proba(input_scaled)[0]

    probability_percent = max(probability) * 100

    if prediction == 1:
        result = "Higher Risk"
    else:
        result = "Lower Risk"

    return {
        "prediction": int(prediction),
        "result": result,
        "probability": round(probability_percent, 2)
    }