import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Constants
STATE_FILE = 'a.pkl'
OPTIONS = ['Alle', 'Top 75%', 'Top 50%', 'Top 25%']

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

if 'stakeholder_values' not in st.session_state:
    st.session_state.stakeholder_values = {}

# Ensure required session state attributes are initialized
if 'slider_value' not in st.session_state:
    st.session_state.slider_value = OPTIONS[0]

if 'stakeholder_punkte_df' not in st.session_state:
    st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'AuswirkungRating', 'FinanzRating', 'Stakeholder Gesamtbew', 'Quelle', 'Stakeholder'])

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'sidebar_companies' not in st.session_state:
    st.session_state.sidebar_companies = []

if 'table2' not in st.session_state:
    st.session_state.table2 = []

# Utility functions
def calculate_class_size(df):
    return (df['Stakeholder Gesamtbew'].max() - df['Stakeholder Gesamtbew'].min()) / 4

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
    # No aggregation, keep individual stakeholder rows
    ranking = df.sort_values(by='Stakeholder Gesamtbew', ascending=False).reset_index(drop=True)
    ranking['Platzierung'] = ranking['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
    return ranking[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']]

def calculate_selected_rows(df, class_size):
    slider_value = st.session_state.slider_value
    if slider_value == 'Top 25%':
        return df[df['Stakeholder Gesamtbew'] > 3 * class_size + df['Stakeholder Gesamtbew'].min()]
    elif slider_value == 'Top 50%':
        return df[df['Stakeholder Gesamtbew'] > 2 * class_size + df['Stakeholder Gesamtbew'].min()]
    elif slider_value == 'Top 75%':
        return df[df['Stakeholder Gesamtbew'] > class_size + df['Stakeholder Gesamtbew'].min()]
    else:
        return df[df['Stakeholder Gesamtbew'] > 0]

def filter_stakeholders():
    if 'ranking_table' not in st.session_state or 'table2' not in st.session_state:
        return []
    valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist())
    filtered_table2 = [item for item in st.session_state.table2 if item in valid_stakeholders]
    return filtered_table2

def filter_sidebar_companies():
    if 'ranking_table' in st.session_state and 'table2' in st.session_state:
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist())
        valid_sidebar_companies = [item for item in st.session_state.sidebar_companies if item in st.session_state.table2 and item in valid_stakeholders]
        st.session_state.sidebar_companies = valid_sidebar_companies

def remove_stakeholders_not_in_sidebar():
    if not st.session_state.stakeholder_punkte_df.empty:
        valid_sidebar = set(st.session_state.sidebar_companies)
        st.session_state.stakeholder_punkte_df['Stakeholder'] = st.session_state.stakeholder_punkte_df['Stakeholder'].apply(lambda x: ', '.join([item for item in x.split(', ') if item in valid_sidebar]))
        st.session_state.stakeholder_punkte_df = st.session_state.stakeholder_punkte_df[st.session_state.stakeholder_punkte_df['Stakeholder'] != '']
        st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
        st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
        save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})

