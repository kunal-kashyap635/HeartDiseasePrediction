# streamlit_app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("❤️ Heart Disease Prediction")

with st.form("input_form"):
    gender = st.selectbox("Gender", [0, 1])
    age = st.number_input("Age", 1, 120, 50)
    currentSmoker = st.selectbox("Current Smoker", [0, 1])
    cigsPerDay = st.number_input("Cigarettes per day", 0, 50, 0)
    BPMeds = st.selectbox("BP Medication", [0, 1])
    prevalentStroke = st.selectbox("Prevalent Stroke", [0, 1])
    prevalentHyp = st.selectbox("Hypertension", [0, 1])
    diabetes = st.selectbox("Diabetes", [0, 1])

    totChol = st.number_input("Total Cholesterol", 100, 600, 200)
    sysBP = st.number_input("Systolic BP", 50, 250, 120)
    diaBP = st.number_input("Diastolic BP", 30, 150, 80)

    # 👉 You only ask these:
    weight = st.number_input("Weight (kg)", 20.0, 200.0, 70.0)
    height = st.number_input("Height (meters)", 1.0, 2.5, 1.70)

    heartRate = st.number_input("Heart Rate", 30, 200, 70)
    glucose = st.number_input("Glucose", 40, 300, 90)

    submitted = st.form_submit_button("Predict")

if submitted:

    # 👉 BMI Calculated Here
    BMI = round(weight / (height * height), 2)

    data = {
        "gender": gender,
        "age": age,
        "currentSmoker": currentSmoker,
        "cigsPerDay": cigsPerDay,
        "BPMeds": BPMeds,
        "prevalentStroke": prevalentStroke,
        "prevalentHyp": prevalentHyp,
        "diabetes": diabetes,
        "totChol": totChol,
        "sysBP": sysBP,
        "diaBP": diaBP,
        "BMI": BMI,  # ONLY BMI sent
        "heartRate": heartRate,
        "glucose": glucose,
    }

    try:
        response = requests.post(API_URL, json=data).json()
        st.success(f"Prediction: {response['prediction']}")
        st.info(f"Probability: {response['probability']*100:.2f}")
        # st.warning(f"Calculated BMI used: {BMI}")
    except Exception as e:
        st.error(f"Error: {e}")
