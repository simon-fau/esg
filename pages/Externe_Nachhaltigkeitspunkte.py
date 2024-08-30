import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Constants
STATE_FILE = 'a.pkl'

# Session state management
def load_session_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_session_state(state):
    current_state = load_session_state()
    combined_state = {**current_state, **state}
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(combined_state, f)

loaded_state = load_session_state()
st.session_state.update(loaded_state)

# Ensure required session state attributes are initialized
if 'stakeholder_punkte_df' not in st.session_state:
    st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'AuswirkungRating', 'FinanzRating', 'Stakeholder Gesamtbew', 'Quelle'])

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'sidebar_companies' not in st.session_state:
    st.session_state.sidebar_companies = []

def adjust_stakeholder_punkte_filtered(new_df_copy, stakeholder_punkte_filtered):
    """Adjust the values and Stakeholder names in stakeholder_punkte_filtered based on new_df_copy for non-included stakeholders."""
    for idx, row in new_df_copy[new_df_copy['Status'] == 'nicht einbezogen'].iterrows():
        stakeholder_name = row['Stakeholder']
        thema = row['Thema']
        unterthema = row['Unterthema']
        unter_unterthema = row['Unter-Unterthema']
        
        matches = stakeholder_punkte_filtered[
            (stakeholder_punkte_filtered['Stakeholder'].str.contains(stakeholder_name)) &
            (stakeholder_punkte_filtered['Thema'] == thema) &
            (stakeholder_punkte_filtered['Unterthema'] == unterthema) &
            (stakeholder_punkte_filtered['Unter-Unterthema'] == unter_unterthema)
        ]
        
        for match_idx, match_row in matches.iterrows():
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Auswirkung'] -= row['Stakeholder Bew Auswirkung']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Finanzen'] -= row['Stakeholder Bew Finanzen']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Gesamtbew'] -= row['Stakeholder Gesamtbew']
            
            updated_stakeholders = match_row['Stakeholder'].replace(stakeholder_name, '').replace(',,', ',').strip(', ')
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder'] = updated_stakeholders

    return stakeholder_punkte_filtered

# Utility functions
def get_numerical_rating(value):
    ratings = {
        'Wesentlich': 3,
        'Eher Wesentlich': 2,
        'Eher nicht Wesentlich': 1,
        'Nicht Wesentlich': 0
    }
    return ratings.get(value, 0)

def aggregate_rankings(df):
    df['Stakeholder Bew Auswirkung'] = df['Auswirkungsbezogene Bewertung'].apply(get_numerical_rating).astype(int)
    df['Stakeholder Bew Finanzen'] = df['Finanzbezogene Bewertung'].apply(get_numerical_rating).astype(int)
    df['Stakeholder Gesamtbew'] = df['Stakeholder Bew Auswirkung'] + df['Stakeholder Bew Finanzen']
    df.fillna({'Thema': 'Unbekannt', 'Unterthema': 'Unbekannt', 'Unter-Unterthema': ''}, inplace=True)
    ranking = df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle']).agg({'Stakeholder Bew Auswirkung': 'sum', 'Stakeholder Bew Finanzen': 'sum', 'Stakeholder Gesamtbew': 'sum'}).reset_index()
    ranking.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
    ranking['Platzierung'] = ranking['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
    return ranking[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']]

def filter_stakeholders():
    if 'ranking_table' not in st.session_state or 'table2' not in st.session_state:
        return []

    valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist())
    filtered_table2 = [item for item in st.session_state.table2 if item in valid_stakeholders]

    return filtered_table2

def display_aggrid(df, with_checkboxes=False):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    if with_checkboxes:
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=True)
    gb.configure_side_bar()
    gb.configure_grid_options(domLayout='autoHeight')  # Adjusted to autoHeight for dynamic sizing
    gb.configure_default_column(flex=1, minWidth=100, resizable=True, autoHeight=True)  # Ensure columns use available space
    grid_options = gb.build()
    return AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)