def remove_from_stakeholder_punkte(removed_stakeholder):
    if not st.session_state.stakeholder_punkte_df.empty:
        # Check if the stakeholder exists in the stakeholder_values dictionary
        if removed_stakeholder in st.session_state.stakeholder_values:
            stakeholder_values_list = st.session_state.stakeholder_values.pop(removed_stakeholder)
            for stakeholder_values in stakeholder_values_list:
                print(f"Removing values for stakeholder: {removed_stakeholder}")
                print(f"Values to remove: {stakeholder_values}")
                for idx, row in st.session_state.stakeholder_punkte_df.iterrows():
                    print(f"Matching row: {row[['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle']].to_dict()}")
                    # Match the rows based on Thema, Unterthema, Unter-Unterthema, and Quelle
                    if (row['Thema'] == stakeholder_values['Thema'] and
                        row['Unterthema'] == stakeholder_values['Unterthema'] and
                        row['Unter-Unterthema'] == stakeholder_values['Unter-Unterthema'] and
                        row['Quelle'] == stakeholder_values['Quelle']):
                        
                        print("Match found. Subtracting values.")
                        # Subtract the stakeholder's values from the DataFrame
                        st.session_state.stakeholder_punkte_df.at[idx, 'Stakeholder Bew Auswirkung'] = max(0, row['Stakeholder Bew Auswirkung'] - stakeholder_values['Stakeholder Bew Auswirkung'])
                        st.session_state.stakeholder_punkte_df.at[idx, 'Stakeholder Bew Finanzen'] = max(0, row['Stakeholder Bew Finanzen'] - stakeholder_values['Stakeholder Bew Finanzen'])
                        st.session_state.stakeholder_punkte_df.at[idx, 'Stakeholder Gesamtbew'] = max(0, row['Stakeholder Gesamtbew'] - stakeholder_values['Stakeholder Gesamtbew'])
                        
                        # Remove the stakeholder from the Stakeholder column
                        new_stakeholders = ', '.join([s for s in row['Stakeholder'].split(', ') if s != removed_stakeholder])
                        st.session_state.stakeholder_punkte_df.at[idx, 'Stakeholder'] = new_stakeholders
                    else:
                        print("No match found for this row.")
                        
            # Remove rows where all values are zero or no stakeholder is left
            st.session_state.stakeholder_punkte_df = st.session_state.stakeholder_punkte_df[
                (st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'] > 0) &
                (st.session_state.stakeholder_punkte_df['Stakeholder'] != '')
            ]
            
            # Recalculate ranking after removal
            st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
            st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
            
            # Save the updated session state
            save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})

    # Also remove the stakeholder from the sidebar and table2
    if removed_stakeholder in st.session_state.sidebar_companies:
        st.session_state.sidebar_companies.remove(removed_stakeholder)
    if removed_stakeholder in st.session_state.table2:
        st.session_state.table2.remove(removed_stakeholder)

    save_session_state({'sidebar_companies': st.session_state.sidebar_companies, 'table2': st.session_state.table2})



    # Also remove the stakeholder from the sidebar and table2
    if removed_stakeholder in st.session_state.sidebar_companies:
        st.session_state.sidebar_companies.remove(removed_stakeholder)
    if removed_stakeholder in st.session_state.table2:
        st.session_state.table2.remove(removed_stakeholder)

    save_session_state({'sidebar_companies': st.session_state.sidebar_companies, 'table2': st.session_state.table2})



# UI components
def add_slider():
    with st.expander("**Grenzwert der Stakeholderpunkte:**", expanded=False):
        col1, col2 = st.columns([1, 4])
        with col1:
            current_slider_value = st.select_slider('', options=OPTIONS, value=st.session_state.slider_value, key='stakeholder_slider')
            if st.button('Auswahl übernehmen'):
                st.session_state.slider_value = current_slider_value
                save_session_state({'slider_value': st.session_state.slider_value})
                st.experimental_rerun()

def display_aggrid(df, with_checkboxes=False):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)
    if with_checkboxes:
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=True)
    gb.configure_side_bar()
    gb.configure_grid_options(domLayout='autoHeight')  
    gb.configure_default_column(flex=1, minWidth=100, resizable=True, autoHeight=True)  
    grid_options = gb.build()
    return AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)

def stakeholder_punkte():
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered
    if not stakeholder_punkte_filtered.empty:
        stakeholder_punkte_filtered.reset_index(inplace=True)
        stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)
        stakeholder_punkte_filtered = stakeholder_punkte_filtered[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle', 'Stakeholder']]
        grid_response = display_aggrid(stakeholder_punkte_filtered, with_checkboxes=True)
        selected = grid_response['selected_rows']
        if st.button("🗑️ Inhalt löschen"):
            if selected:
                selected_indices = [stakeholder_punkte_filtered.iloc[row['_selectedRowNodeInfo']['nodeRowIndex']]['_index'] for row in selected]
                st.session_state.stakeholder_punkte_df.drop(selected_indices, inplace=True)
                save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})
                st.experimental_rerun()
            else:
                st.info("Keine Zeilen ausgewählt.")
        if st.button("🗑️ Alle Inhalte löschen"):
            st.session_state.stakeholder_punkte_df = st.session_state.stakeholder_punkte_df.iloc[0:0]
            st.session_state.sidebar_companies = []
            save_session_state({
                'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df,
                'sidebar_companies': st.session_state.sidebar_companies
            })
            st.experimental_rerun()
    else:
        st.info("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")

def remove_from_table2(selected_items):
    for item in selected_items:
        if item in st.session_state.table2:
            st.session_state.table2.remove(item)
            st.session_state.table1.append(item)
            remove_from_stakeholder_punkte(item)  

def remove_button_selection():
    selected_table2 = st.multiselect(
        "Wählen Sie Stakeholder zum Entfernen aus:",
        st.session_state.table2,
        key="select_table2"
    )
    if st.button("<<< Entfernen"):
        remove_from_table2(selected_table2)
        st.experimental_rerun()

