import streamlit as st
from dotenv import load_dotenv


load_dotenv()

# def login():
#     st.switch_page("pages/login.py")

#Initializing Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
pages = {
    "Navigation": [
        st.Page("./pages/login.py", title="Login Page"),
        st.Page("./pages/dash.py", title="PIC Error Dashboard"),
    ],
}

pg = st.navigation(pages)
pg.run()
    
st.switch_page("pages/login.py")

    

  