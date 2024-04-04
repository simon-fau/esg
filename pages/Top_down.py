import streamlit as st
import matplotlib.pyplot as plt

def update_state_generic(key_prefix, gruppe, unterthema, auswahl, checkbox_value):
    key = f"{key_prefix}_{gruppe}_{unterthema}"
    # Update only if checkbox_value is True to avoid overwriting with False on page reruns
    if checkbox_value:
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
    optionen = ["Trifft zu", "Trifft teilweise zu", "Trifft nicht zu"]

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
        col_text.write("**" + thema + "**")
        col_rb1.write("Trifft zu")
        col_rb2.write("Trifft teilweise zu")
        col_rb3.write("Trifft nicht zu")
        
        for unterthema in unterthemen:
            col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
            with col_text:
                st.markdown(f"• {unterthema}")
            for i, option in enumerate(optionen):
                col = [col_rb1, col_rb2, col_rb3][i]
                checkbox_key = f"{state_key}_{unterthema.replace(' ', '_')}_{option.replace(' ', '_')}"
                with col:
                    # Check if the current option matches the stored state to check the checkbox
                    is_checked = st.session_state.get(checkbox_key, '') == option
                    if st.checkbox("", key=checkbox_key + "_checkbox", value=is_checked, label_visibility="collapsed"):
                        # Only update state if checkbox is checked to avoid overwriting with False
                        update_state_generic(state_key, unterthema.replace(' ', '_'), '', option, True)

def create_expander_with_subgroups(thema, unterthemen_gruppen, state_key_prefix):
    with st.expander(thema):
        for gruppe, unterthemen in unterthemen_gruppen.items():
            st.markdown(f"**{gruppe}**")
            for unterthema in unterthemen:
                col_text, col_rb1, col_rb2, col_rb3 = st.columns([6, 1, 1, 1])
                with col_text:
                    st.markdown(f"• {unterthema}")
                for i, option in enumerate(optionen):
                    col = [col_rb1, col_rb2, col_rb3][i]
                    checkbox_key = f"{state_key_prefix}_{gruppe.replace(' ', '_')}_{unterthema.replace(' ', '_')}_{option.replace(' ', '_')}"
                    with col:
                        is_checked = st.session_state.get(checkbox_key, '') == option
                        if st.checkbox("", key=checkbox_key + "_checkbox", value=is_checked, label_visibility="collapsed"):
                            update_state_generic(state_key_prefix, gruppe.replace(' ', '_'), unterthema.replace(' ', '_'), option, True)


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
