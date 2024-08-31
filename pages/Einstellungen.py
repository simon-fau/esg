import streamlit as st
import os

# Liste der Session State keys, die in Stakeholder_Management.py verwendet werden
stakeholder_keys = [
    'df', 
    'ranking_table', 
    'gruppe', 
    'bestehende_beziehung', 
    'auswirkung', 
    'level_des_engagements', 
    'stakeholdergruppe', 
    'kommunikation', 
    'art_der_betroffenheit', 
    'zeithorizont',
    'checkbox_state_1'
]

# Funktion zum Löschen aller Stakeholder-Session-States
def clear_stakeholder_session_states():
    for key in stakeholder_keys:
        if key in st.session_state:
            del st.session_state[key]

    # Optionale Datei löschen, falls die Sitzung gespeichert wurde
    state_file = 'a.pkl'
    if os.path.exists(state_file):
        os.remove(state_file)

# Button zum Löschen der Session States
if st.button("Clear Stakeholder Management Session States"):
    clear_stakeholder_session_states()
    st.success("All Stakeholder Management session states have been cleared!")