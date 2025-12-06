from pydantic import BaseModel, Field

class Patient(BaseModel):
    
    gender: int = Field(..., ge=0, le=1)
    age: int
    currentSmoker: int = Field(..., ge=0, le=1)
    cigsPerDay: float = 0.0
    BPMeds: int = Field(..., ge=0, le=1)
    prevalentStroke: int = Field(..., ge=0, le=1)
    prevalentHyp: int = Field(..., ge=0, le=1)
    diabetes: int = Field(..., ge=0, le=1)
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    heartRate: float
    glucose: float
    