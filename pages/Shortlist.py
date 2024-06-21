import streamlit as st

def display_page():

    # Initialize session state
    if 'selected_columns' not in st.session_state:
        st.session_state['selected_columns'] = []

    # Title of the app
    st.title("Display Selected Columns from Session State")

    # Check if 'selected_columns' exists in the session state
    if 'selected_columns' in st.session_state:
        selected_columns = st.session_state['selected_columns']
        st.write("Selected Columns:")
        st.write(selected_columns)
    else:
        st.write("No selected columns found in session state.")


