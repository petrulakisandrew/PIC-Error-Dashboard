import streamlit as st
from nav import navigation
import pandas as pd
from db import insert_vendor, update_vendor_cell
from db import query_vendor_requests
from datetime import datetime
from util.helpers import generate_random_id
import time

COLUMN_MAP = {
    "Landlord/Owner/Agent": "landlord",
    "Request Received Date": "request_date",
    "Requester": "requester",
    "V-Code Created/Used": "vcode",
    "W-9": "w9",
    "Federal Tax Class": "fed_class",
    "Proof of Ownership": "ownership_proof",
    "Owner Declaration": "owner_declaration",
    "Economic Disclosure Statement": "disclosure",
    "Direct Deposit Authorization": "direct_deposit",
    "Canceled Check or Similar": "canceled_check",
    "Creator": "creator",
    "Sent to Compliance for Approval Date": "compliance_date",
    "Approver": "approver",
    "Status": "status",
    "Approval Date": "approved_date",
    "User Email": "email",
    "Request ID": "request_id"
}

REQUIRED_FIELDS =[
    "Landlord/Owner/Agent",
    "Request Received Date",
    "Requester",
    "V-Code Created/Used",
    "Federal Tax Class",
    "Creator",
    "Sent to Compliance for Approval Date",
]


def is_missing_required_fields(row):
    for field in REQUIRED_FIELDS:
        if pd.isna(row[field]) or row[field] == '':
            return True

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
        "User Email",
        "Request ID"
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


def refresh_from_database():
    """Callback to reload data from database."""
    st.session_state.vendor_data = load_data_from_db()
    # Clear the editor state to force re-initialization
    if "vendor_editor" in st.session_state:
        del st.session_state.vendor_editor
        
def clear_input():
    st.session_state.editor_reset_counter += 1
    

# Initialize data ONLY on first load
if "vendor_data_initialized" not in st.session_state:
    st.session_state.vendor_data_initialized = True
    st.session_state.vendor_data = load_data_from_db()

if "editor_reset_counter" not in st.session_state:
    st.session_state.editor_reset_counter = 0
    

# Header
st.title("Vendor Approval Requests")

# Controls
col1, col2 = st.columns([1, 5])
with col1:
    st.button("🔄 Refresh from Database", on_click=refresh_from_database)

# Display count
st.write(f"**Total Requests:** {len(st.session_state.vendor_data)}")

editor_key = f"vendor_editor_reset{st.session_state.editor_reset_counter}" if st.session_state.editor_reset_counter >= 0 else "vendor_editor"
print(editor_key)

# Data Editor
edited_df = st.data_editor(
    st.session_state.vendor_data,
    key= editor_key,
    column_config={
        "Landlord/Owner/Agent": st.column_config.TextColumn(
            "Landlord/Owner/Agent",
            help="Vendor From Yardi Voyager",
            max_chars=120,
            required= True,
        ),
        "Request Received Date": st.column_config.DateColumn(
            "Request Received Date",
            help="Date Request Was Received in Voyager",
            format="YYYY-MM-DD",
            required= True,
        ),
        "Requester": st.column_config.TextColumn(
            "Requester",
            help="Initial Requester for Vendor Approval",
            max_chars=60,
            required= True,
        ),
        "V-Code Created/Used": st.column_config.TextColumn(
            "V-Code Created/Used",
            help="Created V-Code for Vendor",
            max_chars=8,
            required= True,
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
            required= True,
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
            required= True,
        ),
        "Sent to Compliance for Approval Date": st.column_config.DateColumn(
            "Sent to Compliance for Approval Date",
            help="Date Request Was Sent to Compliance",
            format="YYYY-MM-DD",
            required= True,
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
        "Request ID": st.column_config.TextColumn(
            "Request ID",
            help = "ID of Vendor Approval Request",
            max_chars = 16,
            disabled = True,
            
        )
    },
    hide_index=True,
    num_rows="dynamic",
    width='stretch',
)

# Save section
st.divider()
col1, col2 = st.columns([1, 5])
with col1:
    with st.popover("Options", icon=":material/transgender:"):
        if st.button("Save", type="primary", icon=":material/save:"):
            try:
                original_df = st.session_state.vendor_data
                merged_df = edited_df.merge(original_df[['Request ID']], on = 'Request ID', how = 'left', indicator = True, suffixes = ('_old','_new'))
                
                new_rows_mask = merged_df['_merge'] ==  'left_only'
                existing_rows_mask = merged_df['_merge'] == 'both'

                new_rows = edited_df[new_rows_mask].copy()
                existing_rows = edited_df[existing_rows_mask].copy()

                for idx, row in new_rows.iterrows():
                    if is_missing_required_fields(row):
                        st.toast(f"Error Applying Updates", duration = 'short', icon = ":material/error_outline:")
                        raise Exception("❌ Missing required fields in new rows.")
                
                for idx, row in existing_rows.iterrows():
                    if is_missing_required_fields(row):
                        st.toast(f"Error Applying Updates", duration = 'short', icon = ":material/error_outline:")
                        raise Exception("❌ Missing required fields in existing rows.")
                    
                for idx, row in new_rows.iterrows():
                    if pd.isna(row['Request ID']):
                        row['Request ID'] = generate_random_id(16)
                    insert_vendor(
                        landlord=row['Landlord/Owner/Agent'],
                        request_date=row['Request Received Date'],
                        requester=row['Requester'],
                        vcode=row['V-Code Created/Used'],
                        w9=row['W-9'],
                        fed_class=row['Federal Tax Class'],
                        ownership_proof=row['Proof of Ownership'],
                        owner_declaration=row['Owner Declaration'],
                        disclosure=row['Economic Disclosure Statement'],
                        direct_deposit=row['Direct Deposit Authorization'],
                        canceled_check=row['Canceled Check or Similar'],
                        creator=row['Creator'],
                        compliance_date=row['Sent to Compliance for Approval Date'],
                        approver=row['Approver'],
                        status=row['Status'],
                        approved_date=row['Approval Date'],
                        email=st.user["email"],
                        request_id=row['Request ID']
                    )
                
                count = 0
                for idx, edited_row in existing_rows.iterrows():
                    request_id = edited_row['Request ID']
                    original_row = original_df[original_df['Request ID'] == request_id].iloc[0]
                    for column in edited_df.columns:
                        db_column = COLUMN_MAP[column]
                        if not db_column or db_column == 'request_id':
                            continue
                        if edited_row[column] != original_row[column]:
                            update_vendor_cell(request_id, db_column, edited_row[column])
                            count += 1
                            
                st.session_state.vendor_data = edited_df.copy()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving to database: {str(e)}")
        st.button("Clear User Input", on_click = clear_input)

        

