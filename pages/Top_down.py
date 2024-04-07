import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd

def display_pie_charts():
     # Daten für jedes Donut-Diagramm vorbereiten
    categories = ['Umwelt', 'Sozial', 'Governance']
    data = pd.DataFrame({
        'Kategorie': categories,
        'Wert': [1] * len(categories)  # Dummy-Werte, da die Diagramme leer sein sollen
    })

    # Streamlit Spalten zur Platzierung der Diagramme erstellen
    cols = st.columns(3)

    # Ein Donut-Diagramm für jede Kategorie erstellen und in einer separaten Spalte anzeigen
    for i, kategorie in enumerate(categories):
        chart = alt.Chart(data.query(f"Kategorie == '{kategorie}'")).mark_arc(innerRadius=60, outerRadius=80).encode(
            theta=alt.Theta(field="Wert", type="quantitative"),  # Winkel des Bogens
            color=alt.value('lightgray'),  # Festlegen der Farbe
            tooltip=['Kategorie:N']  # Tooltip für zusätzliche Informationen
        ).properties(
            width=250,  # Breite des Diagramms anpassen
            height=250,  # Höhe des Diagramms anpassen
            title=kategorie  # Titel des Diagramms
        )

        # Diagramm in der entsprechenden Spalte anzeigen
        cols[i].altair_chart(chart, use_container_width=True)

def update_state_generic(key_prefix, gruppe, unterthema, auswahl):
    key = f"{key_prefix}_{gruppe}_{unterthema}"
    st.session_state[key] = auswahl

def define_themes():
    global unterthemen_esrse1, unterthemen_esrse2, unterthemen_esrse3, unterthemen_esrse4
    global unterthemen_esrse5, unterthemen_esrss1, unterthemen_esrss2, unterthemen_esrss3, unterthemen_esrss4, unterthemen_esrsg1, optionen
    unterthemen_esrse1 = ["Anpassung an den Klimawandel", "Klimaschutz", "Energie"]
    unterthemen_esrse2 = ["Luftverschmutzung", "Wasserverschmutzung", "Bodenverschmutzung", "Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Besorgniserregende Stoffe", "Besonders besorgniserregende Stoffe", "Mikroplastik"]
    unterthemen_esrse3 = ["Wasserverbrauch", "Wasserentnahme", "Ableitung von Wasser", "Ableitung von Wasser in die Ozeane", "Gewinnung und Nutzung von Meeresressourcen"]
    unterthemen_esrse4 = {
        "Direkte Ursachen des Biodiversitätsverlusts": ["Klimawandel", "Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen", "Direkte Ausbeutung", "Invasive gebietsfremde Arten", "Umweltverschmutzung", "Sonstige"],
        "Auswirkungen auf den Zustand der Arten": ["Populationsgröße von Arten", "Globales Ausrottungsrisiko von Arten"],
        "Auswirkungen auf den Umfang und den Zustand von Ökosystemen": ["Landdegradation", "Wüstenbildung", "Bodenversiegelung"],
        "Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen": []
    }
    unterthemen_esrse5 = ["Ressourcenflüsse, einschließlich Ressourcennutzung", "Ressourcenabflüsse in Bezug auf Produkte und Dienstleistungen", "Abfall"]
    unterthemen_esrss1 = {
        "Arbeitsbedingungen": ["Sichere Beschäftigung", "Arbeitszeit", "Angemessene Entlohnung", "Sozialer Dialog", "Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Vereinbarkeit von Berufs- und Privatleben", "Gesundheitsschutz und Sicherheit"],
        "Gleichbehandlung und Chancengleichheit": ["Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Schulungen und Kompetenzentwicklung", "Beschäftigung und Inklusion von Menschen mit Behinderungen", "Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Vielfalt"],
        "Sonstige arbeitsbezoge Rechte": ["Kinderarbeit", "Zwangsarbeit", "Angemessene Unterbringung", "Datenschutz"]
    }
    unterthemen_esrss2 = unterthemen_esrss1
    unterthemen_esrss3 = {
        "Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften": ["Angemessene Unterbringung", "Angemessene Ernährung", "Wasser- und Sanitäreinrichtungen", "Bodenbezogene Auswirkungen", "Sicherheitsbezogene Auswirkungen"],
        "Bürgerrechte und politische Rechte von Gemeinschaften": ["Meinungsfreiheit", "Versammlungsfreiheit", "Auswirkung auf Menschenrechtsverteidiger"],
        "Rechte indigener Völker": ["Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung", "Selbstbestimmung", "Kulturelle Rechte"]
    }
    unterthemen_esrss4 = { 
        "Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer": ["Datenschutz", "Meinungsfreiheit", "Zugang zu (hochwertigen) Informationen"],
        "Persönliche Sicherheit von Verbrauchern und/oder Endnutzern": ["Gesundheitsschutz und Sicherheit", "Persönliche Sicherheit", "Kinderschutz"],
        "Soziale Inklusion von Verbrauchern und/oder Endnutzern": ["Nichtdiskriminierung", "Zugang zu Produkten und Dienstleistungen", "Verantwortliche Vermarkzungspraktiken"]
    }
    unterthemen_esrsg1 = ["Unternehmenskultur", "Schutz von Hinweisgebern", "Tierschutz", "Politisches Engagement und Lobbytätigkeiten", "Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken", "Korruption und Bestechung", "Vermeidung und Aufdeckung einschließlich Schulung", "Vorkommnisse"]
    optionen = ["Vorhanden", "Teilweise Vorhanden", "Nicht Vorhanden"]

