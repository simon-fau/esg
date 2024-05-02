import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


def eigene_punkte():
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame({
            "Thema": [""],
            "Unterthema": [""],
            "Unter-Unterthema":[""]
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen',
        options=[
            'Klimawandel', 
            'Umweltverschmutzung', 
            'Wasser- und Meeresressourcen', 
            'Biologische Vielfalt und Ökosysteme', 
            'Kreislaufwirtschaft',
            'Eigene Belegschaft',
            'Arbeitskräfte in der Wertschöpfungskette',
            'Betroffene Gemeinschaften',
            'Verbraucher und End-nutzer',
            'Unternehmenspolitik'
            ], 
        index=0, 
        key='thema'
    )
    
        if thema == 'Klimawandel':
            unterthema_options = ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie']
        elif thema == 'Umweltverschmutzung':
            unterthema_options = [
                'Luftverschmutzung', 
                'Wasserverschmutzung', 
                'Bodenverschmutzung', 
                'Verschmutzung von lebenden Organismen und Nahrungsressourcen', 
                'Besorgniserregende Stoffe', 
                'Mikroplastik'
            ]
        elif thema == 'Wasser- und Meeresressourcen':
            unterthema_options = ['Wasser', 'Meeresressourcen']
        elif thema == 'Biologische Vielfalt und Ökosysteme':
            unterthema_options = [
                'Direkte Ursachen des Biodiversitätsverlusts', 
                'Auswirkungen auf den Zustand der Arten', 
                'Auswirkungen auf den Umfang und den Zustand von Ökosystemen'
            ]
        elif thema == 'Kreislaufwirtschaft':
            unterthema_options = [
                'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen', 
                'Ressourcenzuflüsse, einschließlich Ressourcennutzung', 
                'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 
                'Abfälle'
            ]
        elif thema == 'Eigene Belegschaft':
            unterthema_options = [
                'Arbeitsbedingungen',
                'Gleichbehandlung und Chancengleichheit für alle',
                'Sonstige arbeitsbezogene Rechte'
            ]
        elif thema == 'Arbeitskräfte in der Wertschöpfungskette':
            unterthema_options = [
                'Arbeitsbedingungen',
                'Gleichbehandlung und Chancengleichheit für alle',
                'Sonstige arbeitsbezogene Rechte'
            ]
        elif thema == 'Betroffene Gemeinschaften':
            unterthema_options = [
                'Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften',
                'Bürgerrechte und politische Rechte von Gemeinschaften',
                'Rechte indigener Völker'
            ]
        elif thema == 'Verbraucher und End-nutzer':
            unterthema_options = [
                'Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer',
                'Persönliche Sicherheit von Verbrauchern und/oder Endnutzern',
                'Soziale Inklusion von Verbrauchern und/oder Endnutzern'
            ]

        elif thema == 'Unternehmenspolitik':
            unterthema_options = [
                'Unternehmenskultur',
                'Schutz von Hinweisgebern (Whistleblowers)',
                'Tierschutz',
                'Politisches Engagement und Lobbytätigkeiten',
                'Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken',
                'Korruption und Bestechung'
            ]

        unterthema = st.selectbox('Unterthema auswählen', options=unterthema_options, index=0, key='unterthema')
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
    
def display_page():
        eigene_punkte()

        






























    









