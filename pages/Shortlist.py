import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def display_page():

    # Initialize session state
    if 'selected_columns' not in st.session_state:
        st.session_state['selected_columns'] = []

    # Title of the app
    st.title("Display Selected Columns from Session State")

    # Check if 'selected_columns' exists in the session state
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Prepare the data for AgGrid
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        # Ensure necessary columns are present
        columns_to_display = ['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]

        # Configure the grid
        gb = GridOptionsBuilder.from_dataframe(selected_columns_df)
        gb.configure_side_bar()
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
        grid_options = gb.build()
        
        # Display the grid
        AgGrid(selected_columns_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    else:
        st.write("No selected columns found in session state.")





