import streamlit as st
from nav import navigation

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