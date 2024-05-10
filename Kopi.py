import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def display_page():
    # Erstellen eines Beispieldatenrahmens
    data = {
        "ID": [1, 2, 3, 4],
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40]
    }
    df = pd.DataFrame(data)

    # Initialisieren der Spalte 'Bewertet' mit 'Nein' für alle Zeilen
    if 'selected_data' in st.session_state:
        # Update 'Bewertet' basierend auf vorhandenen Bewertungen
        df['Bewertet'] = df['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        df['Bewertet'] = 'Nein'
    
    # Erstellen der Bewertungsauswahl
    bewertung = st.selectbox("Bewertung auswählen:", ["", "Gut", "Mittel", "Schlecht"])

    # Button zum Absenden der Bewertung
    if st.button("Bewertung absenden") and bewertung:
        if 'selected_rows' in st.session_state:
            new_data = pd.DataFrame(st.session_state['selected_rows'])
            # Entfernen der Spalte _selectedRowNodeInfo
            if '_selectedRowNodeInfo' in new_data.columns:
                new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)
            new_data['Bewertung'] = bewertung  # Hinzufügen der Bewertung zu den ausgewählten Zeilen
            
            # Prüfen, ob bereits Daten im Session State gespeichert sind
            if 'selected_data' in st.session_state:
                # Anhängen der neuen Daten an das bestehende DataFrame
                st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
            else:
                # Speichern des neuen DataFrame im Session State
                st.session_state.selected_data = new_data
            
            # Aktualisieren der 'Bewertet' Spalte im Haupt-DataFrame
            df['Bewertet'] = df['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
        
    # Anzeigen des DataFrame, wenn es im Session State gespeichert ist und Inhalt hat
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        st.write("Bewertetes DataFrame:")
        st.dataframe(st.session_state.selected_data)

    # Erstellen der Grid-Optionen
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    grid_options = gb.build()

    # Anzeigen des AgGrid
    grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)

    # Speichern der ausgewählten Zeilen im Session State
    st.session_state['selected_rows'] = grid_response['selected_rows']

display_page()



