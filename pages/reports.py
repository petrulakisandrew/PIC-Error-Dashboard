import streamlit as st
from nav import navigation
import streamlit.components.v1 as components
import requests
import pandas as pd


#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="PIC Fatal Error Dashboard",
    page_icon = "./assets/favi.ico",
)

# Navigation Bar
with st.sidebar:
    navigation()
   
@st.cache_data
def load_fmrs():
    url = "https://www.huduser.gov/portal/datasets/fmr/fmr2026/fy2026_safmrs.xlsx" 
    df = pd.read_excel(url, dtype = {'ZIP Code': str})
    return df
   
    
st.header('YSR Reports')
 
df = load_fmrs()

st.dataframe(df)
