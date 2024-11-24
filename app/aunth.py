import streamlit as st
import yaml
from yaml.loader import SafeLoader

import streamlit_authenticator as stauth
from typing import List, Dict



def authenticate():
    with open('app/config/aunth_config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
    
    if st.session_state['authentication_status']:
        authenticator.logout(location='sidebar')
        st.write(f'Салам Алейкум, *{st.session_state["name"]}*')
        return True
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
        
    return False
