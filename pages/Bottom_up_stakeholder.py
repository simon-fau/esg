import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def stakeholder_punkte():
    if 'stakeholder_punkte_df' in st.session_state:
        # Sortieren Sie den DataFrame nach 'NumericalRating' in absteigender Reihenfolge
        st.session_state.stakeholder_punkte_df.sort_values('NumericalRating', ascending=False, inplace=True)
        # Fügen Sie eine neue Spalte 'Platzierung' hinzu, die die Platzierung basierend auf 'NumericalRating' angibt
        st.session_state.stakeholder_punkte_df['Platzierung'] = range(1, len(st.session_state.stakeholder_punkte_df) + 1)
        gb = GridOptionsBuilder.from_dataframe(st.session_state.stakeholder_punkte_df)
        gb.configure_pagination(paginationAutoPageSize=True, paginationPageSize=10)
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=True)
        gb.configure_side_bar()
        grid_options = gb.build()
        AgGrid(st.session_state.stakeholder_punkte_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)
    else:
        st.write("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")

# Fügen Sie einen Schieberegler in der Seitenleiste hinzu
    percentage = st.sidebar.slider('Auswahl in Prozent', 0, 100, 0)
    if st.sidebar.button('In Bewertung übernehmen'):
        # Berechnen Sie die Anzahl der ausgewählten Zeilen basierend auf dem Prozentsatz
        num_rows = int(len(st.session_state.stakeholder_punkte_df) * (percentage / 100))
        # Wählen Sie die entsprechende Anzahl von Zeilen mit dem höchsten 'NumericalRating' aus
        selected_rows = st.session_state.stakeholder_punkte_df.nlargest(num_rows, 'NumericalRating')
        # Speichern Sie die ausgewählten Zeilen im session_state
        st.session_state.selected_rows = selected_rows
        st.experimental_rerun()

def excel_upload():
    """ Diese Funktion lädt Excel-Dateien hoch und erstellt Rankings basierend auf den Bewertungen. """
    def get_numerical_rating(value):
        ratings = {
            'Wesentlich': 3,
            'Eher Wesentlich': 2,
            'Eher nicht Wesentlich': 1,
            'Nicht Wesentlich': 0
        }
        return ratings.get(value, 0)

    def aggregate_rankings(df):
        """ Erzeugt eine aggregierte Rangliste basierend auf den Bewertungen. """
        df['NumericalRating'] = df['Bewertung'].apply(get_numerical_rating)
        df.fillna({'Thema': 'Unbekannt', 'Unterthema': 'Unbekannt', 'Unter-Unterthema': ''}, inplace=True)
        ranking = df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema']).agg({'NumericalRating': 'sum'}).reset_index()
        ranking.sort_values(by='NumericalRating', ascending=False, inplace=True)
        ranking['Platzierung'] = ranking['NumericalRating'].rank(method='min', ascending=False).astype(int)
        return ranking[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating']]

    uploaded_files = st.file_uploader("Excel-Dateien hochladen", accept_multiple_files=True, type=['xlsx'])
    if uploaded_files:
        df_list = [pd.read_excel(file, sheet_name=1, engine='openpyxl') for file in uploaded_files if file]
        combined_df = pd.concat(df_list)
        st.session_state.ranking_df = aggregate_rankings(combined_df)
        st.write("Aktuelles Ranking basierend auf hochgeladenen Dateien:")
        gb = GridOptionsBuilder.from_dataframe(st.session_state.ranking_df)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
        gb.configure_side_bar()
        grid_options = gb.build()
        grid_options['defaultColDef'] = {'flex': 1}
        response = AgGrid(st.session_state.ranking_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)
        st.session_state.grid_response = response
    
        if st.button('Stakeholder Punkte übernehmen'):
            # Filtern Sie die Daten, um nur relevante Spalten zu behalten
            relevant_columns = ['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating']
            new_df = st.session_state.ranking_df[relevant_columns]
            # Filtern Sie die Zeilen, um nur diejenigen zu behalten, deren 'NumericalRating' größer oder gleich 1 ist
            new_df = new_df[new_df['NumericalRating'] >= 1]
            st.session_state.uploaded_files_names = [file.name for file in uploaded_files]
            if 'stakeholder_punkte_df' in st.session_state:
                # Merge the new dataframe with the existing one, adding the NumericalRating of identical entries
                st.session_state.stakeholder_punkte_df = pd.merge(st.session_state.stakeholder_punkte_df, new_df, on=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema'], how='outer')
                st.session_state.stakeholder_punkte_df['NumericalRating'] = st.session_state.stakeholder_punkte_df['NumericalRating_x'].add(st.session_state.stakeholder_punkte_df['NumericalRating_y'], fill_value=0)
                st.session_state.stakeholder_punkte_df.drop(columns=['NumericalRating_x', 'NumericalRating_y'], inplace=True)
            else:
                st.session_state.stakeholder_punkte_df = new_df
    
            st.experimental_rerun()

        
def display_page():          
    tab1, tab2 = st.tabs(["Auswahl", "Stakeholder Nachhaltigkeitspunkte"])
    with tab1:
        excel_upload()
    with tab2:
        stakeholder_punkte()