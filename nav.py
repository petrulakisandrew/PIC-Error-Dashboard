import streamlit as st
from db import check_admin

def navigation():
    if check_admin(st.user["email"],'admin') ==  False:
        st.sidebar.page_link("pages/dash.py", label="Fatal Error Dashboard")
        st.sidebar.page_link("pages/message.py", label="Announcement Board")
        st.sidebar.page_link("pages/info.py", label="Information")
    else:
        st.sidebar.page_link("pages/dash.py", label="Fatal Error Dashboard")
        st.sidebar.page_link("pages/message.py", label="Announcement Board")
        st.sidebar.page_link("pages/info.py", label="Information")
        st.sidebar.page_link("pages/admin.py", label="Admin")
