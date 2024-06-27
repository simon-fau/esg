import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Datei zum Speichern des Sitzungszustands
state_file = 'session_state_bottom_up_stakeholder.pkl'

# Funktion zum Laden des Sitzungszustands
def load_session_state():
    if os.path.exists(state_file):
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

# Funktion zum Speichern des Sitzungszustands
def save_session_state(state):
    # Laden des aktuellen Zustands
    current_state = load_session_state()
    # Hinzufügen des neuen Zustands zum aktuellen Zustand
    combined_state = {**current_state, **state}
    # Speichern des kombinierten Zustands
    with open(state_file, 'wb') as f:
        pickle.dump(combined_state, f)

# Laden des Sitzungszustands aus der Datei
loaded_state = load_session_state()
st.session_state.update(loaded_state)

def calculate_class_size(df):
    # Berechne die Größe der Klassen
    return (df['NumericalRating'].max() - df['NumericalRating'].min()) / 4

# Initialize 'slider_value' in st.session_state if it doesn't exist
options = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = options[0]

# Initialize 'stakeholder_punkte_df' in st.session_state if it doesn't exist
if 'stakeholder_punkte_df' not in st.session_state:
    st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating', 'Quelle'])

def add_slider():
    st.write("**Grenzwert der Stakeholderpunkte:**")
    col1, col2 = st.columns([1, 4])
    with col1:
        # Speichere den aktuellen Zustand des Schiebereglers in der Sidebar mit einem eindeutigen Schlüssel
        current_slider_value = st.select_slider('', options=options, value=st.session_state.slider_value, key='stakeholder_zslider')
   
        # Aktualisiere 'slider_value' im session_state bei Button-Klick in der Sidebar
        if st.button('Auswahl übernehmen'):
            st.session_state.slider_value = current_slider_value
            save_session_state({'slider_value': st.session_state.slider_value})
            st.experimental_rerun()
            
        st.sidebar.markdown("""
            <style>
            .st-emotion-cache-183lzff,
            .st-emotion-cache-1inwz65 {
                font-family: "Source Sans Pro", sans-serif;
            }
            </style>
            """, unsafe_allow_html=True)
    
    with col2:
        pass

def calculate_selected_rows(df, class_size):
    # Berechne die Anzahl der ausgewählten Zeilen basierend auf der Auswahl
    if st.session_state.slider_value == 'Wesentlich':
        return df[df['NumericalRating'] > 3 * class_size + df['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher Wesentlich':
        return df[df['NumericalRating'] > 2 * class_size + df['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher nicht wesentlich':
        return df[df['NumericalRating'] > class_size + df['NumericalRating'].min()]
    else:  # Nicht Wesentlich
        return df[df['NumericalRating'] > 0]


def stakeholder_punkte():
    # Berechne die Größe der Klassen
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)

    # Berechne die ausgewählten Zeilen basierend auf der Auswahl im Schieberegler
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)

    # Speichere die ausgewählten Zeilen im session_state
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered

    if 'stakeholder_punkte_filtered' in st.session_state and not st.session_state.stakeholder_punkte_filtered.empty:
        # Reset index to ensure it is accessible but not displayed in AgGrid
        st.session_state.stakeholder_punkte_filtered.reset_index(inplace=True)
        
        # Move the index to a new column '_index' for internal use
        st.session_state.stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)
        
        # Konfiguration der AgGrid
        gb = GridOptionsBuilder.from_dataframe(st.session_state.stakeholder_punkte_filtered.drop(columns=['_index']))
        gb.configure_pagination(paginationAutoPageSize=True, paginationPageSize=10)
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=True)
        gb.configure_side_bar()
        grid_options = gb.build()

        # Anzeige der AgGrid
        grid_response = AgGrid(
            st.session_state.stakeholder_punkte_filtered.drop(columns=['_index']),
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED
        )

        selected = grid_response['selected_rows']

        if st.button("Inhalt löschen"):
            if selected:
                # Extracting the indices of the selected rows using the internal '_index' column
                selected_indices = [st.session_state.stakeholder_punkte_filtered.iloc[row['_selectedRowNodeInfo']['nodeRowIndex']]['_index'] for row in selected]
                # Dropping the selected rows from the original DataFrame
                st.session_state.stakeholder_punkte_df.drop(selected_indices, inplace=True)
                st.session_state.stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
                save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})
                st.experimental_rerun()
            else:
                st.warning("Keine Zeilen ausgewählt.")
    else:
        st.warning("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")



def extract_company_name(file):
    # Extrahiere den Firmennamen aus der 'Einführung' Tabelle, Zelle B7
    try:
        df = pd.read_excel(file, sheet_name='Einführung', engine='openpyxl', usecols="B")
        if df.shape[0] > 6:
            company_name = df.iloc[6, 0]
            return company_name
        else:
            st.warning(f"Firmennamen in {file.name} nicht gefunden oder außerhalb des zulässigen Bereichs.")
            return None
    except Exception as e:
        st.error(f"Fehler beim Extrahieren des Firmennamens: {e}")
        return None

