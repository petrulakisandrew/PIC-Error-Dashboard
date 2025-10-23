import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import bcrypt
import time
import os
from nav import navigation
from db import log_login
import glob


#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="PIC Fatal Error Dashboard",
    page_icon = "./assets/favi.ico",
)


def file_path_creation(directory, file_name, file):
    os.makedirs(directory, exist_ok = True)
    file_path = os.path.join(directory, file_name)
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(file.getbuffer())
    st.success(f'File {file_name} has been saved to {directory}')
    

#Dialog Box
@st.dialog("Choose Current  PIC Error File", width = 'large', on_dismiss = 'rerun')
def file():
    current_excel_file = st.file_uploader("Browse Machine for Files Below", type = 'xlsx')
    
    if current_excel_file is not None:
        print(current_excel_file.name)
        df = pd.read_excel(current_excel_file)
        st.write(df)
        if st.user['email'] == 'Petrulakisandrew@gmail.com' and st.user["oid"] == "00000000-0000-0000-56f2-9fdf9261e520":
            st.button(
                "Confirm Upload?", 
                on_click = file_path_creation(
                    os.getenv("TARGET_DIRECTORY"), 
                    current_excel_file.name, 
                    current_excel_file
                )
            )
    else:
        st.warning("⚠️ No File Currently Selected")


#Importing Excel DF
directory = os.getenv("TARGET_DIRECTORY")
all_files = glob.glob(os.path.join(directory, "*.xlsx"))

if not all_files:
    raise FileNotFoundError("No Valid Files Found")
    
excel_file = max(all_files, key = os.path.getmtime)
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

if st.user['email'] == 'Petrulakisandrew@gmail.com' and st.user["oid"] == "00000000-0000-0000-56f2-9fdf9261e520":
    st.button("Upload File", on_click= file, type = 'primary', help = "Change The Error Data this Dashboard is Diplaying")
    
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
st.dataframe(filtered_df, 
    width = 2000, 
    hide_index = True
)