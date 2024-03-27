import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd
import time

def long_running_function():
    time.sleep(3)  # Simuliert eine lange Aufgabe

with st.spinner('Bitte warten Sie, die Seite wird geladen...'):
    long_running_function()

def add_entry_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.header("Neuen Eintrag hinzufügen")
        gruppe = st.text_input("Gruppe", '')
        bestehende_beziehung = st.selectbox("Bestehende Beziehung", ['', 'Ja', 'Nein'])
        auswirkung = st.selectbox("Auswirkung auf Interessen", ['', 'Hoch', 'Mittel', 'Niedrig'])
        level_des_engagements = st.selectbox("Level des Engagements", ['', 'Hoch', 'Mittel', 'Niedrig'])
        stakeholdergruppe = st.selectbox("Stakeholdergruppe", ['', 'Intern', 'Extern'])
        kommunikation = st.selectbox("Kommunikation", ['', 'Regelmäßig', 'Gelegentlich', 'Nie'])
        art_der_betroffenheit = st.selectbox("Art der Betroffenheit", ['', 'Direkt', 'Indirekt', 'Keine'])
        zeithorizont = st.selectbox("Zeithorizont", ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'])

        if st.button("Eintrag hinzufügen"):
            new_entry = {
                'Gruppe': gruppe,
                'Bestehende Beziehung': bestehende_beziehung,
                'Auswirkung auf Interessen': auswirkung,
                'Level des Engagements': level_des_engagements,
                'Stakeholdergruppe': stakeholdergruppe,
                'Kommunikation': kommunikation,
                'Art der Betroffenheit': art_der_betroffenheit,
                'Zeithorizont': zeithorizont,
            }

            new_entry_df = pd.DataFrame([new_entry])
            st.session_state['namen_tabelle'] = pd.concat([st.session_state['namen_tabelle'], new_entry_df], ignore_index=True)
            # Aktualisiere den Key für AgGrid, um eine Neurenderung zu erzwingen
            st.session_state['grid_update_key'] = st.session_state.get('grid_update_key', 0) + 1

def display_page():
    if 'namen_tabelle' not in st.session_state:
        st.session_state['namen_tabelle'] = pd.DataFrame({
            'Gruppe': ['Beispielgruppe'],
            'Bestehende Beziehung': ['Ja'],
            'Auswirkung auf Interessen': ['Hoch'],
            'Level des Engagements': ['Mittel'],
            'Stakeholdergruppe': ['Intern'],
            'Kommunikation': ['Regelmäßig'],
            'Art der Betroffenheit': ['Direkt'],
            'Zeithorizont': ['Langfristig'],
        })

    st.subheader("Stakeholder Identifikation und Bewertung")
    add_entry_sidebar()

    gb = GridOptionsBuilder.from_dataframe(st.session_state['namen_tabelle'])
    gb.configure_default_column(editable=True, resizable=True)
    gb.configure_selection('multiple', use_checkbox=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    # Anzeige der Tabelle mit AgGrid
    grid_key = f"grid_{st.session_state.get('grid_update_key', 0)}"
    grid_response = AgGrid(
        st.session_state['namen_tabelle'],
        gridOptions=gridOptions,
        height=500,
        width='100%',
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=False,
        theme='streamlit',
        enable_enterprise_modules=True,
        key=grid_key 
    )
    
     # Speichere die Änderungen zurück in den session_state, um sie persistent zu machen
    st.session_state['namen_tabelle'] = pd.DataFrame(grid_response['data'])

    # Optional: Rücksetzen der ausgewählten Zeilen nach der Verarbeitung
    st.session_state['selected_rows'] = []