def excel_upload():
    def get_numerical_rating(value):
        ratings = {
            'Wesentlich': 3,
            'Eher Wesentlich': 2,
            'Eher nicht Wesentlich': 1,
            'Nicht Wesentlich': 0
        }
        return ratings.get(value, 0)

    def aggregate_rankings(df):
        df['NumericalRating'] = df['Bewertung'].apply(get_numerical_rating).astype(int)
        df.fillna({'Thema': 'Unbekannt', 'Unterthema': 'Unbekannt', 'Unter-Unterthema': ''}, inplace=True)
        ranking = df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle']).agg({'NumericalRating': 'sum'}).reset_index()
        ranking.sort_values(by='NumericalRating', ascending=False, inplace=True)
        ranking['Platzierung'] = ranking['NumericalRating'].rank(method='min', ascending=False).astype(int)
        return ranking[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating', 'Quelle']]

    uploaded_files = st.file_uploader("Excel-Dateien hochladen", accept_multiple_files=True, type=['xlsx'])
    if uploaded_files:
        df_list = []
        company_names = {}
        for file in uploaded_files:
            company_name = extract_company_name(file)
            if company_name:
                company_names[file.name] = company_name
            for sheet_name in ['Top-Down', 'Intern', 'Extern']:
                try:
                    df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl', usecols=['Thema', 'Unterthema', 'Unter-Unterthema', 'Bewertung'])
                    df['Quelle'] = company_name if sheet_name == 'Extern' else sheet_name
                    df_list.append(df)
                except ValueError:
                    st.warning(f"Blatt '{sheet_name}' nicht in {file.name} gefunden.")
        if df_list:
            combined_df = pd.concat(df_list, ignore_index=True)
            st.session_state.ranking_df = aggregate_rankings(combined_df)
            save_session_state({'ranking_df': st.session_state.ranking_df})
            st.write("Aktuelles Ranking basierend auf hochgeladenen Dateien:")
            gb = GridOptionsBuilder.from_dataframe(st.session_state.ranking_df)
            gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
            gb.configure_side_bar()
            grid_options = gb.build()
            grid_options['defaultColDef'] = {'flex': 1}
            response = AgGrid(st.session_state.ranking_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)
            st.session_state.grid_response = response
            save_session_state({'grid_response': st.session_state.grid_response})

            if st.button('Stakeholder Punkte übernehmen'):
                relevant_columns = ['Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating', 'Quelle']
                new_df = st.session_state.ranking_df[relevant_columns]
                new_df = new_df[new_df['NumericalRating'] >= 1]

                if 'stakeholder_punkte_df' in st.session_state:
                    st.session_state.stakeholder_punkte_df = pd.merge(
                        st.session_state.stakeholder_punkte_df, new_df, 
                        on=['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle'], how='outer'
                    )
                    st.session_state.stakeholder_punkte_df['NumericalRating'] = st.session_state.stakeholder_punkte_df['NumericalRating_x'].add(
                        st.session_state.stakeholder_punkte_df['NumericalRating_y'], fill_value=0
                    ).astype(int)
                    st.session_state.stakeholder_punkte_df.drop(columns=['NumericalRating_x', 'NumericalRating_y'], inplace=True)
                else:
                    st.session_state.stakeholder_punkte_df = new_df

                st.session_state.stakeholder_punkte_df.sort_values(by='NumericalRating', ascending=False, inplace=True)
                st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['NumericalRating'].rank(method='min', ascending=False).astype(int)
               
                save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})
                st.success("Stakeholder Punkte erfolgreich übernommen")

                # Extract company names and update the session state
                if company_names:
                    company_names_df = pd.DataFrame(company_names.items(), columns=["File Name", "Company Name"])
                    if 'company_names' in st.session_state:
                        st.session_state.company_names = pd.concat([st.session_state.company_names, company_names_df], ignore_index=True)
                    else:
                        st.session_state.company_names = company_names_df
                    save_session_state({'company_names': st.session_state.company_names})

def display_page():
    st.header("Stakeholder-Management")
    st.markdown("""
        Dieses Tool hilft Ihnen, Ihre Stakeholder effektiv zu verwalten und zu analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.
    """)
    
    tab1, tab2 = st.tabs(["Auswahl", "Stakeholder Nachhaltigkeitspunkte"])
    with tab1:
        excel_upload()
        if 'company_names' in st.session_state:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**Bereits hochgeladene Dateien von:**")
            for index, row in st.session_state.company_names.iterrows():
                st.sidebar.markdown(f"- {row['Company Name']}")
        else:
            st.sidebar.warning("Es wurden noch keine Unternehmensnamen extrahiert.")
    with tab2:
        add_slider()
        stakeholder_punkte()


