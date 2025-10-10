import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import bcrypt
import time
import os

#Check Login
if "logged_in" not in st.session_state or st.session_state.logged_in ==  False:
    st.session_state.logged_in = False
    st.switch_page("pages/login.py")
    

#Importing Excel DF
excel_file = os.getenv("EXCEL_PATH")
print(excel_file)
      
df = pd.read_excel(excel_file, header=26)

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
print(df)

#Page 2: Content
        
#Header for the Dashboard

#Setting Wide Screen Configuration 
st.set_page_config(
    layout = "wide"
)

st.markdown("<h1 style='text-align: center;'>PIC Fatal Error Dashboard</h1>", unsafe_allow_html=True)
 
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
    st.table(action_counts[["Action Type", "Count", "Percent"]])


# --- Selection: show rows for chosen caseworker ---
selected_caseworker = st.selectbox("Select a caseworker to view their errors", case_counts["Caseworker"])
filtered_df = df[df["Caseworker"] == selected_caseworker]
st.write(f"Showing all errors for **{selected_caseworker}**:")
st.dataframe(filtered_df, width = 2000,)

st.set_page_config(
    page_title="DHA Dashboard",
    page_icon="./assets/favi.ico"
)