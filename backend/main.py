from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.predict import predict_heart_disease


app = FastAPI(
    title="Heart Disease Prediction API",
    description="Machine Learning API for heart disease risk prediction",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Heart Disease Prediction API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(data: dict):

    try:

        result = predict_heart_disease(data)

        return result

    except Exception as e:

        return {
            "error": str(e)
        }