import streamlit as st
import pickle
import os
import numpy as np
import pandas as pd

# --- Adjust these to match your training feature names and order ---
FEATURE_NAMES = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]

MODEL_PATH = "model.pkl"
SCALER_PATHS = ["scaler.pkl","preprocessor.pkl"]  # common names we try to load

def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        st.error(f"Model file not found: {path}")
        raise FileNotFoundError(path)
    with open(path,"rb") as f:
        return pickle.load(f)

def load_scaler():
    for p in SCALER_PATHS:
        if os.path.exists(p):
            with open(p,"rb") as f:
                return pickle.load(f)
    return None

def predict(features_list):
    """
    features_list: list or 1D array of length len(FEATURE_NAMES)
    returns dict with label, proba (if available).
    """
    # validate length
    if len(features_list) != len(FEATURE_NAMES):
        raise ValueError(f"Expected {len(FEATURE_NAMES)} features in order {FEATURE_NAMES}, got {len(features_list)}")

    # create DataFrame with column names so model sees correct feature names
    X = pd.DataFrame([features_list], columns=FEATURE_NAMES, dtype=float)

    # load model
    model = load_model()

    # load and apply scaler/preprocessor if present
    scaler = load_scaler()
    if scaler is not None:
        try:
            X_trans = scaler.transform(X)
        except Exception:
            # if the scaler is a ColumnTransformer or expects DataFrame, try passing DataFrame
            X_trans = scaler.transform(X)
        # X_trans may be numpy array
        X_for_model = X_trans
    else:
        # no scaler saved — use the DataFrame (model may accept df or numpy)
        X_for_model = X

    # get prediction
    try:
        pred = model.predict(X_for_model)
    except Exception as e:
        # Last attempt: if model was trained with DataFrame feature names, pass the DataFrame
        try:
            pred = model.predict(X)
        except Exception:
            raise

    label = int(pred[0])
    result_text = "Diabetes" if label == 1 else "No Diabetes"

    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_for_model)
            # probability of positive class (class 1)
            positive_proba = float(proba[0][:,].flatten()[-1]) if proba is not None else None
        except Exception:
            # try with original DataFrame
            try:
                proba = model.predict_proba(X)
                positive_proba = float(proba[0][:,].flatten()[-1])
            except Exception:
                positive_proba = None
    else:
        positive_proba = None

    return {"label": label, "text": result_text, "proba": positive_proba, "features_df": X}

# --- Streamlit UI example: adapt to your existing page layout ---
def predict_page():
    st.header("Diabetes Prediction (fixed input handling)")

    # Inputs: adapt these inputs to your UI
    pregnancies = st.number_input("Pregnancies", value=0, step=1)
    glucose = st.number_input("Glucose", value=0.0)
    bp = st.number_input("Blood Pressure (diastolic)", value=0.0)
    skt = st.number_input("Skin Thickness", value=0.0)
    insulin = st.number_input("Insulin", value=0.0)
    bmi = st.number_input("BMI", value=0.0, format="%.2f")
    dpf = st.number_input("DiabetesPedigreeFunction", value=0.0, format="%.3f")
    age = st.number_input("Age", value=0, step=1)

    if st.button("Predict"):
        try:
            features = [pregnancies, glucose, bp, skt, insulin, bmi, dpf, age]
            res = predict(features)
            st.write("Prediction:", res["text"])
            if res["proba"] is not None:
                st.write(f"Probability of diabetes: {res['proba']*100:.1f}%")
            st.write("Input features sent to model:")
            st.dataframe(res["features_df"])
        except Exception as e:
            st.error(f"Prediction error: {e}")

if __name__ == "__main__":
    predict_page()