def initialize_state():
    initial_state = {**{unterthema: None for unterthema in unterthemen_esrse1 + unterthemen_esrse2 + unterthemen_esrse3 + unterthemen_esrse5 + list(unterthemen_esrsg1)},
                     **{f"{gruppe}_{unterthema}": None for gruppe in unterthemen_esrse4 for unterthema in unterthemen_esrse4[gruppe]},
                     **{f"S1_{gruppe}_{unterthema}": None for gruppe in unterthemen_esrss1 for unterthema in unterthemen_esrss1[gruppe]},
                     **{f"S2_{gruppe}_{unterthema}": None for gruppe in unterthemen_esrss2 for unterthema in unterthemen_esrss2[gruppe]},
                     **{f"S3_{gruppe}_{unterthema}": None for gruppe in unterthemen_esrss3 for unterthema in unterthemen_esrss3[gruppe]},
                     **{f"S4_{gruppe}_{unterthema}": None for gruppe in unterthemen_esrss4 for unterthema in unterthemen_esrss4[gruppe]}}
    for key, value in initial_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

def create_expander(thema, unterthemen, state_key):
    with st.expander(thema):
        col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
        if thema == unterthemen_esrse1:
            col_text.write("**" + "Klimawandel" + "**")
        elif thema == unterthemen_esrse2:
            col_text.write("**" + "Umweltverschmutzung" + "**")
        elif thema == unterthemen_esrse3:
            col_text.write("**" + "Wasser- & Meeresressourcen" + "**")
        elif thema == unterthemen_esrse5:
            col_text.write("**" + "Kreislaufwirtschaft" + "**")
        elif thema == unterthemen_esrsg1:
            col_text.write("**" + "Unternehmenspolitik" + "**")

        col_rb1.write("Vorhanden")
        col_rb2.write("Teilweise Vorhanden")
        col_rb3.write("Nicht Vorhanden")
        for unterthema in unterthemen:
            col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
            with col_text:
                st.markdown(f"<p style='font-family:Source Sans Pro;'>• {unterthema}</p>", unsafe_allow_html=True)
            for i, option in enumerate(optionen):
                col = [col_rb1, col_rb2, col_rb3][i]
                with col:
                    checkbox_key = f"{state_key}_{unterthema}_{option}"
                    checkbox_value = st.session_state.get(checkbox_key, False)
                    # Hier passen wir den Aufruf an die erwartete Signatur von update_state_generic an
                    st.checkbox("Select", key=checkbox_key, value=checkbox_value, on_change=update_state_generic, args=(state_key, '', unterthema, option), label_visibility="collapsed")

