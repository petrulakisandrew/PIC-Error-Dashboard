import streamlit as st
import os
from db import log_login
from datetime import datetime, timezone

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="PIC Error Dashboard Login",
    page_icon = "./assets/favi.ico",
)

#Title for Log-In
st.title("PIC Error Dashboard Login Page")

if "login_logged" not in st.session_state:
    st.session_state.login_logged = False

if not st.user.is_logged_in:
    st.subheader("Please Log In Below.")
    login_button = st.button("Log in with Microsoft", on_click = st.login, kwargs = {"provider":"microsoft"})
    print('Login Button Clicked')






    

