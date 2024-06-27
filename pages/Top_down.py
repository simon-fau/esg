import streamlit as st
import pickle
import os

class YesNoSelection:
    def __init__(self):
        self.load_session_state()
        self.initialize_state()

    # Initialisiert den Zustand der Auswahloptionen
    def initialize_state(self):
        options = {
            'Wesentlich_Klimawandel': False,
            'Eher_Wesentlich_Klimawandel': False,
            'Eher_nicht_wesentlich': False,
            'Nicht_Wesentlich_Klimawandel': False,
            'Wesentlich_Klimawandel_2': False,
            'Eher_Wesentlich_Klimawandel_2': False,
            'Eher_nicht_wesentlich_2': False,
            'Nicht_Wesentlich_Klimawandel_2': False
        }
        if 'yes_no_selection' not in st.session_state:
            st.session_state['yes_no_selection'] = options

    # Speichert den aktuellen Zustand der Auswahloptionen in eine Pickle-Datei
    def save_session_state(self):
        with open('session_states_top_down.pkl', 'wb') as f:
            pickle.dump(st.session_state['yes_no_selection'], f)

    # Lädt den Zustand der Auswahloptionen aus einer Pickle-Datei
    def load_session_state(self):
        if os.path.exists('session_states_top_down.pkl'):
            with open('session_states_top_down.pkl', 'rb') as f:
                st.session_state['yes_no_selection'] = pickle.load(f)

    # Definiert die Struktur für Auswahlsektionen ohne Untersektionen z.B für Klimawandel
    def display_section(self, topics, section_key):
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        header_row = st.columns([4, 1, 1, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([4, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_{section_key}"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}

    # Definiert die Struktur für komplexe Auswahlsektionen mit mehreren Untersektionen z.B für Biodiversität
    def display_complex_section(self, sections, section_key):
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        header_row = st.columns([4, 1, 1, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)

        def create_section(title, topics):
            st.markdown(f"**{title}**")
            current_selection = {}
            for topic, key in topics:
                cols = st.columns([4, 1, 1, 1, 1])
                cols[0].write(f"{topic}:")
                for i, header in enumerate(headers):
                    checkbox_key = f"{header}_{key}_{section_key}"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection

        for section_title, topics in sections:
            st.session_state['yes_no_selection'] = {
                **st.session_state['yes_no_selection'],
                **create_section(section_title, topics)
            }

    # Zeigt einen Speicher-Button an und speichert den Zustand, wenn dieser gedrückt wird
    def display_save_button(self, section_name):
        col1, col2 = st.columns([5, 0.8])
        with col2:
            if st.button(f"Auswahl speichern", key=f'Button_{section_name}'):
                self.save_session_state()
                st.success("Auswahl erfolgreich gespeichert!")

    # Zeigt die Auswahloptionen für Klimawandel an
    def display_E1_Klimawandel(self):
        topics = [("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"), ("Klimaschutz", "Klimaschutz"), ("Energie", "Energie")]
        self.display_section(topics, "E1")
        self.display_save_button("Klimawandel")

    # Zeigt die Auswahloptionen für Umweltverschmutzung an
    def display_E2_Umweltverschmutzung(self):
        topics = [
            ("Luftverschmutzung", "Luftverschmutzung"), ("Wasserverschmutzung", "Wasserverschmutzung"), ("Bodenverschmutzung", "Bodenverschmutzung"),
            ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Verschmutzung_von_lebenden_Organismen_und_Nahrungsressourcen"),
            ("Besorgniserregende Stoffe", "Besorgniserregende_Stoffe"), ("Besonders besorgniserregende Stoffe", "Besonders_besorgniserregende_Stoffe"), ("Mikroplastik", "Mikroplastik")
        ]
        self.display_section(topics, "E2")
        self.display_save_button("Umweltverschmutzung")

    # Zeigt die Auswahloptionen für Wasser- und Meeresressourcen an
    def display_E3_Wasser_und_Meeresressourcen(self):
        topics = [
            ("Wasserverbrauch", "Wasserverbrauch"), ("Wasserentnahme", "Wasserentnahme"), ("Ableitung von Wasser", "Ableitung_von_Wasser"),
            ("Ableitung von Wasser in die Ozeane", "Ableitung_von_Wasser_in_die_Ozeane"), ("Gewinnung und Nutzung von Meeresressourcen", "Gewinnung_und_Nutzung_von_Meeresressourcen")
        ]
        self.display_section(topics, "E3")
        self.display_save_button("WasserundMeeresressourcen")

    # Zeigt die Auswahloptionen für Biodiversität an
    def display_E4_Biodiversität(self):
        sections = [
            ("Direkte Ursachen des Biodiversitätsverlusts", [
                ("Klimawandel", "Klimawandel"),
                ("Land-, Süßwasser- und Meeresnutzungsänderungen", "Land-,_Süßwasser-_und_Meeresnutzungsänderungen"),
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
        self.display_complex_section(sections, "E4")
        self.display_save_button("Biodiversität")

    # Zeigt die Auswahloptionen für Kreislaufwirtschaft an
    def display_E5_Kreislaufwirtschaft(self):
        topics = [("Ressourcenzuflüsse, einschließlich Ressourcennutzung", "Ressourcenzuflüsse,_einschließlich_Ressourcennutzung"), ("Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen", "Ressourcenabflüsse_im_Zusammenhang_mit_Produkten_und_Dienstleistungen"), ("Abfälle", "Abfälle")]
        self.display_section(topics, "E5")
        self.display_save_button("Kreislaufwirtschaft")

    # Zeigt die Auswahloptionen für die eigene Belegschaft an
    def display_S1_Eigene_Belegschaft(self):
        sections = [
            ("Arbeitsbedingungen", [
                ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"),
                ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
                ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
                ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
            ]),
            ("Gleichbehandlung und Chancengleichheit für alle", [
                ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
                ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
            ]),
            ("Sonstige arbeitsbezogene Rechte", [
                ("Kinderarbeit", "Kinderarbeit"), ("Zwangarbeit", "Zwangarbeit"), ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"), ("Datenschutz", "Datenschutz")
            ])
        ]
        self.display_complex_section(sections, "S1")
        self.display_save_button("Eigene_Belegschaft")

    # Zeigt die Auswahloptionen für die Belegschaft in der Lieferkette an
    def display_S2_Belegschaft_Lieferkette(self):
        sections = [
            ("Arbeitsbedingungen", [
                ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"),
                ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
                ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
                ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
            ]),
            ("Gleichbehandlung und Chancengleichheit für alle", [
                ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
                ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
            ]),
            ("Sonstige arbeitsbezogene Rechte", [
                ("Kinderarbeit", "Kinderarbeit"), ("Zwangarbeit", "Zwangarbeit"), ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"), ("Datenschutz", "Datenschutz")
            ])
        ]
        self.display_complex_section(sections, "S2")
        self.display_save_button("Belegschaft_Lieferkette")

    # Zeigt die Auswahloptionen für betroffene Gemeinschaften an
    def display_S3_Betroffene_Gemeinschaften(self):
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
        self.display_complex_section(sections, "S3")
        self.display_save_button("Betroffene_Gemeinschaften")
            
    # Zeigt die Auswahloptionen für Verbraucher und Endnutzer an
    def display_S4_Verbraucher_und_Endnutzer(self):
        sections = [
            ("Informationsbezogene Auswirkungen für Verbraucher und Endnutzer", [
                ("Datenschutz", "Datenschutz"), ("Meinungsfreiheit", "Meinungsfreiheit"), ("Zugang zu (hochwertigen) Informationen", "Zugang_zu_(hochwertigen)_Informationen")
            ]),
            ("Persönliche Sicherheit von Verbrauchern und Endnutzern", [
                ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"), ("Persönliche Sicherheit", "Persönliche_Sicherheit"), ("Kinderschutz", "Kinderschutz")
            ]),
            ("Soziale Inklusion von Verbrauchern und Endnutzern", [
                ("Nichtdiskriminierung", "Nichtdiskriminierung"), ("Zugang zu Produkten und Dienstleistungen", "Zugang_zu_Produkten_und_Dienstleistungen"), ("Verantwortliche Vermarktungspraktiken", "Verantwortliche_Vermarktungspraktiken")
            ])
        ]
        self.display_complex_section(sections, "S4")
        self.display_save_button("Verbraucher_und_Endnutzer")

    # Zeigt die Auswahloptionen für Unternehmenspolitik an
    def display_G1_Unternehmenspolitik(self):
        topics = [
            ("Unternehmenskultur", "Unternehmenskultur"), ("Schutz von Hinweisgebern (Whistleblowers)", "Schutz_von_Hinweisgebern_(Whistleblowers)"), ("Tierschutz", "Tierschutz"),
            ("Politisches Engagement und Lobbytätigkeiten", "Politisches_Engagement_und_Lobbytätigkeiten"), ("Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken", "Management_der_Beziehungen_zu_Lieferanten,_einschließlich_Zahlungspraktiken"),
            ("Vermeidung und Aufdeckung einschließlich Schulung", "Vermeidung_und_Aufdeckung_einschließlich_Schulung"), ("Vorkommnisse", "Vorkommnisse")
        ]
        self.display_section(topics, "G1")
        self.display_save_button("Unternehmenspolitik")

# Hauptfunktion zum Anzeigen der Seite mit den verschiedenen Auswahloptionen
def display_page():
    selection = YesNoSelection()
    tabs = st.tabs(["Klimawandel", "Umweltverschmutzung", "Meeres- und Wasserressourcen", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Belegschaft Lieferkette", "Betroffene Gemeinschaften", "Verbraucher und Endnutzer", "Unternehmenspolitik"])
    with tabs[0]:
        st.subheader("Klimawandel")
        selection.display_E1_Klimawandel()
    with tabs[1]:
        st.subheader("Umweltverschmutzung")
        selection.display_E2_Umweltverschmutzung()
    with tabs[2]:
        st.subheader("Meeres- und Wasserressourcen")
        selection.display_E3_Wasser_und_Meeresressourcen()
    with tabs[3]:
        st.subheader("Biodiversität")
        selection.display_E4_Biodiversität()  
    with tabs[4]:
        st.subheader("Kreislaufwirtschaft")
        selection.display_E5_Kreislaufwirtschaft()
    with tabs[5]:
        st.subheader("Eigene Belegschaft")
        selection.display_S1_Eigene_Belegschaft()
    with tabs[6]:
        st.subheader("Belegschaft Lieferkette")
        selection.display_S2_Belegschaft_Lieferkette()
    with tabs[7]:
        st.subheader("Betroffene Gemeinschaften")
        selection.display_S3_Betroffene_Gemeinschaften()
    with tabs[8]:
        st.subheader("Verbraucher und Endnutzer")
        selection.display_S4_Verbraucher_und_Endnutzer()
    with tabs[9]:
        st.subheader("Unternehmenspolitik")
        selection.display_G1_Unternehmenspolitik()
