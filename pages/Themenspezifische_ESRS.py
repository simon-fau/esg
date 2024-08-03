import streamlit as st
import pickle
import os

def Text():
    st.markdown("""
        Bitte bewerten Sie die Themengebiete anhand ihrer Relevanz für Ihr Unternehmen. Dabei gilt folgende Definition für die verschiedenen Auswahlmöglichkeiten:
        - **Wesentlich**:  Ein Aspekt ist wesentlich, wenn er signifikante tatsächliche oder potenzielle Auswirkungen auf Menschen oder die Umwelt hat oder wesentliche finanzielle Auswirkungen auf das Unternehmen nach sich zieht bzw. zu erwarten sind.
        - **Eher Wesentlich**: Ein Aspekt ist eher wesentlich, wenn er bedeutende, aber nicht unbedingt kritische Auswirkungen auf Menschen oder die Umwelt hat oder wenn finanzielle Auswirkungen wahrscheinlich, aber nicht zwingend erheblich sind.
        - **Eher nicht Wesentlich**: Ein Aspekt ist eher nicht wesentlich, wenn die Auswirkungen auf Menschen oder die Umwelt begrenzt sind oder die finanziellen Auswirkungen gering oder unwahrscheinlich sind.
        - **Nicht Wesentlich**: Ein Aspekt ist nicht wesentlich, wenn er keine oder nur vernachlässigbare Auswirkungen auf Menschen, die Umwelt oder die Finanzen des Unternehmens hat.
    """)

if 'relevance_selection' not in st.session_state:
    st.session_state['relevance_selection'] = {}

def save_session_state():
    with open('session_states_top_down.pkl', 'wb') as f:
        pickle.dump(st.session_state['relevance_selection'], f)

def load_session_state():
    if os.path.exists('session_states_top_down.pkl'):
        with open('session_states_top_down.pkl', 'rb') as f:
            st.session_state['relevance_selection'] = pickle.load(f)

def count_checkboxes():
    checkbox_count = sum(st.session_state['relevance_selection'].values())
    st.session_state['checkbox_count'] = checkbox_count

    total_checkboxes = 93

    percentage_complete = (checkbox_count / total_checkboxes) * 100
    percentage_missing = 100 - percentage_complete

    # Set the session state value for checkbox_state_3
    if checkbox_count == 93:
        st.session_state['checkbox_state_3'] = True
    else:
        st.session_state['checkbox_state_3'] = False
    
    return checkbox_count, percentage_missing


def display_section(topics, section_key, section_title):
    form_key = f'form_{section_key}'
    with st.form(key=form_key, border=False):
        st.subheader(section_title)
        headers = ["Relevant", "Nicht Relevant"]
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)

        current_selection = {}
        validation_passed = True

        for topic, key in topics:
            cols = st.columns([4, 1, 1])
            cols[0].write(f"{topic}:")
            selected_count = 0
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_{section_key}"
                checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                current_selection[checkbox_key] = checkbox_state
                if checkbox_state:
                    selected_count += 1
            if selected_count > 1:
                validation_passed = False

        submitted = st.form_submit_button("💾 Auswahl speichern")
        if submitted:
            if validation_passed:
                st.session_state['relevance_selection'] = {**st.session_state['relevance_selection'], **current_selection}
                st.success("Auswahl erfolgreich gespeichert!")
                save_session_state()
                st.experimental_rerun()  # Seite neu laden, um die neuesten Checkbox-Werte anzuzeigen
            else:
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")

def display_complex_section(sections, section_key, section_title):
    form_key = f'form_{section_key}'
    with st.form(key=form_key, border=False):
        st.subheader(section_title)
        headers = ["Relevant", "Nicht Relevant"]
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)

        def create_section(title, topics):
            st.markdown(f"**{title}**")
            current_selection = {}
            validation_passed = True
            for topic, key in topics:
                cols = st.columns([4, 1, 1])
                cols[0].write(f"{topic}:")
                selected_count = 0
                for i, header in enumerate(headers):
                    checkbox_key = f"{header}_{key}_{section_key}"
                    checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                    checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                    current_selection[checkbox_key] = checkbox_state
                    if checkbox_state:
                        selected_count += 1
                if selected_count > 1:
                    validation_passed = False
            return current_selection, validation_passed

        all_validation_passed = True
        for section_title, topics in sections:
            current_selection, validation_passed = create_section(section_title, topics)
            st.session_state['relevance_selection'] = {
                **st.session_state['relevance_selection'],
                **current_selection
            }
            if not validation_passed:
                all_validation_passed = False

        submitted = st.form_submit_button("💾 Auswahl speichern")
        if submitted:
            if all_validation_passed:
                st.success("Auswahl erfolgreich gespeichert!")
                save_session_state()
                st.experimental_rerun()  # Seite neu laden, um die neuesten Checkbox-Werte anzuzeigen
            else:
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")
    
    st.write(f"Total selected checkboxes: {count_checkboxes()}/93")

