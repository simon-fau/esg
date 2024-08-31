import streamlit as st
import os
import pickle
import shutil

# Define the file paths
STATE_FILE = 'a.pkl'
DEFAULT_STATE_FILE = 'Grundlagen.pkl'

def reset_session_state():
    st.session_state.clear()  # Clear all session state values
    if os.path.exists(STATE_FILE):
        shutil.copy(DEFAULT_STATE_FILE, STATE_FILE)  # Overwrite the state file with the default
        st.success("Session state has been reset, and the default settings have been restored.")
    else:
        st.error("State file not found. Please ensure 'a.pkl' and 'Grundlagen.pkl' exist in the correct directory.")

# Display page content
def display_settings_page():
    st.header("Einstellungen")
    st.markdown("Auf dieser Seite können Sie Ihre Einstellungen verwalten.")
    
    if st.button('🔄 Reset Session State'):
        reset_session_state()

def display_page():
    display_settings_page()