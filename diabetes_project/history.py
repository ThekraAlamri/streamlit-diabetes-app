import streamlit as st
import sqlite3
import pandas as pd


def history():
    """Prediction history page"""
    st.title("📈 Prediction History")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please login first to view history.")
        return

    conn = sqlite3.connect('db/diabetes_app.db')
    c = conn.cursor()

    try:
        c.execute('''
            SELECT pregnancies, glucose, blood_pressure, skin_thickness, insulin, 
                   bmi, dpf, age, prediction, probability, date 
            FROM predictions 
            WHERE username=? 
            ORDER BY date DESC
        ''', (st.session_state["username"],))

        rows = c.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=[
                "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
                "Insulin", "BMI", "DPF", "Age", "Prediction", "Probability", "Date"
            ])

            # Format prediction column
            df["Prediction"] = df["Prediction"].map({0: "Low Risk", 1: "High Risk"})
            df["Probability"] = df["Probability"].round(1).astype(str) + "%"

            st.dataframe(df, use_container_width=True)

            # Summary statistics
            st.subheader("Summary")
            total_predictions = len(df)
            high_risk_count = sum(df["Prediction"] == "High Risk")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Predictions", total_predictions)
            with col2:
                st.metric("High Risk Predictions", high_risk_count)
            with col3:
                st.metric("Low Risk Predictions", total_predictions - high_risk_count)

        else:
            st.info("No prediction history found. Make your first prediction!")

    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()