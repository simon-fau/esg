import streamlit as st

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def onCellValueChanged(params):
    rowIndex = params.node.rowIndex
    colId = params.column.colId
    newValue = params.newValue
    st.session_state.df2.at[rowIndex, colId] = newValue

def display_page():
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame({
            "Thema": [""] * 3,
            "Unterthema": [""] * 3,
            "Unter-Unterthema": [""] * 3
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen', options=['Klimawandel'], index=0, key='thema1')
        unterthema = st.selectbox('Unterthema auswählen', options=['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'], index=0, key='unterthema1')
        unter_unterthema = st.text_input('Unter-Unterthema eingeben', key='unter_unterthema1')
        add_row = st.button('Hinzufügen', key='add_row')
        add_empty_row = st.button('Leere Zeile hinzufügen', key='add_empty_row')
        delete_rows = st.button('Ausgewählte Zeilen löschen', key='delete_rows')

    if add_row:
        new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
        st.session_state.df2 = st.session_state.df2._append(new_row, ignore_index=True)

    if add_empty_row:
        empty_row = {"Thema": "", "Unterthema": "", "Unter-Unterthema": ""}
        st.session_state.df2 = st.session_state.df2._append(empty_row, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df2)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True) 
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    grid_response = AgGrid(
        st.session_state.df2,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,
        width='100%',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,  # Set this to True
        return_mode=DataReturnMode.AS_INPUT,
        selection_mode='multiple'
    )
    
    st.session_state.df2 = grid_response['data']

    if delete_rows:
        selected_rows = grid_response['selected_rows']
        selected_indices = [row['index'] for row in selected_rows]
        st.session_state.df2 = st.session_state.df2.drop(selected_indices).reset_index(drop=True)
        st.experimental_rerun()
