import streamlit as st
import bcrypt
import os

#Reading hashed password from secure file as universal variable
PASSWORD = os.getenv("PASSWORD").encode("utf-8")

#Password verification definition
def check_password(password):
    print(f'Checking password hash: {bcrypt.hashpw(password.encode("utf-8"), PASSWORD)} against stored hash: {PASSWORD}')
    return bcrypt.checkpw(password.encode('utf-8'), PASSWORD)

def login_attempt(user_input):
    print(f'Login attempt')
    if check_password(user_input):
        print(f"Password Correct") 
        st.session_state.logged_in = True
        # st.switch_page("./pages/dash.py")
        # st.success("Weclome") 
    else:
        print(f"Password incorrect") 
        st.session_state.logged_in = False
        st.warning("Incorrect Password")
        st.stop()


#Login Check:
if "logged_in" not in st.session_state or st.session_state.logged_in ==  False:
    st.session_state.logged_in = False
    
#Title for Log-In
st.title("PIC Error Dashboard Login Page")

#Implementing Password for Dashboard:  
if not st.session_state.logged_in:
    user_input = st.text_input("Enter password", type = "password").strip()
    login_button = st.button("Login", on_click = login_attempt, args = (user_input,))
    
if st.session_state.logged_in and st.session_state.logged_in ==  True:
    st.switch_page("./pages/dash.py")

    

# st.write(st.session_state.logged_in) 