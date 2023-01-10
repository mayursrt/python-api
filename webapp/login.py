import streamlit as st
import auth
import requests
from streamlit_ws_localstorage import injectWebsocketCode
import uuid

HOST_PORT = 'linode.liquidco.in'
def login(email, password):
    conn = injectWebsocketCode(hostPort=HOST_PORT, uid=str(uuid.uuid1()))
    login_state = auth.authenticate_user(email, password)
    if login_state:
        ret = conn.setLocalStorageVal(key='access_token', val='v1')
        if ret:
            st.success("You have logged in successfully.")
        else:
            st.error("An error occured. Please try again later.")
    else:
        st.error("Invalid Credentials")


def register(email, password, password_cnf):
    if password == password_cnf:
        register_state = auth.add_user(email, password)
        if register_state:
            st.success("You have registered successfully.")
        else:
            st.error("User already exists")
    else:
        st.error("Passwords do not match.")
        
def logout():
    conn = injectWebsocketCode(hostPort=HOST_PORT, uid=str(uuid.uuid1()))
    ret = conn.setLocalStorageVal(key='access_token', val='')
    if ret:
        st.success("Successfully Logged out")
    else:
        st.error("Please try again")