import streamlit as st
import pandas as pd

def display_page():
    # Überprüfen, ob 'dataf' im Session State vorhanden ist, und Initialisierung
    if 'dataf' not in st.session_state:
        st.session_state['dataf'] = pd.DataFrame([
            ["E1", "Klimawandel", "Anpassung an den Klimawandel", "", "Standard"],
            ["E1", "Klimawandel", "Eindämmung des Klimawandels", "", "Standard"],
            # Fügen Sie weitere Zeilen nach Bedarf hinzu
            ["E5", "Kreislaufwirtschaft", "Abfall", "", "Standard"],
        ], columns=["ESRS", "Nachhaltigkeitsaspekt", "Themen", "Unterthemen", "Datenherkunft"])

    # Horizontale Linie in der Sidebar
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    
    # Direktes Hinzufügen von Sidebar-Elementen
    st.sidebar.title("Bewertung")
    # Auswahl der zu bewertenden Zeile
    if 'selected_row' not in st.session_state:
        st.session_state['selected_row'] = 0

    if 'dataf' in st.session_state and not st.session_state['dataf'].empty:
        row_options = [f"Zeile {i}: {row['Themen']}" for i, row in st.session_state['dataf'].iterrows()]
        selected_option = st.sidebar.selectbox("Wählen Sie einen Eintrag für die Bewertung:", row_options, key="row_select")
        selected_row_index = row_options.index(selected_option)
        st.session_state['selected_row'] = selected_row_index

        # Ausblenden der Maximum und Minimum Werte des Sliders in der Sidebar und Ändern der Schriftart
        st.markdown("""
        <style>
            .st-emotion-cache-1dx1gwv {
            display: none !important;
            }
            .st-emotion-cache-10y5sf6 {
            font-family: 'Source Sans Pro', monospace;
            }        
        </style>
        """, unsafe_allow_html=True)

        with st.sidebar.expander("**Auswirkungsbezogen**", expanded=False):
            #Slider für die Bewertungen der Auswirkungsbezogenen Wesentlichkeit & Finanziellen Wesentlichkeit
            eintrittswahrscheinlichkeit = st.select_slider(
                "Eintrittswahrscheinlichkeit:",
                options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"],
                key="eintrittswahrscheinlichkeit_auswirkung"
            )
            # Weitere Bewertungskriterien wie zuvor definiert
                        # Fortsetzung der Bewertungskriterien
            ausmass = st.select_slider(
                "Ausmaß:",
                options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"],
                key="ausmass_auswirkung"
            )

            umfang = st.select_slider(
                "Umfang:",
                options=["Keine", "Lokal", "Regional", "National", "International", "Global"],
                key="umfang_auswirkung"
            )

            behebbarkeit = st.select_slider(
                "Behebbarkeit:",
                options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"],
                key="behebbarkeit_auswirkung"
            )

        with st.sidebar.expander("**Finanziell**", expanded=False):
            fin_eintrittswahrscheinlichkeit = st.select_slider(
                "Eintrittswahrscheinlichkeit (finanziell):",
                options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"],
                key="eintrittswahrscheinlichkeit_finanziell"
            )

            fin_ausmass = st.select_slider(
                "Ausmaß (finanziell):",
                options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"],
                key="ausmass_finanziell"
            )

    # Zugriff auf das DataFrame aus dem session_state und Anzeige als Tabelle
    if 'dataf' in st.session_state:
        dataf = st.session_state['dataf']

        st.write("Übersicht der potentiellen Nachhaltigkeitspunkte")
        with st.expander("Tabelle anzeigen/ausblenden", expanded=True):
            st.table(dataf)
    else:
        st.error("Es wurden keine Daten aus 'Potentielle Nachhaltigkeitspunkte' gefunden.")


    


