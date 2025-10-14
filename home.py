import streamlit as st
from dotenv import load_dotenv


load_dotenv()

# def login():
#     st.switch_page("pages/login.py")

#Initializing Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
    
st.switch_page("pages/login.py")

    

  