import streamlit as st
from db import check_permission
from util.helpers import vendor_status_badge


def handle_logout():
    st.logout()
    st.session_state.logged_login = False

def navigation():
        st.button("Log out", on_click=handle_logout, icon=":material/logout:", key="logout_button")
        with st.sidebar.expander("PIC Systems"):
            st.page_link("pages/dash.py", label="Fatal Error Dashboard", icon=":material/dashboard:")
            st.page_link("pages/info.py", label="Information", icon=":material/info:")
        st.sidebar.page_link("pages/vendor_requests.py", label="Vendor Approval Requests", icon = vendor_status_badge())
        st.sidebar.page_link("pages/message.py", label="Announcement Board", icon=":material/campaign:")
        st.sidebar.page_link("pages/tax_abatement.py", label="Tax Abatement Program", icon=":material/monetization_on:")
        st.sidebar.page_link("pages/reports.py", label="Reports", icon=":material/assessment:")
        if check_permission(st.user["email"],'admin'):
            with st.sidebar.expander("Admin"):
                st.page_link("pages/admin.py", label="Permissions", icon=":material/admin_panel_settings:")
                st.page_link("pages/all_logins.py", label="Monitor Logins", icon=":material/visibility:")
