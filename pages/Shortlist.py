import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import altair as alt

def create_shortlist():
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

def Scatter_Chart(intersection_value, stakeholder_importance_value):
    st.title("Scatter Chart")

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Prepare the data
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]
        required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating']

        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'

        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        min_rating = st.session_state.combined_df['NumericalRating'].min()
        max_rating = st.session_state.combined_df['NumericalRating'].max()
        selected_columns['size'] = ((selected_columns['NumericalRating'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        selected_columns['size'] = selected_columns['size'].fillna(100)

        # Base scatter chart
        scatter = alt.Chart(selected_columns, width=800, height=600).mark_circle().encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Environmental', 'Social', 'Governance', 'Sonstige'],
                range=['green', 'yellow', 'blue', 'gray']
            ), legend=alt.Legend(
                title="Thema",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Environmental', 'Social', 'Governance', 'Sonstige']
            )),
            size=alt.Size('size:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Importance",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=required_columns
        )

        # Line
        line = alt.Chart(pd.DataFrame({
            'x': [0, intersection_value],
            'y': [intersection_value, 0]
        })).mark_line(color='red').encode(
            x='x:Q',
            y='y:Q'
        )

       
        # Area to the left of the line
        area = alt.Chart(pd.DataFrame({
            'x': [0, 0, intersection_value],
            'y': [0, intersection_value, 0]
        })).mark_area(opacity=0.3, color='lightcoral').encode(
            x='x:Q',
            y='y:Q'
        )

        chart = scatter + area + line

        st.altair_chart(chart)

def filter_table(intersection_value, stakeholder_importance_value):
    st.title("Filtered Table")

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Prepare the data
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns
        
        # Filter the data based on the sum of 'Score Finanzen' and 'Score Auswirkung' being greater than intersection_value
        filtered_df = selected_columns_df[
            (selected_columns_df['Score Finanzen'] + selected_columns_df['Score Auswirkung'] > intersection_value) |
            (selected_columns_df['size'] > stakeholder_importance_value)
        ]
        
        # Ensure necessary columns are present
        columns_to_display = ['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Finanzen', 'Score Auswirkung']
        filtered_df = filtered_df[columns_to_display]

        # Configure the grid
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_side_bar()
        gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
        grid_options = gb.build()
        
        # Display the grid
        AgGrid(filtered_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    else:
        st.write("No selected columns found in session state.")

def display_page():
    # Slider for intersection value
    intersection_value = st.sidebar.slider("Grenzwert für Relevanz angeben", min_value=0, max_value=1000, value=100, step=10, key="intersection_slider")
    stakeholder_importance_value = st.sidebar.slider("grenzwert für Stakeholder Relevanz angeben", min_value=100, max_value=1000, value=500, step=50, key="stakeholder_importance_slider")
    create_shortlist()
    Scatter_Chart(intersection_value, stakeholder_importance_value)
    filter_table(intersection_value, stakeholder_importance_value)