def stakeholder_punkte():
    # Check if stakeholder_punkte_filtered is available in session state
    if 'stakeholder_punkte_filtered' in st.session_state:
        # Ensure it's a DataFrame
        if isinstance(st.session_state.stakeholder_punkte_filtered, pd.DataFrame):
            # Display the filtered stakeholder points using AgGrid
            
            response = display_aggrid(st.session_state.stakeholder_punkte_filtered, with_checkboxes=True)
            
            # Store the response for further processing if needed
            st.session_state.grid_response = response
            save_session_state({'grid_response': st.session_state.grid_response})
        else:
            st.error("stakeholder_punkte_filtered is not a DataFrame.")
    else:
        st.info("Keine Stakeholder-Daten zum Anzeigen verfügbar.")


def display_sidebar_items():
    with st.sidebar:
        st.markdown("---")
        st.write("**Bereits in Bewertung aufgenommen:**")
        for item in st.session_state.sidebar_companies:
            if item in st.session_state.valid_stakeholder:
                st.write(item)

def display_not_in_sidebar_count():
    filtered_table2 = filter_stakeholders()
    
    if not filtered_table2:
        st.write("Keine Stakeholder in der Bewertung aufgenommen.")
        return
    
    count = len([opt for opt in filtered_table2 if opt not in st.session_state.sidebar_companies])
    
    st.write(f"Anzahl der noch nicht in die Bewertung aufgenommenen Stakeholder: {count}")
    
    if count == 0:
        st.session_state['checkbox_state_5'] = True
    else:
        st.session_state['checkbox_state_5'] = False

def update_status(df):
    if 'table2' in st.session_state and 'ranking_table' in st.session_state:
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
        df['Status'] = df['Stakeholder'].apply(lambda x: 'einbezogen' if x in valid_stakeholders else 'nicht einbezogen')
    else:
        df['Status'] = 'nicht einbezogen'
    return df

