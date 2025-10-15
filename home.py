import streamlit as st
from dotenv import load_dotenv
from db import DatabaseController
import os
from db import log_login
from datetime import datetime, timezone
from browser_detection import browser_detection_engine

load_dotenv()


if "login_logged" not in st.session_state:
    st.session_state.login_logged = False

#Initializing Session
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
elif st.user.is_logged_in and not st.session_state.login_logged:
    value = browser_detection_engine()
    log_login(st.user["email"], datetime.now(timezone.utc), value["userAgent"])
    st.session_state.login_logged = True
    st.switch_page("pages/dash.py")
else:
    st.switch_page("pages/dash.py")

    


    

  