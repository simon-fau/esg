import streamlit as st
import os
import pandas as pd
from pages.Stakeholder import generate_stakeholder_ranking


def display_network_from_file(html_file_path):
    if os.path.exists(html_file_path):
        try:
            with open(html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            st.components.v1.html(html_content, height=350, width=350, scrolling=False)
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
    else:
        st.error(f"Die Datei {html_file_path} wurde nicht gefunden.")

def display_page():

    col1, col2, col3, = st.columns((2.5, 3.5, 2), gap='medium')
    
    with col1:
        st.markdown('#### Stakeholder')
        # Überprüfen Sie den Pfad und aktualisieren Sie ihn ggf.
        network_html_path = "network.html"
        display_network_from_file(network_html_path)

        # Füge zusätzlichen leeren Raum hinzu
        st.markdown("<br>", unsafe_allow_html=True)

        # Stakeholder-Ranking anzeigen
        generate_stakeholder_ranking()

     # In den restlichen Spalten können weitere Dashboard-Elemente hinzugefügt werden.
    with col2:
        st.markdown('#### Details')
        # Hier können weitere Informationen oder Visualisierungen hinzugefügt werden.

    with col3:
        st.markdown('#### Details')
        # Details zu den Stakeholdern oder anderen relevanten Daten.