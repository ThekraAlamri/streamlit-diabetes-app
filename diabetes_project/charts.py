# charts.py
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def charts():
    """Charts and analytics page"""
    st.title("📊 Analytics & Charts")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please login first to view charts.")
        return

    conn = sqlite3.connect('db/diabetes_app.db')
    c = conn.cursor()

    try:
        c.execute('''
            SELECT prediction, probability, glucose, bmi, age, date 
            FROM predictions 
            WHERE username=? 
            ORDER BY date
        ''', (st.session_state["username"],))

        rows = c.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=["Prediction", "Probability", "Glucose", "BMI", "Age", "Date"])
            df["Date"] = pd.to_datetime(df["Date"])
            df["Risk Level"] = df["Prediction"].map({0: "Low Risk", 1: "High Risk"})

            # Risk distribution pie chart
            st.subheader("Risk Distribution")
            fig, ax = plt.subplots(figsize=(8, 6))
            risk_counts = df["Risk Level"].value_counts()
            colors = ['#90EE90', '#FFB6C1']  # Light green for low risk, light red for high risk
            ax.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%', colors=colors)
            ax.set_title("Distribution of Diabetes Risk Predictions")
            st.pyplot(fig)

            # Probability trend over time
            if len(df) > 1:
                st.subheader("Probability Trend Over Time")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df["Date"], df["Probability"], marker='o', linewidth=2, markersize=6)
                ax.set_xlabel("Date")
                ax.set_ylabel("Diabetes Probability (%)")
                ax.set_title("Diabetes Risk Probability Over Time")
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Health metrics correlation
            st.subheader("Health Metrics Analysis")
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

            # Glucose vs Probability
            scatter = ax1.scatter(df["Glucose"], df["Probability"],
                                  c=df["Prediction"], cmap='RdYlGn_r', alpha=0.7)
            ax1.set_xlabel("Glucose Level")
            ax1.set_ylabel("Probability (%)")
            ax1.set_title("Glucose vs Diabetes Probability")

            # BMI vs Probability
            ax2.scatter(df["BMI"], df["Probability"],
                        c=df["Prediction"], cmap='RdYlGn_r', alpha=0.7)
            ax2.set_xlabel("BMI")
            ax2.set_ylabel("Probability (%)")
            ax2.set_title("BMI vs Diabetes Probability")

            # Age vs Probability
            ax3.scatter(df["Age"], df["Probability"],
                        c=df["Prediction"], cmap='RdYlGn_r', alpha=0.7)
            ax3.set_xlabel("Age")
            ax3.set_ylabel("Probability (%)")
            ax3.set_title("Age vs Diabetes Probability")

            # Risk level histogram
            ax4.hist(df["Probability"], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            ax4.set_xlabel("Probability (%)")
            ax4.set_ylabel("Frequency")
            ax4.set_title("Probability Distribution")

            plt.tight_layout()
            st.pyplot(fig)

        else:
            st.info("No data available for charts. Make some predictions first!")

    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()