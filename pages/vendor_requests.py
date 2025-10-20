import streamlit as st
from nav import navigation
import pandas as pd

#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    
#Page Config
st.set_page_config(
    layout = "wide"
)

#Navigation Bar:
with st.sidebar:
    navigation()
    

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
    "Approval Date"
]

# Create empty DataFrame with all columns as string
vendor_df = pd.DataFrame({col: pd.Series(dtype="string") for col in columns})


st.data_editor(
    vendor_df,
    column_config = {
        "Landlord/Owner/Agent": st.column_config.TextColumn(
            "Landlord/Owner/Agent",
            help = "Vendor From Yardi Voyager",
            max_chars = 50,
        )
    },
    hide_index = True,
    num_rows = "dynamic"
)