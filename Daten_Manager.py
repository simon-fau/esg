import pandas as pd
import streamlit as st

def load_initial_data():
    if 'namen_tabelle' not in st.session_state:
        # Annahme: 'namen_tabelle.csv' ist Ihre initiale Datendatei.
        # Passen Sie den Pfad und den Dateinamen entsprechend Ihrer Anwendung an.
        try:
            st.session_state['namen_tabelle'] = pd.read_csv('pfad/zu/namen_tabelle.csv')
        except FileNotFoundError:
            st.session_state['namen_tabelle'] = pd.DataFrame(columns=['Gruppe', 'Score'])
            # Optional: Warnung oder Fehlermeldung anzeigen, wenn die Datei nicht gefunden wird.
