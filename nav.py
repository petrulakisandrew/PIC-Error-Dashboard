import streamlit as st

def navigation():
    st.sidebar.page_link("pages/login.py", label="Login Page")
    st.sidebar.page_link("pages/dash.py", label="Fatal Error Dashboard")
    st.sidebar.page_link("pages/info.py", label="Information")
