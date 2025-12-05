import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

# ------------------------------
# 🎨 Modern Page Styling
# ------------------------------
st.set_page_config(
    page_title="Heart Disease Risk Predictor",
    page_icon="❤️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .title {
        text-align: center;
        color: #D61C4E;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: -10px;
    }
    .subtitle {
        text-align: center;
        color: #4a4a4a;
        font-size: 18px;
    }
    .stButton>button {
        border-radius: 10px;
        height: 50px;
        font-size: 18px;
        background-color: #D61C4E;
        color: white;
    }
    .stButton>button:hover {
        background-color: #b3133d;
        color: white;
    }
    .section {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# TITLE
# ------------------------------
st.markdown("<h1 class='title'>❤️ Heart Disease Risk Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Predict your 10-year risk using medical parameters</p>", unsafe_allow_html=True)
st.write("")

st.sidebar.title("🔧 Input Controls")
st.sidebar.info("Fill the form to calculate your 10-year heart disease risk.")

# ------------------------------
# INPUT FORM UI
# ------------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🧍‍♂️ Personal & Lifestyle Information")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", [0, 1], help="0 = Female, 1 = Male")
    age = st.number_input("Age", 1, 120, 50)

with col2:
    currentSmoker = st.selectbox("Current Smoker", [0, 1])
    cigsPerDay = st.number_input("Cigarettes per day", 0, 50, 0)

with col3:
    diabetes = st.selectbox("Diabetes", [0, 1])
    BPMeds = st.selectbox("On BP Medication (BPMeds)", [0, 1])

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🩺 Medical Measurements")

col4, col5, col6 = st.columns(3)

with col4:
    totChol = st.number_input("Total Cholesterol", 100, 600, 200)
    sysBP = st.number_input("Systolic BP", 50, 250, 120)

with col5:
    diaBP = st.number_input("Diastolic BP", 30, 150, 80)
    heartRate = st.number_input("Heart Rate", 30, 200, 70)

with col6:
    glucose = st.number_input("Glucose Level", 40, 300, 90)
    prevalentStroke = st.selectbox("Prevalent Stroke", [0, 1])
    prevalentHyp = st.selectbox("Hypertension", [0, 1])

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("⚖️ Body Measurements (BMI Auto-Calculated)")

col7, col8 = st.columns(2)

with col7:
    weight = st.number_input("Weight (kg)", 20.0, 200.0, 70.0)

with col8:
    height = st.number_input("Height (meters)", 1.0, 2.5, 1.70)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# BMI CALCULATION
# ------------------------------
BMI = round(weight / (height ** 2), 2)

st.info(f"📌 Calculated BMI: **{BMI}**")

# ------------------------------
# PREDICT BUTTON
# ------------------------------
predict_btn = st.button("🔮 Predict Risk")

# ------------------------------
# API CALL
# ------------------------------
if predict_btn:
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
        "BMI": BMI,
        "heartRate": heartRate,
        "glucose": glucose,
    }

    try:
        response = requests.post(API_URL, json=data).json()

        pred = response["prediction"]
        prob = response["probability"] * 100

        st.success("Prediction Successful!")

        colA, colB = st.columns(2)

        with colA:
            st.metric(
                label="🩺 CHD Prediction (0=No, 1=Yes)",
                value=str(pred)
            )

        with colB:
            st.metric(
                label="📊 Risk Probability (%)",
                value=f"{prob:.2f} %"
            )

        if pred == 1:
            st.warning("⚠️ High Risk: Please consult a cardiologist.")
        else:
            st.info("✅ Low Risk: Maintain healthy lifestyle!")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
