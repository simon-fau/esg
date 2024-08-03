import streamlit as st
import pickle

# Konstante für den Dateinamen des Sitzungszustands
STATE_FILE = 'a.pkl'

# Funktion zum Speichern des Sitzungszustands
def save_state():
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(dict(st.session_state), f)

def initialize_session_state():
    if 'ranking_table' not in st.session_state:
        st.error("No ranking table found in session state")
        return False
    if 'table2' not in st.session_state:
        st.session_state.table2 = []
    if 'table1' not in st.session_state:
        st.session_state.table1 = st.session_state['ranking_table']['Gruppe'].tolist()
    else:
        update_table1()
    if 'checkbox_state_2' not in st.session_state:
        st.session_state['checkbox_state_2'] = False
    return True

def update_table1():
    current_ranking = st.session_state['ranking_table']['Gruppe'].tolist()
    new_items = [item for item in current_ranking if item not in st.session_state.table1 and item not in st.session_state.table2]
    st.session_state.table1.extend(new_items)

def display_not_in_evaluation():
    st.write("**Nicht in Bewertung aufgenommene Stakeholder:**")
    ranking_table = st.session_state['ranking_table'].copy()
    
    if 'Score' in ranking_table.columns:
        ranking_table['Score'] = ranking_table['Score'].apply(lambda x: x)  # Remove percentage formatting if any
        not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.table1)]
        st.dataframe(not_in_evaluation[['Ranking', 'Gruppe', 'Score']],
                     column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, 
                     hide_index=True,
                     width=800)
    else:
        not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.table1)]
        st.dataframe(not_in_evaluation[['Ranking', 'Gruppe']],
                     hide_index=True,
                     width=800)

def display_in_evaluation():
    st.write("**In Bewertung aufgenommene Stakeholder:**")
    if st.session_state.table2:
        table2_df = st.session_state['ranking_table'][st.session_state['ranking_table']['Gruppe'].isin(st.session_state.table2)]
        if 'Score' in table2_df.columns:
            table2_df['Score'] = table2_df['Score'].apply(lambda x: x)  # Remove percentage formatting if any
            st.dataframe(table2_df[['Ranking', 'Gruppe', 'Score']],
                         column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, 
                         hide_index=True,
                         width=800)
        else:
            st.dataframe(table2_df[['Ranking', 'Gruppe']],
                         hide_index=True,
                         width=800)

def add_to_table2(selected_items):
    for item in selected_items:
        if item in st.session_state.table1:
            st.session_state.table2.append(item)
            st.session_state.table1.remove(item)

def remove_from_table2(selected_items):
    for item in selected_items:
        if item in st.session_state.table2:
            st.session_state.table2.remove(item)
            st.session_state.table1.append(item)

def add_button_selection():
    selected_table1 = st.multiselect(
        "Wählen Sie Stakeholder zum Hinzufügen aus:",
        st.session_state.table1,
        key="select_table1"
    )
    if st.button("Hinzufügen >>>"):
        add_to_table2(selected_table1)
        st.experimental_rerun()

def remove_button_selection():
    selected_table2 = st.multiselect(
        "Wählen Sie Stakeholder zum Entfernen aus:",
        st.session_state.table2,
        key="select_table2"
    )
    if st.button("<<< Entfernen"):
        remove_from_table2(selected_table2)
        st.experimental_rerun()

def check_abgeschlossen_stakeholder_auswahl():
    if 'checkbox_state_2' not in st.session_state:
        st.session_state['checkbox_state_2'] = False
    
    # Checkbox erstellen und Zustand in st.session_state speichern
    st.session_state['checkbox_state_2'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_2'])

def display_page():
    col1, col2 = st.columns([7, 1])
    with col1:
        st.header("Stakeholder Auswahl")
    with col2:
        container = st.container(border=False)
        with container:
            check_abgeschlossen_stakeholder_auswahl()
    st.write("Wählen Sie die Stakeholder aus, die Sie in die Bewertung aufnehmen möchten.")

    if not initialize_session_state():
        return

    col1, col_placeholder, col2 = st.columns([1, 1, 1])

    with col1:
        st.write(" ")
        st.write(" ")
        add_button_selection()
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")

        display_not_in_evaluation()
    
    with col_placeholder:
        pass

    with col2:
        st.write(" ")
        st.write(" ")
        remove_button_selection()
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        display_in_evaluation()

    save_state()