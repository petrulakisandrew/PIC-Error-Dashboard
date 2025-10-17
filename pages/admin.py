import streamlit as st
from nav import navigation
from db import check_admin
from db import store_users
from db import add_permissions
from db import remove_permissions
from db import store_permissions
from db import permission_exists



#Check Login and Logged Login
if not st.user.is_logged_in:
    st.switch_page("pages/login.py")

#Check if User is Admin:
if check_admin(st.user["email"],'admin') ==  False:
    st.switch_page("pages/dash.py")

#Page Config
st.set_page_config(
    layout = "wide"
)

#Navigation Bar:
with st.sidebar:
    navigation()
    
    
st.markdown("<h1 style='text-align: center;'>Administrative</h1>", unsafe_allow_html=True)    

user_df = store_users()

full_name = user_df["first_name"]+ ' ' + user_df["last_name"]

#User Select Box
selected_user = st.selectbox("Select a User to Modify Permissions", full_name)

first, last = selected_user.split(" ")
user_email = user_df[(user_df["first_name"] == first) & (user_df["last_name"] == last)]["email"].values[0]
st.write(f'User Email: {user_email}')


#Checkbox for All Permissions
permissions_df = store_permissions()
permissions = permissions_df['permission'].tolist()

st.dataframe(permissions_df)

checkbox_permissions = {}

for perm in permissions:
    checkbox_permissions[perm] = st.checkbox(str(perm))

st.write(checkbox_permissions.items())


#Groundwork for Select Logic
for item, checked in checkbox_permissions.items():
    if checked:
        print(f"{item} is checked")
    else:
        print(f"{item} is not checked")
    

    
st.set_page_config(
    page_title="DHA Dashboard",
    page_icon="./assets/favi.ico"
)