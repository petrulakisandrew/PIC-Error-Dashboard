import streamlit as st
from db import check_permission
from nav import navigation
from db import query_logins
from db import store_users
import pandas as pd

#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Check if User is Admin:
if check_permission(st.user["email"],'admin') ==  False:
    st.switch_page("pages/dash.py")
    
#Page Config
st.set_page_config(
    layout = "wide",
    page_title="Recent Logins",
    page_icon = "./assets/favi.ico",
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
            Recent Logins
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

#Login Data Query
login_df = pd.DataFrame(query_logins())
print(login_df)

#Pulling Active Users
active_users = store_users()

#Creating Dropdown
search = st.text_input("Filter by User")

if search:
    mask = login_df.applymap(lambda x: search in str(x).lower()).any(axis = 1)
    login_df = login_df[mask]


st.data_editor(
    login_df,
    column_config = {
        "0": st.column_config.TextColumn(
            "Email",
            help = "User Email",
            disabled = True
        ),
        "1": st.column_config.DateColumn(
            "Login Time",
            help = "Time User Logged In",
            disabled = True
        ),
        "2": st.column_config.TextColumn(
            "Agent Title",
            help = "The Machine the User Used to Login"
        ),
        "3": st.column_config.TextColumn(
            "First Name",
            help = "The Users First Name"
        ),
        "4": st.column_config.TextColumn(
            "Last Name",
            help = "The Users Last Name"
        )
        
    },
    hide_index = True
)

    

    
    