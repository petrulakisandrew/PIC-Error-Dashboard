import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


#Initiate GIT

#Importing Excel DF
with open("local_paths.txt", "r") as f:
    excel_file = f.readline().strip() 
      
df = pd.read_excel(excel_file, header=26)

#Cleaning unused columns
df = df.drop(["Rec Nbr in Error","Section","Development Number", "Building Number", "Building Number Entrance","Unit Number","PHA Use Only1","PHA Use Only2","PHA Use Only3","PHA Use Only4","PHA Use Only5"], axis=1)
# print(df.head())

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

#Header for the Dashboard
st.markdown("<h1 style='text-align: center;'>PIC Fatal Error Dashboard</h1>", unsafe_allow_html=True)
 
#Including Total Count of Fatal Errors
col1, = st.columns(1) 
col1.metric("Total Fatal Errors", df["Error Number"].count()) 

#Bar Chart for Errors by Caseworker
case_counts = df["Caseworker"].value_counts().reset_index()
case_counts.columns = ["Caseworker", "Count"]

st.subheader("Errors by Caseworker")


fig = px.bar(case_counts, x="Caseworker", y="Count", text="Count")
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# --- Selection: show rows for chosen caseworker ---
selected_caseworker = st.selectbox("Select a caseworker to view their errors", case_counts["Caseworker"])
filtered_df = df[df["Caseworker"] == selected_caseworker]
st.write(f"Showing all errors for **{selected_caseworker}**:")
st.dataframe(filtered_df, width = 2000,)