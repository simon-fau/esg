import streamlit as st
import pandas as pd
import plotly.express as px

def display_page():
    # Überprüfen, ob 'dataf' im Session State vorhanden ist, und Initialisierung
    if 'dataf' not in st.session_state:
        st.session_state['dataf'] = pd.DataFrame([
            ["E1", "Klimawandel", "Anpassung an den Klimawandel", "", "Standard"],
            ["E1", "Klimawandel", "Eindämmung des Klimawandels", "", "Standard"],
            ["E1", "Klimawandel", "Energie", "", "Standard"],
            ["E2", "Verschmutzung", "Luftverschmutzung", "", "Standard"],
            ["E2", "Verschmutzung", "Wasserverschmutzung", "", "Standard"],
            ["E2", "Verschmutzung", "Bodenverschmutzung", "", "Standard"],
            ["E2", "Verschmutzung", "Verschmutzung lebender Organismen und Nahrungsressourcen", "", "Standard"],
            ["E2", "Verschmutzung", "Verschmutzung: Bedenkliche Stoffe", "", "Standard"],
            ["E2", "Verschmutzung", "Verschmutzung: Sehr bedenkliche Stoffe", "", "Standard"],
            ["E3", "Wasser- und Meeresressourcen", "Wasserentnahmen", "", "Standard"],
            ["E3", "Wasser- und Meeresressourcen", "Wasserverbrauch", "", "Standard"],
            ["E3", "Wasser- und Meeresressourcen", "Wassernutzung", "", "Standard"],
            ["E3", "Wasser- und Meeresressourcen", "Wassereinleitungen in Gewässer und in die Ozeane", "", "Standard"],
            ["E3", "Wasser- und Meeresressourcen", "Verschlechterung der Wasser-/Meereshabitate und Intensität des Einflusses auf die Meeresressourcen", "", "Standard"],
            ["E4", "Biodiversität und Ökosysteme", "Verlust der biologischen Vielfalt", "", "Standard"],
            ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf den Zustand der Arten", "", "Standard"],
            ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf und Abhängigkeiten von Ökosystemleistungen", "", "Standard"],
            ["E5", "Kreislaufwirtschaft", "Ressourcenzuflüsse, einschließlich Ressourcennutzung", "", "Standard"],
            ["E5", "Kreislaufwirtschaft", "Ressourcenabflüsse in Bezug auf Produkte und Dienstleistungen", "", "Standard"],
            ["E5", "Kreislaufwirtschaft", "Abfall", "", "Standard"],
        ], columns=["ESRS", "Nachhaltigkeitsaspekt", "Themen", "Unterthemen", "Datenherkunft"])

    # Horizontale Linie Trennung Bewertung und Ablauf Wesentlichkeitsanalyse
    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

    with st.sidebar.expander("**Bewertung**", expanded=True):
        # Auswahl der zu bewertenden Zeile
        if 'dataf' in st.session_state and not st.session_state['dataf'].empty:
            row_options = [f"Zeile {i}: {row['Themen']}" for i, row in st.session_state['dataf'].iterrows()]
            row_options.insert(0, "")  # Füge die Option "Wähle eine Zeile" am Anfang der Liste hinzu
            selected_option = st.selectbox("", row_options, key="row_select")
            if selected_option != "":
                selected_row_index = row_options.index(selected_option) - 1
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


    # Zugriff auf das DataFrame aus dem session_state und Anzeige als Tabelle
    if 'dataf' in st.session_state:
        dataf = st.session_state['dataf']

        st.write("Übersicht der potentiellen Nachhaltigkeitspunkte")
        with st.expander("Tabelle anzeigen/ausblenden", expanded=True):
            st.table(dataf)
    else:
        st.error("Es wurden keine Daten aus 'Potentielle Nachhaltigkeitspunkte' gefunden.")

    # Beispiel Daten
    data = pd.DataFrame({
    'Thema': ['Wasserverbrauch', 'Luftverschmutzung', 'Sichere Arbeitsplätze', 'Gesundheit & Sicherheit', 
              'Korruption und Bestechung', 'Bodenverdrängung', 'Diversity', 'Abfall', 'Angemessene Entlohnung', 
              'Prävention und Aufdeckung'],
    'Finanzielle Wesentlichkeit': [2, 8, 5, 7, 3, 2, 9, 6, 4, 10],
    'Auswirkung soziale Wesentlichkeit': [7, 6, 9, 8, 2, 1, 3, 4, 5, 10],
    'Relevanz für Stakeholder': [20, 35, 15, 25, 30, 10, 5, 40, 25, 10],
    'Kategorie': ['Environmental', 'Environmental', 'Social', 'Social', 'Governance', 
                  'Environmental', 'Social', 'Governance', 'Governance', 'Social']
    })

    # Erstellung des Plots
    fig = px.scatter(data, 
                 x='Finanzielle Wesentlichkeit', 
                 y='Auswirkung soziale Wesentlichkeit',
                 size='Relevanz für Stakeholder', 
                 color='Kategorie',
                 hover_name='Thema', 
                 size_max=60)

    # Anpassungen am Layout
    fig.update_layout(
    xaxis_title="Finanzielle Wesentlichkeit",
    yaxis_title="Auswirkungsbezogene Wesentlichkeit",
    legend_title="Kategorie"
    )

    # Anzeige des Plots in Streamlit
    st.plotly_chart(fig)
    


