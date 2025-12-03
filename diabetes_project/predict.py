import streamlit as st
import joblib
import numpy as np

st.title("🩺 Predict Diabetes")

st.write("Please enter the following details:")

# Input fields
pregnancies = st.number_input("Pregnancies", min_value=0)
glucose = st.number_input("Glucose", min_value=0)
blood_pressure = st.number_input("Blood Pressure", min_value=0)
skin_thickness = st.number_input("Skin Thickness", min_value=0)
insulin = st.number_input("Insulin", min_value=0)
bmi = st.number_input("BMI", min_value=0.0, format="%.2f")
dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.3f")
age = st.number_input("Age", min_value=0)

if st.button("Predict"):
    try:
        # Load the trained model
        model = joblib.load("model.pkl")

        # Make prediction
        features = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        prediction = model.predict(features)[0]

        if prediction == 1:
            st.error("🚨 The model predicts that this person **has diabetes**.")
        else:
            st.success("✅ The model predicts that this person **does NOT have diabetes**.")
    except Exception as e:
        st.error(f"Model loading failed: {e}")
