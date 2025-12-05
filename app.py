from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema.patient_schema import Patient
from model.predict import predict_chd

app = FastAPI(title="Heart Disease Prediction API")

# Allow Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "Message": "Heart Disease Prediction",
        "status": "running",
    }

@app.get("/health")
def health():
    return {"Author": "Kunal kashyap", "Version": "1.0.0"}

@app.post("/predict")
def predict(patient: Patient):
    result = predict_chd(patient.dict())
    return result
