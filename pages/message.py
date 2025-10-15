import streamlit as st
from db import log_message
from db import query_message
from datetime import datetime, timezone
import pandas as pd
from db import DatabaseController
import os 
from nav import navigation

def display_chat():
    rows = query_message()
    message_df = pd.DataFrame(rows, columns = ["First Name","Last Name","Message","Timestamp"])
    
    for i, row in message_df.iterrows():
        with st.chat_message("user"):
            st.markdown(f"{row['First Name']} : {row['Message']}")
    # print(message_df)


#Checking Log In State
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    
#Navigation Bar
with st.sidebar:
    navigation()
    

#Page Header    
st.markdown("<h1 style='text-align: center;'>Message Board</h1>", unsafe_allow_html=True)

#Chat Message Box
prompt = st.chat_input(
    "Say something"   
) 

if prompt:
    log_message(prompt, datetime.now(timezone.utc),st.user.get("name").split(" ")[0], st.user.get("name").split(" ")[-1])

display_chat()

st.set_page_config(
    page_title="DHA Dashboard",
    page_icon="./assets/favi.ico"
)