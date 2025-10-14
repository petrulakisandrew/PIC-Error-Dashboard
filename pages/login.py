import streamlit as st
import bcrypt
import os
from db import log_login
from datetime import datetime

#Title for Log-In
st.title("PIC Error Dashboard Login Page")

#Implementing Microsoft Authentication for Dashboard:  
if not st.user.is_logged_in:
    st.subheader("Please Log In Below.")
    login_button = st.button("Log in with Microsoft", on_click = st.login, kwargs = {"provider":"microsoft"})
    # print(st.user, st.user.is_logged_in)
else:
    log_login("NULL",datetime.utcnow(),"NULL")
    st.switch_page("./pages/dash.py")