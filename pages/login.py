import streamlit as st
import bcrypt
import os
from db import log_login
from datetime import datetime

#Title for Log-In
st.title("PIC Error Dashboard Login Page")


if not st.user.is_logged_in:
    st.subheader("Please Log In Below.")
    st.session_state.logged_login = False
    login_button = st.button("Log in with Microsoft", on_click = st.login, kwargs = {"provider":"microsoft"})
else:
    log_login(st.user["email"],datetime.utcnow(),"NULL" )
    st.switch_page("pages/dash.py")
    





    

