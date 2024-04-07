import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

def display_page():
    # Initialisierung des Session State für das DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "Thema": [""] * 5,  # Beginnen mit 5 leeren Zeilen
            "Unterthema": [""] * 5,
            "Unter-Unterthema": [""] * 5
        })

    # Sidebar für die Eingabe neuer Zeilen
    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen', options=['Klimawandel'], index=0)
        unterthema = st.selectbox('Unterthema auswählen', options=['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'], index=0)
        unter_unterthema = st.text_input('Unter-Unterthema eingeben')
        add_row = st.button('Hinzufügen')

    # Hinzufügen der neuen Zeile, wenn der Button gedrückt wird
    if add_row:
        # Finde die erste komplett leere Zeile
        empty_row_index = st.session_state.df[(st.session_state.df["Thema"] == "") & (st.session_state.df["Unterthema"] == "") & (st.session_state.df["Unter-Unterthema"] == "")].first_valid_index()
        if empty_row_index is not None:
            # Aktualisiere die erste leere Zeile mit den neuen Daten
            st.session_state.df.at[empty_row_index, "Thema"] = thema
            st.session_state.df.at[empty_row_index, "Unterthema"] = unterthema
            st.session_state.df.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
        else:
            # Füge eine neue Zeile hinzu, falls keine leere Zeile gefunden wurde
            new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
            st.session_state.df = st.session_state.df._append(new_row, ignore_index=True)

    # Ag-Grid Konfiguration
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight')
    grid_options = gb.build()

    # Anzeige des Ag-Grids
    grid_response = AgGrid(
        st.session_state.df,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,  # Einstellen der gewünschten Höhe
        width='100%',
        update_mode='MODEL_CHANGED',
        allow_unsafe_jscode=True
    )

    # Aktualisieren des DataFrames im Session State
    st.session_state.df = pd.DataFrame(grid_response['data'])





    









