import streamlit as st
import sqlite3
import bcrypt


def signup():
    """User signup page"""
    st.title("🔐 Sign Up")

    with st.form("signup_form"):
        username = st.text_input("Choose a username")
        password = st.text_input("Choose a password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not username or not password:
                st.error("Please enter username and password")
                return

            if password != confirm_password:
                st.error("Passwords do not match")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return

            conn = sqlite3.connect('db/diabetes_app.db')
            c = conn.cursor()

            try:
                c.execute("SELECT * FROM users WHERE username=?", (username,))
                if c.fetchone():
                    st.error("Username already exists")
                    return

                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                          (username, hashed_pw))
                conn.commit()
                st.success("Account created successfully! Please login.")

            except sqlite3.Error as e:
                st.error(f"Database error: {e}")
            finally:
                conn.close()