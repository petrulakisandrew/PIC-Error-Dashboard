import streamlit as st
from dotenv import load_dotenv
from db import DatabaseController
import os


load_dotenv()

#Initializing Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
    
st.switch_page("pages/login.py")

    

  