def refresh_new_df_copy():
    if 'new_df_copy' in st.session_state and 'stakeholder_punkte_filtered' in st.session_state:
        st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
        st.session_state.stakeholder_punkte_filtered = adjust_stakeholder_punkte_filtered(
            st.session_state.new_df_copy,
            st.session_state.stakeholder_punkte_filtered
        )
        
        save_session_state({'new_df_copy': st.session_state.new_df_copy,
                            'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

def remove_invalid_stakeholders():
    if 'table2' in st.session_state and 'ranking_table' in st.session_state:
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
        st.session_state.sidebar_companies = [item for item in st.session_state.sidebar_companies if item in valid_stakeholders]
        save_session_state({'sidebar_companies': st.session_state.sidebar_companies})
        refresh_new_df_copy()

def excel_upload():
    uploaded_file = st.file_uploader("Excel-Datei hochladen", type=['xlsx'])
    
    if uploaded_file:
        df_list = []
        for sheet_name in ['Top-Down', 'Intern', 'Extern']:
            try:
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl', usecols=['Thema', 'Unterthema', 'Unter-Unterthema', 'Auswirkungsbezogene Bewertung', 'Finanzbezogene Bewertung'])
                df['Quelle'] = sheet_name
                df_list.append(df)
            except ValueError:
                st.info(f"Blatt '{sheet_name}' nicht in {uploaded_file.name} gefunden.")
        
        if df_list:
            combined_df = pd.concat(df_list, ignore_index=True)
            st.session_state.ranking_df = aggregate_rankings(combined_df)
            save_session_state({'ranking_df': st.session_state.ranking_df})
            
            st.write("Vorschau der hochgeladenen Daten:")
            response = display_aggrid(st.session_state.ranking_df, with_checkboxes=False)
            st.session_state.grid_response = response
            save_session_state({'grid_response': st.session_state.grid_response})

            if 'table2' not in st.session_state:
                st.session_state.table2 = []

            valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
            options = [opt for opt in valid_stakeholders if opt not in st.session_state.sidebar_companies]

            selected_option = st.selectbox('Wählen Sie den zugehörigen Stakeholder aus:', options)
            st.session_state.selected_option = selected_option
            save_session_state({'selected_option': st.session_state.selected_option})

            if st.button('Punkte übernehmen'):
                if st.session_state.selected_option:
                    st.session_state.sidebar_companies.append(st.session_state.selected_option)
                    save_session_state({'sidebar_companies': st.session_state.sidebar_companies})

                    relevant_columns = ['Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']
                    new_df = st.session_state.ranking_df[relevant_columns]
                    new_df = new_df[new_df['Stakeholder Gesamtbew'] >= 1]
                    
                    new_df['Stakeholder'] = st.session_state.selected_option
                    
                    if 'new_df_copy' not in st.session_state:
                        st.session_state.new_df_copy = new_df.copy()
                    else:
                        st.session_state.new_df_copy = pd.concat([st.session_state.new_df_copy, new_df], ignore_index=True)
                    
                    st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
                    save_session_state({'new_df_copy': st.session_state.new_df_copy})

                    if not st.session_state.stakeholder_punkte_df.empty:
                        merged_df = pd.merge(
                            st.session_state.stakeholder_punkte_df, new_df, 
                            on=['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle'], how='outer', suffixes=('_x', '_y')
                        )

                        merged_df['Stakeholder Bew Auswirkung'] = merged_df['Stakeholder Bew Auswirkung_x'].add(merged_df['Stakeholder Bew Auswirkung_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Bew Finanzen'] = merged_df['Stakeholder Bew Finanzen_x'].add(merged_df['Stakeholder Bew Finanzen_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Gesamtbew'] = merged_df['Stakeholder Gesamtbew_x'].add(merged_df['Stakeholder Gesamtbew_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder'] = merged_df.apply(lambda row: ', '.join(filter(None, [row.get('Stakeholder_x', ''), row.get('Stakeholder_y', '')])), axis=1)
                        merged_df.drop(columns=['Stakeholder Bew Auswirkung_x', 'Stakeholder Bew Auswirkung_y', 'Stakeholder Bew Finanzen_x', 'Stakeholder Bew Finanzen_y', 'Stakeholder Gesamtbew_x', 'Stakeholder Gesamtbew_y', 'Stakeholder_x', 'Stakeholder_y'], inplace=True)
                        st.session_state.stakeholder_punkte_df = merged_df
                    else:
                        st.session_state.stakeholder_punkte_df = new_df

                    st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
                    st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
                    save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})

                    st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_df
                    save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

                    st.success("Stakeholder Punkte erfolgreich übernommen")

                    st.session_state.uploaded_file = None
                    save_session_state({'uploaded_file': st.session_state.uploaded_file})
                    st.experimental_rerun()
                else:
                    if not options:
                        st.info("Punkte können nicht übernommen werden. Bitte fügen Sie den entsprechenden Stakeholder unter hinzu und/oder nehmen sie diesen explizit in die Bewertung auf.")
                    else:
                        st.success("Stakeholder Punkte erfolgreich übernommen")
    
    if 'new_df_copy' in st.session_state:
        refresh_new_df_copy()
        st.write("Kopie von neuen Daten:")
        st.dataframe(st.session_state.new_df_copy)

def display_sidebar_items():
    remove_invalid_stakeholders()
    
    with st.sidebar:
        st.markdown("---")
        st.write("**Bereits in Bewertung aufgenommen:**")
        for item in st.session_state.sidebar_companies:
            st.write(item)

def display_page():
    refresh_new_df_copy()
    
    st.write(st.session_state.ranking_table)
    st.write(st.session_state.table2)
    st.write(st.session_state.sidebar_companies)
    
    if 'stakeholder_punkte_filtered' not in st.session_state:
        st.session_state.stakeholder_punkte_filtered = []
    
    st.write(st.session_state.stakeholder_punkte_filtered)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Stakeholder-Management") 
    with col2:
        container = st.container(border=True)
        with container:
            display_not_in_sidebar_count()
    st.markdown("""
        Dieses Tool hilft Ihnen, Ihre Stakeholder effektiv zu verwalten und zu analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.
    """)
    
    tab1, tab2 = st.tabs(["Auswahl", "Ranking der Stakeholderbewertung"])
    with tab1:
        excel_upload()
        display_sidebar_items()
        
    with tab2:
        stakeholder_punkte()
