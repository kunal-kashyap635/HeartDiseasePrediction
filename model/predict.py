# model/predict.py
import pickle
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "heart_disease_model.pkl")

# Load model once at import time
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_chd(patient_dict: dict):
    """
    Convert patient dict → DataFrame → model.predict
    """
    df = pd.DataFrame([patient_dict])
    
    proba = model.predict_proba(df)[0][1]
    pred = int(proba >= 0.5)

    return {"prediction": pred, "probability": float(proba)}
