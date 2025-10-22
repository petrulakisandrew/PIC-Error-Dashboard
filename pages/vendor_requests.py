import streamlit as st
from nav import navigation
import pandas as pd
from db import insert_vendor
from db import query_vendor_requests
from datetime import datetime

# Page Config
st.set_page_config(
    layout="wide",
    page_title="Vendor Approval Requests",
    page_icon="./assets/favi.ico",
)

# Check Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

# Navigation Bar
with st.sidebar:
    navigation()


def load_data_from_db():
    """Load vendor requests from database and return formatted DataFrame."""
    columns = [
        "Landlord/Owner/Agent",
        "Request Received Date",
        "Requester",
        "V-Code Created/Used",
        "W-9",
        "Federal Tax Class",
        "Proof of Ownership",
        "Owner Declaration",
        "Economic Disclosure Statement",
        "Direct Deposit Authorization",
        "Canceled Check or Similar",
        "Creator",
        "Sent to Compliance for Approval Date",
        "Approver",
        "Status",
        "Approval Date",
        "User Email"
    ]
    
    current_requests = query_vendor_requests()
    df = pd.DataFrame(current_requests, columns=columns)
    
    # Convert date columns
    date_columns = [
        'Request Received Date',
        'Sent to Compliance for Approval Date',
        'Approval Date'
    ]
    for column in date_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda x: datetime.strptime(x, '%Y-%m-%d').date() if pd.notna(x) and x and isinstance(x, str) else (x if pd.notna(x) else None)
            )
    
    # Convert boolean columns
    bool_columns = [
        "W-9",
        "Proof of Ownership",
        "Owner Declaration",
        "Economic Disclosure Statement",
        "Direct Deposit Authorization",
        "Canceled Check or Similar",
        "Status"
    ]
    for column in bool_columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda v: None if pd.isna(v) else bool(v))
    
    return df


# Initialize data ONLY on first load
if "vendor_data_initialized" not in st.session_state:
    st.session_state.vendor_data_initialized = True
    st.session_state.vendor_data = load_data_from_db()


def refresh_from_database():
    """Callback to reload data from database."""
    st.session_state.vendor_data = load_data_from_db()
    # Clear the editor state to force re-initialization
    if "vendor_editor" in st.session_state:
        del st.session_state.vendor_editor


# Header
st.title("Vendor Approval Requests")

# Controls
col1, col2 = st.columns([1, 5])
with col1:
    st.button("🔄 Refresh from Database", on_click=refresh_from_database)

# Display count
st.write(f"**Total Requests:** {len(st.session_state.vendor_data)}")

# Data Editor
edited_df = st.data_editor(
    st.session_state.vendor_data,
    key="vendor_editor",
    column_config={
        "Landlord/Owner/Agent": st.column_config.TextColumn(
            "Landlord/Owner/Agent",
            help="Vendor From Yardi Voyager",
            max_chars=120,
        ),
        "Request Received Date": st.column_config.DateColumn(
            "Request Received Date",
            help="Date Request Was Received in Voyager",
            format="YYYY-MM-DD",
        ),
        "Requester": st.column_config.TextColumn(
            "Requester",
            help="Initial Requester for Vendor Approval",
            max_chars=60,
        ),
        "V-Code Created/Used": st.column_config.TextColumn(
            "V-Code Created/Used",
            help="Created V-Code for Vendor",
            max_chars=8,
        ),
        "W-9": st.column_config.CheckboxColumn(
            "W-9",
            help="Check if W-9 Exists",
            default=False,
        ),
        "Federal Tax Class": st.column_config.SelectboxColumn(
            "Federal Tax Class",
            help="Federal Tax Class of Vendor",
            width="medium",
            options=[
                "Sole Proprietor",
                "LLC - C Corporation",
                "LLC - S Corporation",
                "LLC - Partnership",
                "Public Benefit Organization",
                "Other"
            ],
        ),
        "Proof of Ownership": st.column_config.CheckboxColumn(
            "Proof of Ownership",
            help="Check if Proof of Ownership Exists",
            default=False,
        ),
        "Owner Declaration": st.column_config.CheckboxColumn(
            "Owner Declaration",
            help="Check if Owner Declaration Exists",
            default=False,
        ),
        "Economic Disclosure Statement": st.column_config.CheckboxColumn(
            "Economic Disclosure Statement",
            help="Check if Economic Disclosure Statement Exists",
            default=False,
        ),
        "Direct Deposit Authorization": st.column_config.CheckboxColumn(
            "Direct Deposit Authorization",
            help="Check if Direct Deposit Authorization Exists",
            default=False,
        ),
        "Canceled Check or Similar": st.column_config.CheckboxColumn(
            "Canceled Check or Similar",
            help="Check if a Canceled Check or Similar Exists",
            default=False,
        ),
        "Creator": st.column_config.TextColumn(
            "Creator",
            help="Creator of Vendor Approval Request",
            max_chars=60,
        ),
        "Sent to Compliance for Approval Date": st.column_config.DateColumn(
            "Sent to Compliance for Approval Date",
            help="Date Request Was Sent to Compliance",
            format="YYYY-MM-DD",
        ),
        "Approver": st.column_config.TextColumn(
            "Approver",
            help="Name of Vendor Request Approver",
            max_chars=60,
        ),
        "Status": st.column_config.CheckboxColumn(
            "Status",
            help="Request Approval Status (Approved = True)",
            default=False,
        ),
        "Approval Date": st.column_config.DateColumn(
            "Approval Date",
            help="Date Request Was Approved by Compliance",
            format="YYYY-MM-DD",
        ),
        "User Email": st.column_config.TextColumn(
            "User Email",
            help="Email of Vendor Request Creator",
            max_chars=120,
        ),
    },
    hide_index=True,
    num_rows="dynamic",
    width='stretch',
)

# Save section
st.divider()
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Save", type="primary", icon="💾"):
        try:
            # TODO: MAKE THE SAVE LOGIC BEATS, IT DONT SAVE NOW
            st.session_state.vendor_data = edited_df
            st.success(f"✅ Successfully saved {len(edited_df)} records to database!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error saving to database: {str(e)}")

