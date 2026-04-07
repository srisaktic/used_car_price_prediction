
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import numpy as np
import pandas as pd
from pathlib import Path
import joblib
import os


# ---------- Load artifacts (must exist in the same folder) ----------

BASE_DIR  = Path(__file__).resolve().parent           # .../app_folder
MODEL_DIR = BASE_DIR / "models"                       # .../app_folder/models

xgb_model = joblib.load(MODEL_DIR / "xgb_model.pkl")
scaler    = joblib.load(MODEL_DIR / "scaler.pkl")
te        = joblib.load(MODEL_DIR / "target_encoder.pkl")
ohe       = joblib.load(MODEL_DIR / "onehot_encoder.pkl")

# ---------- Columns (must match training) ----------
categorical_high = ["model"]                      # Target Encoding
categorical_low  = ["transmission", "fuelType"]  # One-Hot Encoding
numerical = [
    "year","mileage","tax","mpg","engineSize",
    "age","eng_age","mpg_eng","mpg_age","mileage_per_year","tax_per_engine"
]

# If you grouped rare models as 'Rare' during training, keep that convention at inference:
RARE_LABEL = "Rare"   # if a model wasn’t seen in training, TE will use the global prior; OHE ignores unknowns.

# ---------- Request schema ----------
class CarFeatures(BaseModel):
    model: str
    year: int
    transmission: str     # e.g., "Automatic", "Manual", "Semi-Auto"
    mileage: int
    fuelType: str         # e.g., "Diesel", "Petrol", "Hybrid"
    tax: int
    mpg: float
    engineSize: float

    @field_validator("year")
    @classmethod
    def year_range(cls, v):
        if v < 1990 or v > 2025:
            raise ValueError("year out of range [1990, 2025]")
        return v

    @field_validator("mileage")
    @classmethod
    def mileage_nonneg(cls, v):
        if v < 0: raise ValueError("mileage must be >= 0")
        return v

    @field_validator("mpg")
    @classmethod
    def mpg_reasonable(cls, v):
        if v < 5 or v > 100:
            raise ValueError("mpg should be within [5, 100] for non-EV data")
        return v

    @field_validator("engineSize")
    @classmethod
    def engine_reasonable(cls, v):
        if v < 1.0 or v > 6.6:
            raise ValueError("engineSize should be within [1.0, 6.6]")
        return v

app = FastAPI(title="BMW Price Predictor", version="1.0.0")

# ---------- Health ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- Preprocess exactly like training ----------
def preprocess_one(record: dict) -> np.ndarray:
    """
    record keys MUST include:
    ['model','year','transmission','mileage','fuelType','tax','mpg','engineSize']
    """
    df = pd.DataFrame([record])

    # Normalize/strip model text just in case
    df["model"] = df["model"].astype(str).str.strip()

    # === Feature engineering (must match training) ===
    df["age"] = 2025 - df["year"]
    df["age"] = df["age"].replace(0, 1)
    df["eng_age"] = df["engineSize"] / df["age"]
    df["mpg_eng"] = df["mpg"] / df["engineSize"]
    df["mpg_age"] = df["mpg"] / df["age"]
    df["mileage_per_year"] = df["mileage"] / df["age"]
    df["tax_per_engine"] = df["tax"] / df["engineSize"]

    # Guard against inf/nan
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    # If during training you grouped very rare models to 'Rare', you can optionally map here.
    # We don't have the exact rare model list at inference; TargetEncoder will fall back to prior for unseen categories.
    # If you WANT to force unknown models to a bucket, uncomment below:
    # known_models = set(te.mapping[0]['col'].tolist()) if hasattr(te, 'mapping') else None
    # if known_models is not None:
    #     df.loc[~df['model'].isin(known_models), 'model'] = RARE_LABEL

    # ---- Transform with train-fitted encoders/scaler (DO NOT fit here) ----
    X_num = scaler.transform(df[numerical])
    X_te  = te.transform(df[categorical_high])     # unseen models get prior smoothing
    X_ohe = ohe.transform(df[categorical_low])     # unknown categories ignored -> all zeros

    # Final order: numerics, TE(model), OHE(low)
    X_pre = np.hstack([X_num, X_te, X_ohe])
    return X_pre

# ---------- Predict ----------
@app.post("/bmw_predict_price")
def predict(features: CarFeatures):
    try:
        X = preprocess_one(features.model_dump())
        pred = float(xgb_model.predict(X)[0])
        return {"predicted_price": round(pred, 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {e}")
    

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    # If docs are enabled, go there; otherwise go to /health
    return RedirectResponse(url=app.docs_url or "/health")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later to your Streamlit domain
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)