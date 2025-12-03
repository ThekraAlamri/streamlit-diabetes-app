import streamlit as st
from login import login_page
from logout import logout_page
from predict import predict_page
from charts import charts_page
from history import history_page
from train_model import model_info_page
from signup import signup_page

st.set_page_config(page_title="Diabetes App", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def main():
    if not st.session_state.logged_in:
        selected = st.sidebar.radio("🔐 Menu", ["Login", "Sign Up"])
        if selected == "Login":
            login_page()
        elif selected == "Sign Up":
            signup_page()
    else:
        st.sidebar.success(f"👋 Welcome, {st.session_state.username}!")
        selected = st.sidebar.radio("📋 Navigation", [
            "🏠 Home",
            "🩺 Predict Diabetes",
            "💊 Treatment Information",
            "📊 Model Info",
            "📈 Charts & Visualization",
            "🔓 Logout"
        ])

        if selected == "🏠 Home":
            st.title("🏠 Home")
            st.write("This is the Diabetes Prediction App homepage.")
        elif selected == "🩺 Predict Diabetes":
            predict_page()
        elif selected == "💊 Treatment Information":
            st.title("💊 Treatment Information")
            st.write("Information about treatments for diabetes.")
        elif selected == "📊 Model Info":
            model_info_page()
        elif selected == "📈 Charts & Visualization":
            charts_page()
        elif selected == "🔓 Logout":
            logout_page()

if __name__ == "__main__":
    main()
