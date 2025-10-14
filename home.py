import streamlit as st
from dotenv import load_dotenv
from db import DatabaseController
import os


load_dotenv()

#Initializing Session
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
else:
    st.switch_page("pages/dash.py")

    


    

  