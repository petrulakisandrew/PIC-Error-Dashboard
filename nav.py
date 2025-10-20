import streamlit as st
from db import check_permission

def navigation():
    if check_permission(st.user["email"],'admin') ==  False:
        st.sidebar.page_link("pages/dash.py", label="Fatal Error Dashboard")
        st.sidebar.page_link("pages/message.py", label="Announcement Board")
        st.sidebar.page_link("pages/info.py", label="Information")
    else:
        st.sidebar.page_link("pages/dash.py", label="Fatal Error Dashboard")
        st.sidebar.page_link("pages/message.py", label="Announcement Board")
        st.sidebar.page_link("pages/info.py", label="Information")
        st.sidebar.page_link("pages/admin.py", label="Admin")
