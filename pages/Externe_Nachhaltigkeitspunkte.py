import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Constants
STATE_FILE = 'a.pkl'
OPTIONS = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']

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
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = OPTIONS[0]

if 'stakeholder_punkte_df' not in st.session_state:
    st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating', 'Quelle'])

# Utility functions
def calculate_class_size(df):
    return (df['NumericalRating'].max() - df['NumericalRating'].min()) / 4

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

def calculate_selected_rows(df, class_size):
    slider_value = st.session_state.slider_value
    if slider_value == 'Wesentlich':
        return df[df['NumericalRating'] > 3 * class_size + df['NumericalRating'].min()]
    elif slider_value == 'Eher Wesentlich':
        return df[df['NumericalRating'] > 2 * class_size + df['NumericalRating'].min()]
    elif slider_value == 'Eher nicht wesentlich':
        return df[df['NumericalRating'] > class_size + df['NumericalRating'].min()]
    else:
        return df[df['NumericalRating'] > 0]

def extract_company_name(file):
    try:
        df = pd.read_excel(file, sheet_name='Einführung', engine='openpyxl', usecols="B")
        if df.shape[0] > 10:
            return df.iloc[10, 0]
        st.warning(f"Firmennamen in {file.name} nicht gefunden oder außerhalb des zulässigen Bereichs.")
    except Exception as e:
        st.error(f"Fehler beim Extrahieren des Firmennamens: {e}")
    return None

# UI components
def add_slider():
    with st.expander("**Grenzwert der Stakeholderpunkte:**", expanded=False):
    
        col1, col2 = st.columns([1, 4])
        with col1:
            current_slider_value = st.select_slider('', options=OPTIONS, value=st.session_state.slider_value, key='stakeholder_zslider')
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

def display_aggrid(df, with_checkboxes=False):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    if with_checkboxes:
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=True)
    gb.configure_side_bar()
    gb.configure_grid_options(domLayout='autoHeight')  # Adjusted to autoHeight for dynamic sizing
    gb.configure_default_column(flex=1, minWidth=100, resizable=True, autoHeight=True)  # Ensure columns use available space
    
    # Set specific width for "Platzierung" and "Numerical Rating" columns
    gb.configure_column('Platzierung', width=30)  # Adjust width as needed
    gb.configure_column('NumericalRating', width=80)  # Adjust width as needed
    
    grid_options = gb.build()
    return AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)

def stakeholder_punkte():
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered

    if not stakeholder_punkte_filtered.empty:
        stakeholder_punkte_filtered.reset_index(inplace=True)
        stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)
        grid_response = display_aggrid(stakeholder_punkte_filtered.drop(columns=['_index']), with_checkboxes=True)
        selected = grid_response['selected_rows']

        
        if st.button("🗑️ Inhalt löschen"):
            if selected:
                selected_indices = [stakeholder_punkte_filtered.iloc[row['_selectedRowNodeInfo']['nodeRowIndex']]['_index'] for row in selected]
                st.session_state.stakeholder_punkte_df.drop(selected_indices, inplace=True)
                save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})
                st.experimental_rerun()
            else:
                st.warning("Keine Zeilen ausgewählt.")
    
        if st.button("🗑️ Alle Inhalte löschen"):
            st.session_state.stakeholder_punkte_df = st.session_state.stakeholder_punkte_df.iloc[0:0]
            if 'company_names' in st.session_state:
                del st.session_state['company_names']
            save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df, 'company_names': pd.DataFrame()})
            st.experimental_rerun()
    else:
        st.warning("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")

def excel_upload():
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
            st.write("")
            st.write("")
            st.write("Vorschau der hochgeladenen Daten:")
            response = display_aggrid(st.session_state.ranking_df, with_checkboxes=False)
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

                if company_names:
                    company_names_df = pd.DataFrame(company_names.items(), columns=["File Name", "Company Name"])
                    if 'company_names' in st.session_state:
                        st.session_state.company_names = pd.concat([st.session_state.company_names, company_names_df], ignore_index=True)
                    else:
                        st.session_state.company_names = company_names_df
                    save_session_state({'company_names': st.session_state.company_names})

def display_sidebar():
    if 'company_names' in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Bereits hochgeladene Dateien von:**")
        for index, row in st.session_state.company_names.iterrows():
            st.sidebar.markdown(f"- {row['Company Name']}")
    
def display_page():
    st.header("Stakeholder-Management")
    st.markdown("""
        Dieses Tool hilft Ihnen, Ihre Stakeholder effektiv zu verwalten und zu analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.
    """)
    
    tab1, tab2 = st.tabs(["Auswahl", "Ranking der Stakeholderbewertung"])
    with tab1:
        excel_upload()
        display_sidebar()
    with tab2:
        add_slider()
        stakeholder_punkte()