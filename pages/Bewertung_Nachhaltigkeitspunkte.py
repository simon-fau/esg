import streamlit as st
import pandas as pd

def sidebar_bewertung_Nachhaltigkeitspunkte():
    
# Horizontale Linie Trennung Bewertung und Ablauf Wesentlichkeitsanalyse
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

    with st.sidebar.expander("**Bewertung**", expanded=True):
    

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

        st.markdown("---")
        st.write("**Auswirkungsbezogene Wesentlichkeit**")

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

        st.markdown("---")
        st.write("**Finanzielle Wesentlichkeit**")

        fin_eintrittswahrscheinlichkeit = st.select_slider(
                "Eintrittswahrscheinlichkeit:",
                options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"],
                key="eintrittswahrscheinlichkeit_finanziell"
            )

        fin_ausmass = st.select_slider(
                "Ausmaß (finanziell):",
                options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"],
                key="ausmass_finanziell"
            )

        st.markdown("---")
        st.write("**Stakeholder Relevanz**")

        sta_relevanz = st.select_slider(
                "Wichtigkeit:",
                options=["Unwichtig", "Gering", "Mittel", "Hoch", "Sehr hoch"],
                key="stakeholder_relevanz"
            )

        st.markdown("---")
         # Button "Bewertung absenden"
        if st.button("Bewertung absenden"):
            # Hier können Sie den Code hinzufügen, der ausgeführt werden soll, wenn der Button gedrückt wird.
            st.write("Bewertung wurde abgesendet!")

def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' in st.session_state:
        df2 = st.session_state.df2
    else:
        df2 = pd.DataFrame({
            "Thema": [],
            "Unterthema": [],
            "Unter-Unterthema": []
        })

    # Zeige alle Themen unabhängig von ihrer Bewertung
    st.write("Liste aller eigens hinzugefügten Themen:")
    st.dataframe(df2)

def stakeholder_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df3' in st.session_state:
        df3 = st.session_state.df3
    else:
        df3 = pd.DataFrame({
            "Thema": [],
            "Unterthema": [],
            "Unter-Unterthema": []
        })

    # Zeige alle Themen unabhängig von ihrer Bewertung
    st.write("Liste aller Themen stakeholder:")
    st.dataframe(df3)

def Top_down_Nachhaltigkeitspunkte():
    # Initialize a list to store topic details
    essential_topics_data = []

    # Iterate over items in session_state to collect essential and more essential topics
    for topic, values in st.session_state.items():
        if isinstance(values, dict):
            if values.get('Wesentlich', False) or values.get('Eher Wesentlich', False):
                # Assuming topic names are stored in the format "Thema - Unterthema - Unter-Unterthema"
                topic_details = topic.split(' - ')
                while len(topic_details) < 3:
                    topic_details.append('')
                # Append to the list with importance level
                essential_topics_data.append(topic_details + ['Wesentlich' if values.get('Wesentlich', False) else 'Eher Wesentlich'])

    # Create a DataFrame from the collected data
    df_essential = pd.DataFrame(essential_topics_data, columns=['Thema', 'Unterthema', 'Unter-Unterthema', 'Wichtigkeit'])
    df_essential = df_essential.sort_values(by=['Wichtigkeit', 'Thema'], ascending=[False, True])

    # Display the DataFrame
    st.write("Liste der als 'Wesentlich' oder 'Eher Wesentlich' markierten Themen aus Top_down:")
    st.dataframe(df_essential)

def display_page():
    sidebar_bewertung_Nachhaltigkeitspunkte()
    tab1, tab2, tab3 = st.tabs(["Bewertung eigender Nachhaltigkeitspunkte", "Stakeholder Nachhaltigkeitspunkte", "Endergebnis"])
    with tab1:
        eigene_Nachhaltigkeitspunkte()
        Top_down_Nachhaltigkeitspunkte()
    with tab2:
        stakeholder_Nachhaltigkeitspunkte()
    with tab3:
        st.title("Endergebnis")

        