def display_sidebar_items():
    filter_sidebar_companies()
    with st.sidebar:
        st.markdown("---")
        st.write("**Bereits in Bewertung aufgenommen:**")
        for item in st.session_state.sidebar_companies:
            st.write(item)
    remove_stakeholders_not_in_sidebar()

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
            options = [opt for opt in st.session_state.table2 if opt not in st.session_state.sidebar_companies]
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
                    # Iterate over each row in the DataFrame
                    for idx, row in new_df.iterrows():
                        if row['Stakeholder Gesamtbew'] >= 1:  # Only process rows with "Stakeholder Gesamtbew" >= 1
                            key = st.session_state.selected_option
                            
                            # Ensure 'st.session_state.stakeholder_values[key]' is a list
                            if key not in st.session_state.stakeholder_values or not isinstance(st.session_state.stakeholder_values[key], list):
                                st.session_state.stakeholder_values[key] = []

                            # Append values to the list
                            st.session_state.stakeholder_values[key].append({
                                'Thema': row['Thema'],
                                'Unterthema': row['Unterthema'],
                                'Unter-Unterthema': row['Unter-Unterthema'],
                                'Stakeholder Bew Auswirkung': row['Stakeholder Bew Auswirkung'],
                                'Stakeholder Bew Finanzen': row['Stakeholder Bew Finanzen'],
                                'Stakeholder Gesamtbew': row['Stakeholder Gesamtbew'],
                                'Quelle': row['Quelle']
                            })


                    # Proceed with merging and sorting if necessary
                    if not st.session_state.stakeholder_punkte_df.empty:
                        merged_df = pd.merge(
                            st.session_state.stakeholder_punkte_df, new_df, 
                            on=['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle'], how='outer', suffixes=('_x', '_y')
                        )
                        merged_df['Stakeholder Bew Auswirkung'] = merged_df['Stakeholder Bew Auswirkung_x'].add(merged_df['Stakeholder Bew Auswirkung_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Bew Finanzen'] = merged_df['Stakeholder Bew Finanzen_x'].add(merged_df['Stakeholder Bew Finanzen_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Gesamtbew'] = merged_df['Stakeholder Gesamtbew_x'].add(merged_df['Stakeholder Gesamtbew_y'], fill_value=0).astype(int)
                        if 'Stakeholder_x' in merged_df.columns and 'Stakeholder_y' in merged_df.columns:
                            merged_df['Stakeholder'] = merged_df[['Stakeholder_x', 'Stakeholder_y']].apply(lambda x: ', '.join(filter(pd.notna, x)), axis=1)
                        elif 'Stakeholder_x' in merged_df.columns:
                            merged_df['Stakeholder'] = merged_df['Stakeholder_x']
                        elif 'Stakeholder_y' in merged_df.columns:
                            merged_df['Stakeholder'] = merged_df['Stakeholder_y']
                        merged_df.drop(columns=['Stakeholder Bew Auswirkung_x', 'Stakeholder Bew Auswirkung_y', 'Stakeholder Bew Finanzen_x', 'Stakeholder Bew Finanzen_y', 'Stakeholder Gesamtbew_x', 'Stakeholder Gesamtbew_y', 'Stakeholder_x', 'Stakeholder_y'], inplace=True)
                        st.session_state.stakeholder_punkte_df = merged_df
                    else:
                        st.session_state.stakeholder_punkte_df = new_df[new_df['Stakeholder Gesamtbew'] >= 1]

                    # Final sorting and ranking
                    st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
                    st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
                    save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})
                    st.success("Stakeholder Punkte erfolgreich übernommen")
                    st.session_state.uploaded_file = None
                    save_session_state({'uploaded_file': st.session_state.uploaded_file})
                    st.experimental_rerun()
                else:
                    if not options:
                        st.info("Punkte können nicht übernommen werden. Bitte fügen sie den entsprechenden Stakeholder unter hinzu und/oder nehmen sie diesen explizit in die Bewertung auf.")
                    else:
                        st.success("Stakeholder Punkte erfolgreich übernommen")

def display_page():
    st.write(st.session_state.ranking_table)
    st.write(st.session_state.table2)
    st.write(st.session_state.sidebar_companies)
    st.write(st.session_state.stakeholder_values)
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
        add_slider()
        stakeholder_punkte()