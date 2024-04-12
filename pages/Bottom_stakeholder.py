import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def display_page():
    # Initialisierung des Session State für das DataFrame
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame({
            "Thema": [""] * 3,  # Beginnen mit 5 leeren Zeilen
            "Unterthema": [""] * 3,
            "Unter-Unterthema": [""] * 3
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen', options=['Klimawandel'], index=0)
        unterthema = st.selectbox('Unterthema auswählen', options=['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'], index=0)
        unter_unterthema = st.text_input('Unter-Unterthema eingeben')
        add_row = st.button('Hinzufügen')
        add_empty_row = st.button('Leere Zeile hinzufügen')  # Button zum Hinzufügen einer leeren Zeile
        delete_rows = st.button('Ausgewählte Zeilen löschen')  # Button zum Löschen der ausgewählten Zeilen
    
    # Hinzufügen der neuen Zeile, wenn der Button gedrückt wird
    if add_row:
        # Finde die erste komplett leere Zeile
        empty_row_index = st.session_state.df2[(st.session_state.df2["Thema"] == "") & (st.session_state.df2["Unterthema"] == "") & (st.session_state.df2["Unter-Unterthema"] == "")].first_valid_index()
        if empty_row_index is not None:
            # Aktualisiere die erste leere Zeile mit den neuen Daten
            st.session_state.df2.at[empty_row_index, "Thema"] = thema
            st.session_state.df2.at[empty_row_index, "Unterthema"] = unterthema
            st.session_state.df2.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
        else:
            # Füge eine neue Zeile hinzu, falls keine leere Zeile gefunden wurde
            new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
            st.session_state.df2 = st.session_state.df2._append(new_row, ignore_index=True)

        if add_empty_row:
            empty_row = {"Thema": "", "Unterthema": "", "Unter-Unterthema": ""}
            st.session_state.df2 = st.session_state.df2.append(empty_row, ignore_index=True)

    # Ag-Grid Konfiguration
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df2)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')  # Aktivieren der Zeilen-IDs und Festlegen der ID-Spalte auf 'index'
    grid_options = gb.build()

    # Hinzufügen der Checkbox-Spalte zu den Spaltendefinitionen
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    # Anzeige des Ag-Grids
    grid_response = AgGrid(
        st.session_state.df2.reset_index(),  # Zurücksetzen des Index, um eine Spalte 'index' zu erstellen
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,  # Einstellen der gewünschten Höhe
        width='100%',
        update_mode='MODEL_CHANGED',
        allow_unsafe_jscode=True,
        return_mode=DataReturnMode.__members__['FILTERED_AND_SORTED'],  # Rückgabe der ausgewählten Zeilen
        selection_mode='multiple'  # Erlauben der Mehrfachauswahl
    )

    # Funktion zum Löschen der ausgewählten Zeilen
    def delete_selected_rows(selected_rows):
        selected_indices = [row['index'] for row in selected_rows]  # Extrahieren der Indizes der ausgewählten Zeilen
        st.session_state.df2 = st.session_state.df2.drop(selected_indices)
        st.experimental_rerun()  # Neuladen der Seite

    # Löschen der ausgewählten Zeilen, wenn der Button gedrückt wird
    if delete_rows:
        selected_rows = grid_response['selected_rows']
        delete_selected_rows(selected_rows)





























    