def create_expander_with_subgroups(thema, unterthemen_gruppen, state_key_prefix):
    with st.expander(thema):
        # Nur in der ersten Zeile die Optionen anzeigen
        col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
        with col_text:
            st.write("")  # Leer, um die Spalte zu füllen
        with col_rb1:
            st.write("Vorhanden")
        with col_rb2:
            st.write("Teilweise Vorhanden")
        with col_rb3:
            st.write("Nicht Vorhanden")

        for gruppe, unterthemen in unterthemen_gruppen.items():
            st.markdown(f"**{gruppe}**")
            for unterthema in unterthemen:
                col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
                with col_text:
                    st.markdown(f"• {unterthema}")
                for i, option in enumerate(optionen):
                    col = [col_rb1, col_rb2, col_rb3][i]
                    with col:
                        checkbox_key = f"{state_key_prefix}_{gruppe}_{unterthema}_{option}"
                        checkbox_value = st.session_state.get(checkbox_key, False)
                        # Die Label-Visibility "collapsed" entfernen, da wir jetzt die Optionen oben anzeigen
                        st.checkbox("Select", key=checkbox_key, value=checkbox_value, on_change=update_state_generic, args=(state_key_prefix, gruppe, unterthema, option), label_visibility="collapsed")


def display_expanders():
    create_expander("ESRS E1 Klimawandel", unterthemen_esrse1, 'auswahl')
    create_expander("ESRS E2 Umweltverschmutzung", unterthemen_esrse2, 'auswahl')
    create_expander("ESRS E3 Wasser- & Meeresressourcen", unterthemen_esrse3, 'auswahl')
    create_expander_with_subgroups("ESRS E4 Biologische Vielfalt und Ökosysteme", unterthemen_esrse4, 'auswahl_e4')
    create_expander("ESRS E5 Kreislaufwirtschaft", unterthemen_esrse5, 'auswahl')
    create_expander_with_subgroups("ESRS S1 Eigene Belegschaft", unterthemen_esrss1, 'auswahl_s1')
    create_expander_with_subgroups("ESRS S2 Arbeitskräfte in der Wertschöpfungskette", unterthemen_esrss2, 'auswahl_s2')
    create_expander_with_subgroups("ESRS S3 Betroffene Gemeinschaften", unterthemen_esrss3, 'auswahl_s3')
    create_expander_with_subgroups("ESRS S4 Verbraucher und Endnutzer", unterthemen_esrss4, 'auswahl_s4')
    create_expander("ESRS G1 Unternehmenspolitik", unterthemen_esrsg1, 'auswahl')

def display_page():
    display_pie_charts()
    define_themes()
    initialize_state()
    display_expanders()
    themen_auswahlen = {
        "ESRS E1": [f"auswahl_{unterthema}" for unterthema in unterthemen_esrse1],
        "ESRS E2": [f"auswahl_{unterthema}" for unterthema in unterthemen_esrse2],
        "ESRS E3": [f"auswahl_{unterthema}" for unterthema in unterthemen_esrse3],
        "ESRS E4": [f"auswahl_e4_{gruppe}_{unterthema}" for gruppe in unterthemen_esrse4 for unterthema in unterthemen_esrse4[gruppe]],
        "ESRS E5": [f"auswahl_{unterthema}" for unterthema in unterthemen_esrse5],
        "ESRS S1": [f"auswahl_s1_{gruppe}_{unterthema}" for gruppe in unterthemen_esrss1 for unterthema in unterthemen_esrss1[gruppe]],
        "ESRS S2": [f"auswahl_s2_{gruppe}_{unterthema}" for gruppe in unterthemen_esrss2 for unterthema in unterthemen_esrss2[gruppe]],
        "ESRS S3": [f"auswahl_s3_{gruppe}_{unterthema}" for gruppe in unterthemen_esrss3 for unterthema in unterthemen_esrss3[gruppe]],
        "ESRS S4": [f"auswahl_s4_{gruppe}_{unterthema}" for gruppe in unterthemen_esrss4 for unterthema in unterthemen_esrss4[gruppe]],
        "ESRS G1": [f"auswahl_{unterthema}" for unterthema in unterthemen_esrsg1]
    }   