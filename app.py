import streamlit as st
import numpy as np
import joblib

model = joblib.load('hypertension_model.pkl')

st.title("Hypertension Risk Prediction App")

st.markdown("Please provide the following information to assess your hypertension risk.")

st.sidebar.header("BMI Calculator")

weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=60.0)
height_cm = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)

height_m = height_cm / 100
bmi_value = round(weight / (height_m ** 2), 1)

st.sidebar.write(f"**Your BMI:** {bmi_value}")

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight 🟡"
    elif 18.5 <= bmi < 25:
        return "Normal ✅"
    elif 25 <= bmi < 30:
        return "Overweight 🟠"
    else:
        return "Obese 🔴"

st.sidebar.write(f"**Category:** {bmi_category(bmi_value)}")


age = st.slider("Age", 10, 100, 25)
bmi = bmi_value
salt = st.slider("Salt Intake", 0.0, 20.0, 10.0)
stress = st.slider("Stress Level", 1.0, 10.0, 5.0)
sleep = st.slider("Sleep Duration per day", 1.0, 12.0, 6.0)

bp_hist = st.selectbox("Blood Pressure History", ['Normal', 'Hypertension', 'Prehypertension'])
medication = st.selectbox("Medication", ['None', 'ACE Inhibitor', 'Beta Blocker', 'Diuretic', 'Other'])
family_hist = st.selectbox("Family History of Hypertension", ['No', 'Yes'])
exercise = st.selectbox("Exercise Level", ['Low', 'Moderate', 'High'])
smoking = st.selectbox("Smoking Status", ['Non-Smoker', 'Smoker'])

bp_hist_map = {'Normal':0, 'Hypertension':1, 'Prehypertension':2}
med_map = {'None':0, 'ACE Inhibitor':1, 'Beta Blocker':2, 'Diuretic':3, 'Other':4}
fam_map = {'No':0, 'Yes':1}
ex_map = {'Low':0, 'Moderate':1, 'High':2}
smoke_map = {'Non-Smoker':0, 'Smoker':1}

features = np.array([[age, bmi, salt, stress, sleep,
                      bp_hist_map[bp_hist],
                      med_map[medication],
                      fam_map[family_hist],
                      ex_map[exercise],
                      smoke_map[smoking]]])

if st.button("Predict"):
    result = model.predict(features)[0]
    if result == 1:
        st.error("⚠️ Hypertension is present. Please consult a medical professional.")
    else:
        st.success("✅ No Hypertension detected.")
