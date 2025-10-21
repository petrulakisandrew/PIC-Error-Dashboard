import streamlit as st
from nav import navigation
from db import check_permission
from db import store_users
from db import add_permissions
from db import remove_permissions
from db import store_permissions
from db import permission_exists
from db import store_user_permissions
import time


#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Check if User is Admin:
if check_permission(st.user["email"],'admin') ==  False:
    st.switch_page("pages/dash.py")

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="User Permissions",
    page_icon = "./assets/favi.ico",
)

def apply_updates():
    try:
        for item, checked in checkbox_permissions.items():
            if checked:
                if permission_exists(user_email, item) ==  False:
                    add_permissions(user_email, item)
                    print(f'{item} Added Succesfully') 
                else:
                    print(f'{item} Already Exists')
                # print(f"{item} is checked")
            else:
                if permission_exists(user_email, item) ==  True:
                    remove_permissions(user_email, item)
                    print(f'{item} Removed')
                else:
                    print(f'{item} Already Removed')
        st.toast("Updates Applied Successfully", duration = 'short', icon = ":material/done_outline:")
                # print(f"{item} is not checked")
    except Exception as e:
        st.toast(f"Error Applying Updates: {e}", duration = 'short', icon = ":material/error_outline:")

    


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
            User Permissions
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

#Storing User DataFrame
user_df = store_users()
full_name = user_df["first_name"]+ ' ' + user_df["last_name"]


#User Select Box
selected_user = st.selectbox("Select a User to Modify Permissions", full_name)
first, last = selected_user.split(" ")
user_email = user_df[(user_df["first_name"] == first) & (user_df["last_name"] == last)]["email"].values[0]
st.write(f'User Email: {user_email}')



#Check all Existing User Permissions:
user_permissions = store_user_permissions()
# print(user_permissions)

active_user_permissions = user_permissions[user_email]
# print(active_user_permissions)

#Checkbox for All Permissions
permissions_df = store_permissions()
permissions = permissions_df['permission'].tolist()
permissions_df["active"] = permissions_df["permission"].isin(active_user_permissions)


edited_df = st.data_editor(
    permissions_df,
    column_config = {
        "permission": st.column_config.TextColumn(
            "Permission",
            help = "Permission titles",
            disabled = True
        ),
        "description": st.column_config.TextColumn(
            "Description",
            help = "Description of each permission available",
            disabled = True
        ),
        "active": st.column_config.CheckboxColumn(
            "Active",
            help = "Enable or disable this permission for the user"
        )
    },
    hide_index = True
)


checkbox_permissions = dict(zip(edited_df["permission"], edited_df["active"]))


st.button(label = "Apply Changes", on_click = apply_updates)