import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def stakeholder_punkte():
    if 'df3' not in st.session_state:
        st.session_state.df3 = pd.DataFrame({
            "Thema": [""] * 5,
            "Unterthema": [""] * 5,
            "Unter-Unterthema": [""] * 5
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen',
        options=[
            'Klimawandel', 
            'Umweltverschmutzung', 
            'Wasser- und Meeresressourcen', 
            'Biologische Vielfalt und Ökosysteme', 
            'Kreislaufwirtschaft'], 
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
        elif thema == 'EIgene Belegschaft':
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

        unterthema = st.selectbox('Unterthema auswählen', options=unterthema_options, index=0, key='unterthema1')
        unter_unterthema = st.text_input('Unter-Unterthema eingeben', key='unter_unterthema1')    
        add_row = st.button('Hinzufügen', key='add_row1')

        if add_row:
            empty_row_index = st.session_state.df3[(st.session_state.df3["Thema"] == "") & (st.session_state.df3["Unterthema"] == "") & (st.session_state.df3["Unter-Unterthema"] == "")].first_valid_index()
            if empty_row_index is not None:
                st.session_state.df3.at[empty_row_index, "Thema"] = thema
                st.session_state.df3.at[empty_row_index, "Unterthema"] = unterthema
                st.session_state.df3.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
            else:
                new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
                st.session_state.df3 = st.session_state.df3._append(new_row, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df3)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    grid_response = AgGrid(
        st.session_state.df3.reset_index(),
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
        st.session_state.df3 = st.session_state.df3._append(empty_row, ignore_index=True)
        st.experimental_rerun()

    delete_rows = st.button('Ausgewählte Zeilen löschen', key='delete_rows')
    if delete_rows:
        selected_rows = grid_response['selected_rows']
        selected_indices = [row['index'] for row in selected_rows]
        st.session_state.df3 = st.session_state.df3.drop(selected_indices)
        st.experimental_rerun()

    save_changes = st.button('Änderungen speichern', key='save_changes')
    if save_changes:
        st.session_state.df3 = grid_response['data'].set_index('index')
        
def excel_upload():   
    
    # Funktion, um die Hierarchie zu füllen, falls höhere Ebenen leer sind
    def fill_hierarchy(row):
        if pd.isna(row['Unter-Unterthema']):
            if pd.isna(row['Unterthema']):
                return row['Thema']
            else:
                return row['Unterthema']
        return row['Unter-Unterthema']

    def get_numerical_rating(value):
        ratings = {
            'Wesentlich': 3,
            'Eher Wesentlich': 2,
            'Eher nicht Wesentlich': 1,
            'Nicht Wesentlich': 0
        }
        return ratings.get(value, 0)

    def aggregate_rankings(aggregate_df4):
        aggregate_df4['Hierarchie'] = aggregate_df4.apply(fill_hierarchy, axis=1)
        aggregate_df4['NumericalRating'] = aggregate_df4['Bewertung'].apply(get_numerical_rating)
        ranking = aggregate_df4.groupby(['Hierarchie'], as_index=False)['NumericalRating'].sum()
        return ranking.sort_values(by='NumericalRating', ascending=False)

    # Funktion, um neue Bewertungen zu den bestehenden hinzuzufügen
    def update_rankings(new_df4):
        if 'ranking_df4' not in st.session_state or st.session_state.ranking_df4.empty:
            st.session_state.ranking_df4 = new_df4.copy()
        else:
            st.session_state.ranking_df4 = pd.concat([st.session_state.ranking_df4, new_df4])
            st.session_state.ranking_df4 = aggregate_rankings(st.session_state.ranking_df4)

    uploaded_files = st.file_uploader("Excel-Dateien hochladen", accept_multiple_files=True, type=['xlsx'])
    df4_list = []

    for uploaded_file in uploaded_files:
        if uploaded_file:
            df4 = pd.read_excel(uploaded_file, engine='openpyxl')
            df4_list.append(df4)

    if st.button('Ranking erstellen'):
        if df4_list:
            combined_df4 = pd.concat(df4_list)
            update_rankings(combined_df4)
            st.write("Aktuelles Ranking basierend auf hochgeladenen Dateien:")
            st.dataframe(st.session_state.ranking_df4)
        else:
            st.error("Bittee laden Sie mindestens eine Excel-Datei hoch.")

def display_page():
    col1, col2 = st.columns([2 , 1])
    with col1:
        stakeholder_punkte()
    with col2:
        excel_upload()