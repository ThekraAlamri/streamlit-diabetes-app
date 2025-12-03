import streamlit as st

def logout():
    st.session_state.user = None
    st.session_state.page = 'login'
    st.success("You have been logged out.")
