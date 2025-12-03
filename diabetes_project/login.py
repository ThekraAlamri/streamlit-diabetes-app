import streamlit as st
import sqlite3
import bcrypt


def login():
    """User login page"""
    st.title("🔑 Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not username or not password:
                st.error("Please enter username and password")
                return

            conn = sqlite3.connect('db/diabetes_app.db')
            c = conn.cursor()

            try:
                c.execute("SELECT password FROM users WHERE username=?", (username,))
                data = c.fetchone()

                if data:
                    stored_password = data[0]
                    if bcrypt.checkpw(password.encode(), stored_password):
                        st.success(f"Welcome back, {username}!")
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.rerun()
                    else:
                        st.error("Incorrect password")
                else:
                    st.error("User not found")

            except sqlite3.Error as e:
                st.error(f"Database error: {e}")
            finally:
                conn.close()