def display_E1_Klimawandel():
    topics = [("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"), ("Klimaschutz", "Klimaschutz"), ("Energie", "Energie")]
    display_section(topics, "E1", "Klimawandel")

def display_E2_Umweltverschmutzung():
    topics = [
        ("Luftverschmutzung", "Luftverschmutzung"), ("Wasserverschmutzung", "Wasserverschmutzung"), ("Bodenverschmutzung", "Bodenverschmutzung"),
        ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Verschmutzung_von_lebenden_Organismen_und_Nahrungsressourcen"),
        ("Besorgniserregende Stoffe", "Besorgniserregende_Stoffe"), ("Besonders besorgniserregende Stoffe", "Besonders_besorgniserregende_Stoffe"), ("Mikroplastik", "Mikroplastik")
    ]
    display_section(topics, "E2", "Umweltverschmutzung")

def display_E3_Wasser_und_Meeresressourcen():
    topics = [
        ("Wasserverbrauch", "Wasserverbrauch"), ("Wasserentnahme", "Wasserentnahme"), ("Ableitung von Wasser", "Ableitung_von_Wasser"),
        ("Ableitung von Wasser in die Ozeane", "Ableitung_von_Wasser_in_die_Ozeane"), ("Gewinnung und Nutzung von Meeresressourcen", "Gewinnung_und_Nutzung_von_Meeresressourcen")
    ]
    display_section(topics, "E3", "Wasser- und Meeresressourcen")

def display_E4_Biodiversität():
    sections = [
        ("Direkte Ursachen des Biodiversitätsverlusts", [
            ("Klimawandel", "Klimawandel"),
            ("Land-, Süßwasser- und Meeresnutzungsänderungen", "Land-_Süßwasser-_und_Meeresnutzungsänderungen"),
            ("Direkte Ausbeutung", "Direkte_Ausbeutung"),
            ("Invasive gebietsfremde Arten", "Invasive_gebietsfremde_Arten"),
            ("Umweltverschmutzung", "Umweltverschmutzung"),
            ("Sonstige", "Sonstige")
        ]),
        ("Auswirkungen auf den Zustand der Arten", [
            ("Populationsgröße von Arten", "Populationsgröße_von_Arten"),
            ("Globales Ausrottungsrisiko von Arten", "Globales_Ausrottungsrisiko_von_Arten")
        ]),
        ("Auswirkungen auf den Umfang und den Zustand von Ökosystemen", [
            ("Landdegradation", "Landdegradation"),
            ("Wüstenbildung", "Wüstenbildung"),
            ("Bodenversiegelung", "Bodenversiegelung")
        ]),
        ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", [
            ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", "Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistungen")
        ])
    ]
    display_complex_section(sections, "E4", "Biodiversität")

def display_E5_Kreislaufwirtschaft():
    topics = [("Ressourcenzuflüsse, einschließlich Ressourcennutzung", "Ressourcenzuflüsse,_einschließlich_Ressourcennutzung"), ("Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen", "Ressourcenabflüsse_im_Zusammenhang_mit_Produkten_und_Dienstleistungen"), ("Abfälle", "Abfälle")]
    display_section(topics, "E5", "Kreislaufwirtschaft")

def display_S1_Eigene_Belegschaft():
    sections = [
        ("Arbeitsbedingungen", [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"), ("Sozialer Dialog", "Sozialer_Dialog"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
        ]),
        ("Gleichbehandlung und Chancengleichheit für alle", [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
        ]),
        ("Sonstige arbeitsbezogene Rechte", [
            ("Kinderarbeit", "Kinderarbeit"), ("Zwangarbeit", "Zwangarbeit"), ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"), ("Datenschutz", "Datenschutz")
        ])
    ]
    display_complex_section(sections, "S1", "Eigene Belegschaft")

def display_S2_Belegschaft_Lieferkette():
    sections = [
        ("Arbeitsbedingungen", [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"), ("Sozialer Dialog", "Sozialer_Dialog"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
        ]),
        ("Gleichbehandlung und Chancengleichheit für alle", [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
        ]),
        ("Sonstige arbeitsbezogene Rechte", [
            ("Kinderarbeit", "Kinderarbeit"), ("Zwangarbeit", "Zwangarbeit"), ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"), ("Datenschutz", "Datenschutz")
        ])
    ]
    display_complex_section(sections, "S2", "Belegschaft in der Lieferkette")

