import streamlit as st
from nav import navigation
import pandas as pd
from db import insert_vendor
from db import query_vendor_requests
from datetime import datetime

#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    
#Page Config
st.set_page_config(
    layout = "wide",
    page_title="Vendor Approval Requests",
    page_icon = "./assets/favi.ico",
)

#Navigation Bar:
with st.sidebar:
    navigation()
  
  
def convert_columns_datetime(columns):
    for column in columns:
        vendor_df[column] = pd.to_datetime(vendor_df[column])
            

def convert_columns_bool(columns):
    for column in columns:
        vendor_df[column] = vendor_df[column].astype(bool)

current_requests = query_vendor_requests()

#Header    
st.markdown("""
    <div style="
        text-align: center;
        margin-top: -30px;
        margin-bottom: 5px;
    ">
        <h1 style="
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-weight: 600;
            font-size: 2.2em;
            color: white;
            margin-bottom: 12px;
        ">
            Vendor Approval Requests
        </h1>
        <div style="
            width: 60%;
            height: 2px;
            margin: 0 auto;
            background: linear-gradient(
                to right,
                rgba(0,0,0,0),
                rgba(100,149,237,0.75),
                rgba(0,0,0,0)
            );
            border-radius: 1px;
        "></div>
    </div>
""", unsafe_allow_html=True)   

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

# Create empty DataFrame with all columns as strings
vendor_df = pd.DataFrame(current_requests, columns = columns)

#Date Time Columsn
date_columns = ['Request Received Date','Sent to Compliance for Approval Date','Approval Date']
convert_columns_datetime(date_columns)

#Boolean Columns
bool_columns = ["W-9","Proof of Ownership","Owner Declaration","Economic Disclosure Statement","Direct Deposit Authorization","Canceled Check or Similar","Status"]
convert_columns_bool(bool_columns)


st.data_editor(
    vendor_df,
    column_config = {
        "Landlord/Owner/Agent": st.column_config.TextColumn(
            "Landlord/Owner/Agent",
            help = "Vendor From Yardi Voyager",
            max_chars = 120,
        ),
        "Request Received Date": st.column_config.DatetimeColumn(
            label = "Request Received Date",
            help = "Date Request Was Received in Voyager",
            min_value = None,
            max_value = datetime.today(),
            format = "YYYY-MM-DD",
            step = 86400
        ),
        "Requester": st.column_config.TextColumn(
            "Requester",
            help = "Initial Requester for Vendor Approval",
            max_chars = 60,
        ),
        "V-Code Created/Used": st.column_config.TextColumn(
            "V-Code Created/Used",
            help = "Created V-Code for Vendor",
            max_chars = 8,
        ),
        "W-9": st.column_config.SelectboxColumn(
            "W-9",
            help = "Check if W-9 Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Federal Tax Class": st.column_config.SelectboxColumn(
            "Federal Tax Class",
            help = "Federal Tax Class of Vendor",
            width = "Medium",
            options = [
                "Sole Proprietor",
                "LLC - C Corporation",
                "LLC - S Corporation",
                "LLC - Partnership",
                "Public Benefit Organization",
                "Other"
            ]
        ),
        "Proof of Ownership": st.column_config.SelectboxColumn(
            "Proof of Ownership",
            help = "Check if Proof of Ownership Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Owner Declaration": st.column_config.SelectboxColumn(
            "Owner Declaration",
            help = "Check if Owner Declaration Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Economic Disclosure Statement": st.column_config.SelectboxColumn(
            "Economic Disclosure Statement",
            help = "Check if Economic Disclosure Statement Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Direct Deposit Authorization": st.column_config.SelectboxColumn(
            "Direct Deposit Authorization",
            help = "Check if Direct Deposit Authorization Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Canceled Check or Similar": st.column_config.SelectboxColumn(
            "Canceled Check or SimilarCanceled Check or Similar",
            help = "Check if a Canceled Check or Similar Exists",
            width = "Medium",
            options = [True, False]
        ),
        "Creator": st.column_config.TextColumn(
            "Creator",
            help = "Creator of Vendor Approval Request",
            max_chars = 60,
        ),
        "Sent to Compliance for Approval Date": st.column_config.DatetimeColumn(
            label = "Sent to Compliance for Approval Date",
            help = "Date Request Was Sent to Compliance",
            min_value = None,
            max_value = datetime.today(),
            format = "YYYY-MM-DD",
            step = 86400
        ),
        "Approver": st.column_config.TextColumn(
            "Approver",
            help = "Name of Vendor Request Approver",
            max_chars = 60,
        ),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help = "Request Approval Status",
            width = "Medium",
            options = [True, False]
        ),
        "Approval Date": st.column_config.DatetimeColumn(
            label = "Approval Date",
            help = "Date Request Was Approved by Compliance",
            min_value = None,
            max_value = datetime.today(),
            format = "YYYY-MM-DD",
            step = 86400
        ),
        "Email": st.column_config.TextColumn(
            "Email",
            help = "Email of Vendor Request Creator",
            max_chars = 120,
        ),
    },
    hide_index = True,
    num_rows = "dynamic",
    disabled = False
)

# insert_vendor('test', datetime(2025, 10, 21, 15, 30, 0), 'test', 'test', True, 'test', True, True, True, True, True, 'test', datetime(2025, 10, 21, 15, 30, 0), 'test', True, datetime(2025, 10, 21, 15, 30, 0), 'test')