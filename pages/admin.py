import streamlit as st
from nav import navigation
from db import check_admin



#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Check if User is Admin:
if check_admin(st.user["email"],'admin') ==  False:
    st.switch_page("pages/dash.py")

#Page Config
st.set_page_config(
    layout = "wide"
)

#Navigation Bar:
with st.sidebar:
    navigation()
    
    
st.markdown("<h1 style='text-align: center;'>Administrative</h1>", unsafe_allow_html=True)    
    
    
st.set_page_config(
    page_title="DHA Dashboard",
    page_icon="./assets/favi.ico"
)