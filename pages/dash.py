import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import bcrypt
import time
import os
from nav import navigation
from db import log_login


#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Importing Excel DF
excel_file = os.getenv("EXCEL_PATH")
# print(excel_file)
      
df = pd.read_excel(excel_file, header=26)

#Masking SSN in "HOH SSN" column 
df["HOH SSN"] = df["HOH SSN"].apply(lambda x: '***-**-' + x[6:])

#Masking all SSN's in "Field in Error" Column
df["Field Contents"] = df["Field Contents"].apply(lambda x: '***-**-' + x[6:] if len(str(x).strip()) ==  9 else x)
    
#Cleaning unused columns
df = df.drop(["Rec Nbr in Error","Section","Development Number", "Building Number", "Building Number Entrance","Unit Number","PHA Use Only1","PHA Use Only2","PHA Use Only3","PHA Use Only4","PHA Use Only5"], axis=1)


#Caseworker Column
conditions = [
    (df["Last Name"].str.strip().str.lower() >= "a" ) & (df["Last Name"].str.strip().str.lower() <= "bel"), 
    (df["Last Name"].str.strip().str.lower() >= "ben" ) & (df["Last Name"].str.strip().str.lower() <= "col"),
    (df["Last Name"].str.strip().str.lower() >= "con" ) & (df["Last Name"].str.strip().str.lower() <= "ful"),
    (df["Last Name"].str.strip().str.lower() >= "gad" ) & (df["Last Name"].str.strip().str.lower() <= "haw"),
    (df["Last Name"].str.strip().str.lower() >= "hay" ) & (df["Last Name"].str.strip().str.lower() <= "lev"),
    (df["Last Name"].str.strip().str.lower() >= "lew" ) & (df["Last Name"].str.strip().str.lower() <= "pau"),
    (df["Last Name"].str.strip().str.lower() >= "paw" ) & (df["Last Name"].str.strip().str.lower() <= "ste"), 
    (df["Last Name"].str.strip().str.lower() >= "sti" ) & (df["Last Name"].str.strip().str.lower() <= "z"),
]

caseworkers = ["Candice","Gail","Scott","Cristine","Sandra","Ozury","Occupancy","Mary"]

df["Caseworker"] = np.select(conditions, caseworkers, default="Other")


df = df.drop(df[df["Error Type"] == " WARNING"].index)


#Page 2: Content
        
#Navigation Bar
with st.sidebar:
    navigation()

#Setting Wide Screen Configuration 
st.set_page_config(
    layout = "wide"
)


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
            PIC Fatal Error Dashboard
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
 
#Including Total Count of Fatal Errors and Date
col1, col2, col3, col4 = st.columns(4) 
col1.metric("Total Fatal Errors", df["Error Number"].count()) 

today = datetime.today().strftime("%B %d, %Y")
col4.metric("Date", today)

#All Counts and Sub DF's
case_counts = df["Caseworker"].value_counts().reset_index()
case_counts.columns = ["Caseworker", "Count"]

action_counts = df["Type of Action"].value_counts().reset_index()
action_counts.columns = ["Action Type", "Count"]
action_counts["Action Type"] = action_counts["Action Type"].astype(str) + " action" 
 
# Side-by-side charts
col1, col2, = st.columns(2)

with col1:
    st.subheader("Errors by Caseworker")
    st.bar_chart(data=case_counts.set_index("Caseworker")["Count"])


with col2:
    st.subheader("Errors by 58 Action Type")
    action_counts["Percent"] = 100 * action_counts["Count"] / action_counts["Count"].sum()
    action_counts["Percent"] = action_counts["Percent"].map("{:.2f}%".format)
    st.table(action_counts[["Action Type", "Count", "Percent"]])


# --- Selection: show rows for chosen caseworker ---
selected_caseworker = st.selectbox("Select a caseworker to view their errors", case_counts["Caseworker"])
filtered_df = df[df["Caseworker"] == selected_caseworker]
st.write(f"Showing all errors for **{selected_caseworker}**:")
st.dataframe(filtered_df, width = 2000, hide_index = True)

st.set_page_config(
    page_title="DHA Dashboard",
    page_icon="./assets/favi.ico"
)