def display_S3_Betroffene_Gemeinschaften():
    sections = [
        ("Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften", [
            ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"), ("Angemessene Ernährung", "Angemessene_Ernährung"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"),
            ("Bodenbezogene Auswirkungen", "Bodenbezogene_Auswirkungen"), ("Sicherheitsbezogene Auswirkungen", "Sicherheitsbezogene_Auswirkungen")
        ]),
        ("Bürgerrechte und politische Rechte von Gemeinschaften", [
            ("Meinungsfreiheit", "Meinungsfreiheit"), ("Versammlungsfreiheit", "Versammlungsfreiheit"), ("Auswirkungen auf Menschenrechtsverteidiger", "Auswirkungen_auf_Menschenrechtsverteidiger")
        ]),
        ("Rechte von indigenen Völkern", [
            ("Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung", "Freiwillige_und_in_Kenntnis_der_Sachlage_erteilte_vorherige_Zustimmung"), ("Selbstbestimmung", "Selbstbestimmung"), ("Kulturelle Rechte", "Kulturelle_Rechte")
        ])
    ]
    display_complex_section(sections, "S3", "Betroffene Gemeinschaften")

def display_S4_Verbraucher_und_Endnutzer():
    sections = [
        ("Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer", [
            ("Datenschutz", "Datenschutz"), ("Meinungsfreiheit", "Meinungsfreiheit"), ("Zugang zu (hochwertigen) Informationen", "Zugang_zu_(hochwertigen)_Informationen")
        ]),
        ("Persönliche Sicherheit von Verbrauchern und/oder Endnutzern", [
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"), ("Persönliche Sicherheit", "Persönliche_Sicherheit"), ("Kinderschutz", "Kinderschutz")
        ]),
        ("Soziale Inklusion von Verbrauchern und/oder Endnutzern", [
            ("Nichtdiskriminierung", "Nichtdiskriminierung"), ("Zugang zu Produkten und Dienstleistungen", "Zugang_zu_Produkten_und_Dienstleistungen"), ("Verantwortliche Vermarktungspraktiken", "Verantwortliche_Vermarktungspraktiken")
        ])
    ]
    display_complex_section(sections, "S4", "Verbraucher und Endnutzer")

def display_G1_Unternehmenspolitik():
    topics = [
        ("Unternehmenskultur", "Unternehmenskultur"), ("Schutz von Hinweisgebern (Whistleblowers)", "Schutz_von_Hinweisgebern_(Whistleblowers)"), ("Tierschutz", "Tierschutz"),
        ("Politisches Engagement und Lobbytätigkeiten", "Politisches_Engagement_und_Lobbytätigkeiten"), ("Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken", "Management_der_Beziehungen_zu_Lieferanten,_einschließlich_Zahlungspraktiken"),
        ("Vermeidung und Aufdeckung einschließlich Schulung", "Vermeidung_und_Aufdeckung_einschließlich_Schulung"), ("Vorkommnisse", "Vorkommnisse")
    ]
    display_section(topics, "G1", "Unternehmenspolitik")

def display_page():
    load_session_state()
    checkbox_count = count_checkboxes()
    
    col1, col2 = st.columns([6, 1])
    with col1:
        st.header("Themenspezifische ESRS") 
    with col2:
        container = st.container(border=False)
        with container:
            st.write(f"{checkbox_count} von 93 bewertet")
                      
    Text()
    
    tabs = st.tabs(["Klimawandel", "Umweltverschmutzung", "Wasser- und Meeressourcen", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Belegschaft Lieferkette", "Betroffene Gemeinschaften", "Verbraucher und Endnutzer", "Unternehmenspolitik"])
    with tabs[0]:
        display_E1_Klimawandel()
    with tabs[1]:    
        display_E2_Umweltverschmutzung()
    with tabs[2]:  
        display_E3_Wasser_und_Meeresressourcen()
    with tabs[3]:  
        display_E4_Biodiversität()  
    with tabs[4]: 
        display_E5_Kreislaufwirtschaft()
    with tabs[5]:
        display_S1_Eigene_Belegschaft()
    with tabs[6]:
        display_S2_Belegschaft_Lieferkette()
    with tabs[7]:
        display_S3_Betroffene_Gemeinschaften()
    with tabs[8]:
        display_S4_Verbraucher_und_Endnutzer()
    with tabs[9]:
        display_G1_Unternehmenspolitik()
    
   

