import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def display_page():
    tab1, tab2 = st.tabs(["Eigene Nachhaltigkeitspunkte hinzufügen", "Stakeholder Umweltpunkte hinzufügen "])
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame({
            "Thema": [""] * 5,
            "Unterthema": [""] * 5,
            "Unter-Unterthema": [""] * 5
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen', options=['Klimawandel'], index=0, key='thema')
        unterthema = st.selectbox('Unterthema auswählen', options=['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'], index=0, key='unterthema')
        unter_unterthema = st.text_input('Unter-Unterthema eingeben', key='unter_unterthema')
        add_row = st.button('Hinzufügen', key='add_row')

    if add_row:
        empty_row_index = st.session_state.df2[(st.session_state.df2["Thema"] == "") & (st.session_state.df2["Unterthema"] == "") & (st.session_state.df2["Unter-Unterthema"] == "")].first_valid_index()
        if empty_row_index is not None:
            st.session_state.df2.at[empty_row_index, "Thema"] = thema
            st.session_state.df2.at[empty_row_index, "Unterthema"] = unterthema
            st.session_state.df2.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
        else:
            new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
            st.session_state.df2 = st.session_state.df2._append(new_row, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df2)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    grid_response = AgGrid(
        st.session_state.df2.reset_index(),
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,
        width='100%',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        return_mode=DataReturnMode.__members__['AS_INPUT'],  # Adjust the DataReturnMode as per available options
        selection_mode='multiple'
    )

    add_empty_row = st.button('Leere Zeile hinzufügen', key='add_empty_row')
    if add_empty_row:
        empty_row = {"Thema": "", "Unterthema": "", "Unter-Unterthema": ""}
        st.session_state.df2 = st.session_state.df2._append(empty_row, ignore_index=True)
        st.experimental_rerun()

    delete_rows = st.button('Ausgewählte Zeilen löschen', key='delete_rows')
    if delete_rows:
        selected_rows = grid_response['selected_rows']
        selected_indices = [row['index'] for row in selected_rows]
        st.session_state.df2 = st.session_state.df2.drop(selected_indices)
        st.experimental_rerun()

    save_changes = st.button('Änderungen speichern', key='save_changes')
    if save_changes:
        st.session_state.df2 = grid_response['data'].set_index('index')





























    









