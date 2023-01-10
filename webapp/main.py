import streamlit as st
import login
import requests
from streamlit_ws_localstorage import injectWebsocketCode
import uuid

HOST_PORT = 'linode.liquidco.in'
conn = injectWebsocketCode(hostPort=HOST_PORT, uid=str(uuid.uuid1()))


st.title("Login")
with st.form(key='login_form', clear_on_submit=True):
    user_email =  st.text_input('Email', type='default')
    user_password = st.text_input('Password', type='password')
    login_button = st.form_submit_button(label='Login')

if login_button:
    login.login(user_email, user_password)

a = st.sidebar.radio('Select one:', [1, 2])

st.title("Register")
with st.form(key='register_form', clear_on_submit=True):
    reg_user_email =  st.text_input('Email', type='default')
    reg_user_password = st.text_input('Password', type='password')
    reg_user_password_cnf = st.text_input('Confirm Password', type='password')
    register_button = st.form_submit_button(label='Register')

if register_button:
    login.register(reg_user_email, reg_user_password, reg_user_password_cnf)


st.title("Logout")
if st.button('Logout'):
    login.logout()