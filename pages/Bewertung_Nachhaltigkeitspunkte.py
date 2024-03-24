import streamlit as st

def display_page():

    # Horizontale Linie in der Sidebar
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    

    # Direktes Hinzufügen von Sidebar-Elementen
    st.sidebar.title("Bewertung")
    st.sidebar.write("Hier können Sie die Nachhaltigkeitspunkte nach der auswirkungsbezogenen und finanziallen Wesentlichkeit bewerten.")

    with st.sidebar.expander("**Auswirkungsbezogen**", expanded=False):
        
        #Ausblenden der Maximum und Minimum Werte des Sliders in der Sidebar
        st.markdown("""
        <style>
            
            .st-emotion-cache-1dx1gwv {
            display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)

        #Slider für die Bewertungen der Auswirkungsbezogenen Wesentlichkeit & Finanziellen Wesentlichkeit
        eintrittswahrscheinlichkeit = st.select_slider(
            "Eintrittswahrscheinlichkeit:",
            options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"],
            key="eintrittswahrscheinlichkeit_auswirkung"
        )
    
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
        
        # Überschrift für die Tabelle
        st.write("Übersicht der potentiellen Nachhaltigkeitspunkte")

        # Erstelle einen Expander und zeige die Tabelle darin an
        with st.expander("Tabelle anzeigen/ausblenden", expanded=False):
            st.table(dataf)
    else:
        st.error("Es wurden keine Daten aus 'Potentielle Nachhaltigkeitspunkte' gefunden.")
    


