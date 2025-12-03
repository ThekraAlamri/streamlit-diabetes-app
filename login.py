import streamlit as st

def login_page():
    st.title("🔐 Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Logged in as {username}")
        else:
            st.error("❌ Invalid username or password")
