import streamlit as st
import pandas as pd
from pages.Stakeholder_Management import stakeholder_ranking

def update_session_state():
    # Ensure that the 'Gruppe' column is used to initialize or update table1 if the ranking table exists
    if 'ranking_table' in st.session_state:
        current_ranking = st.session_state['ranking_table']['Gruppe'].tolist()
        
        # Initialize table1 if not present
        if 'table1' not in st.session_state:
            st.session_state.table1 = current_ranking
        else:
            # Update table1 with any new items from the ranking table
            new_items = [item for item in current_ranking if item not in st.session_state.table1 and item not in st.session_state.table2]
            st.session_state.table1.extend(new_items)
    else:
        st.error("No ranking table found in session state")

def stakeholder_alle():
    # Display table 1 with checkboxes
    selected_table1 = []
    for item in st.session_state.table1:
        if st.checkbox(item, key=f"table1_{item}"):
            selected_table1.append(item)
    return selected_table1

def stakeholder_auswahl():
    if 'table2' not in st.session_state:
        st.session_state.table2 = []  # table2 wird bereits leer initialisiert

    # Display table 2 with checkboxes
    selected_table2 = []
    for item in st.session_state.table2:
        if st.checkbox(item, key=f"table2_{item}"):
            selected_table2.append(item)
    return selected_table2

def button_nach_rechts(selected_table1):
    # Buttons to move items
    if st.button("Hinzufügen >>>"):
        if selected_table1:
            move_items(st.session_state.table1, st.session_state.table2, selected_table1)
            st.experimental_rerun()

def button_nach_links(selected_table2):
    if st.button("<<< Entfernen"):
        if selected_table2:
            move_items(st.session_state.table2, st.session_state.table1, selected_table2)
            st.experimental_rerun()

def move_items(source, target, items):
    for item in items:
        if item in source:
            source.remove(item)
        if item not in target:
            target.append(item)

def display_page():
    st.title("Stakeholder Auswahl")
    st.write("Wählen Sie die Stakeholder aus, die Sie in die Bewertung aufnehmen möchten.")
    
    with st.sidebar:
        st.markdown("---")
        st.write("**Stakeholder Ranking**")
        stakeholder_ranking()
    
    # Update the session state to reflect any new items in the ranking table
    update_session_state()

    st.markdown("---")
    col1, col2 = st.columns([1, 1])  # Adjust the width of the button column if needed
    
    with col1:
        st.write("**Nicht in Bewertung aufgenommene Stakeholder:**")
        selected_table1 = stakeholder_alle()
        button_nach_rechts(selected_table1)

    with col2:
        st.write("**In Bewertung aufgenommene Stakeholder:**")
        selected_table2 = stakeholder_auswahl()
        button_nach_links(selected_table2)

