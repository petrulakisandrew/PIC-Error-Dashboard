import streamlit as st
from db import check_permission
from util.helpers import vendor_status_badge


def handle_logout():
    st.logout()
    st.session_state.logged_login = False

def navigation():
        st.button("Log out", on_click=handle_logout)
        with st.sidebar.expander("PIC Systems"):
            st.page_link("pages/dash.py", label="Fatal Error Dashboard")
            st.page_link("pages/info.py", label="Information")
        st.sidebar.page_link("pages/vendor_requests.py", label="Vendor Approval Requests", icon = vendor_status_badge())
        st.sidebar.page_link("pages/message.py", label="Announcement Board")
        st.sidebar.page_link("pages/tax_abatement.py", label="Tax Abatement Program")
        if check_permission(st.user["email"],'admin'):
            with st.sidebar.expander("Admin"):
                st.page_link("pages/admin.py", label="Permissions")
                st.page_link("pages/all_logins.py", label="Monitor Logins")
