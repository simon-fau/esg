import streamlit as st
import pickle
import os

class YesNoSelection:
    def __init__(self):
        self.load_session_state()
        self.initialize_state()

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

    def save_session_state(self):
        with open('a.pkl', 'wb') as f:
            pickle.dump(st.session_state['yes_no_selection'], f)

    def load_session_state(self):
        if os.path.exists('a.pkl'):
            with open('a.pkl', 'rb') as f:
                st.session_state['yes_no_selection'] = pickle.load(f)

    def E1_Klimawandel(self):
        topics = [
            ("Anpassung an Klimawandel", "Klimawandel"),
            ("Klimaschutz", "Klimaschutz"),
            ("Energie", "Energie")
        ]
        
        header_row = st.columns([4, 1, 1, 1, 1])
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([4, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_E1"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}

    def E2_Umweltverschmutzung(self):
        topics = [
            ("Luftverschmutzung", "Luftverschmutzung"),
            ("Wasserverschmutzung", "Wasserverschmutzung"),
            ("Bodenverschmutzung", "Bodenverschmutzung"),
            ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Organismen_Nahrungsressourcen"),
            ("Besorgniserregende Stoffe", "Besorgniserregende_Stoffe"),
            ("Besonders besorgniserregende Stoffe", "Besonders_besorgniserregende_Stoffe"),
            ("Mikroplastik", "Mikroplastik")
        ]
        
        header_row = st.columns([4, 1, 1, 1, 1])
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([4, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_E2"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}

    def E3_Wasser_und_Meeresressourcen(self):
        topics = [
            ("Wasserverbrauch", "Wasserverbrauch"),
            ("Wasserentnahme", "Wasserentnahme"),
            ("Ableitung von Wasser", "Ableitung_Wasser"),
            ("Ableitung von Wasser in die Ozeane", "Ableitung_Wasser_Ozeane"),
            ("Gewinnung und Nutzung von Meeresressourcen", "Meeresressourcen_Nutzung")
        ]
        
        header_row = st.columns([4, 1, 1, 1, 1])
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([4, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_E3"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}

    def E4_Biodiversität(self):
        direkte_Ursachen_Biodiversitätsverlust = [
            ("Klimawandel", "Klimawandel"),
            ("Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen", "Landnutzungsänderungen"),
            ("Direkte Ausbeutung", "Direkte_Ausbeutung"),
            ("Invasive gebietsfremde Arten", "Invasive_Arten"),
            ("Umweltverschmutzung", "Umweltverschmutzung"),
            ("Sonstige", "Sonstige")
        ]
        
        auswirkung_auf_zustand_der_Arten = [
            ("Populationsgröße von Arten", "Populationsgröße_Arten"),
            ("Globales Ausrottungsrisiko von Arten", "Globales_Ausrottungsrisiko_Arten")
        ]
    
        auswirkung_auf_Oekosysteme = [
            ("Landdegradation", "Landdegradation"),
            ("Wüstenbildung", "Wüstenbildung"),
            ("Bodenversiegelung", "Bodenversiegelung")
        ]
    
        Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistunge = [
            ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", "Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen")
        ]
    
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
                    checkbox_key = f"{header}_{key}_E4"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection
    
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **create_section("Direkte Ursachen des Biodiversitätsverlusts", direkte_Ursachen_Biodiversitätsverlust),
            **create_section("Auswirkungen auf den Zustand der Arten", auswirkung_auf_zustand_der_Arten),
            **create_section("Auswirkungen auf den Umfang und den Zustand von Ökosystemen", auswirkung_auf_Oekosysteme),
            **create_section("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistunge),
        }

    def E5_Kreislaufwirtschaft(self):
        topics = [
            ("Ressourcenzuflüsse, einschließlich Ressourcennutzung", "Ressourcenzuflüsse"),
            ("Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen", "Ressourcenabflüsse"),
            ("Abfälle", "Abfälle")
        ]

        header_row = st.columns([4, 1, 1, 1, 1])
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([4, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_E5"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}

    def S1_Eigene_Belegschaft(self):
        arbeitsbedingungen = [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"),
            ("Arbeitszeit", "Arbeitszeit"),
            ("Angemessene Entlohnung", "Angemessene Entlohnung"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit"),
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz"),
        ]

        gleichbehandlung_und_chancengleichheit = [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung"),
            ("Schulungen und Kompetenzentwicklung", "Schulungen"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Inklusion"),
            ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Gewalt"),
            ("Vielfalt", "Vielfalt"),
        ]

        sonstige_arbeitsbezogene_rechte = [
            ("Kinderarbeit", "Kinderarbeit"),
            ("Zwangarbeit", "Zwangarbeit"),
            ("Angemessene Unterbringungen", "Unterbringungen"),
            ("Datenschutz", "Datenschutz"),
        ]

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
                    checkbox_key = f"{header}_{key}_S1"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection
    
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **create_section("Arbeitsbedingungen", arbeitsbedingungen),
            **create_section("Gleichbehandlung und Chancengleichheit für alle", gleichbehandlung_und_chancengleichheit),
            **create_section("Sonstige arbeitsbezogene Rechte", sonstige_arbeitsbezogene_rechte),
        }

    def S2_Belegschaft_Lieferkette(self):
        arbeitsbedingungen = [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"),
            ("Arbeitszeit", "Arbeitszeit"),
            ("Angemessene Entlohnung", "Angemessene Entlohnung"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit"),
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz"),
        ]

        gleichbehandlung_und_chancengleichheit = [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung"),
            ("Schulungen und Kompetenzentwicklung", "Schulungen"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Inklusion"),
            ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Gewalt"),
            ("Vielfalt", "Vielfalt"),
        ]

        sonstige_arbeitsbezogene_rechte = [
            ("Kinderarbeit", "Kinderarbeit"),
            ("Zwangarbeit", "Zwangarbeit"),
            ("Angemessene Unterbringungen", "Unterbringungen"),
            ("Datenschutz", "Datenschutz"),
        ]

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
                    checkbox_key = f"{header}_{key}_S2"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection
    
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **create_section("Arbeitsbedingungen", arbeitsbedingungen),
            **create_section("Gleichbehandlung und Chancengleichheit für alle", gleichbehandlung_und_chancengleichheit),
            **create_section("Sonstige arbeitsbezogene Rechte", sonstige_arbeitsbezogene_rechte),
        }

    def S3_Betroffene_Gemeinschaften(self):
        wirtschafttliche_soziale_und_kulturelle_rechte = [
            ("Angemessene Unterbringungen", "Unterbringungen"),
            ("Angemessene Ernährung", "Ernährung"),
            ("Wasser- und Sanitäreinrichtungen", "Wasser"),
            ("Bodenbezogene Auswirkungen", "Boden"),
            ("Sicherheitsbezogene Auswirkungen", "Sicherheit"),
        ]

        bürgerrechte_und_politische_rechte = [
            ("Meinungsfreiheit", "Meinungsfreiheit"),
            ("Versammlungsfreiheit", "Versammlungsfreiheit"),
            ("Auswirkungen auf Menschenrechtsverteidiger", "Menschenrechtsverteidiger"),
        ]

        rechte_von_indigenen_völkern = [
            ("Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung", "Zustimmung"),
            ("Selbstbestimmung", "Selbstbestimmung"),
            ("Kulturelle Rechte", "Kulturelle_Rechte"),
        ]

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
                    checkbox_key = f"{header}_{key}_S3"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection
    
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **create_section("Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften", wirtschafttliche_soziale_und_kulturelle_rechte),
            **create_section("Bürgerrechte und politische Rechte von Gemeinschaften", bürgerrechte_und_politische_rechte),
            **create_section("Rechte von indigenen Völkern", rechte_von_indigenen_völkern),
        }
            
    def S4_Verbraucher_und_Endnutzer(self):
        informationsbezogene_auswirkungen_für_verbraucher_und_endnutzer = [
            ("Datenschutz", "Datenschutz"),
            ("Meinungsfreiheit", "Meinungsfreiheit"),
            ("Zugang zu (hochwertigen) Informationen", "Zugang"),   
        ]

        persönliche_sicherheit_von_verbrauchern_und_endnutzern = [
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz"),
            ("Persönliche Sicherheit", "Persönliche_Sicherheit"),
            ("Kinderschutz", "Kinderschutz"),
        ]

        soziale_inklusion_von_verbrauchern_und_endnutzern = [
            ("Nichtdiskriminierung", "Nichtdiskriminierung"),
            ("Zugang zu Produkten und Dienstleistungen", "Zugang"),
            ("Verantwortliche Vermarktungspraktiken", "Vermarktungspraktiken"),
        ]

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
                    checkbox_key = f"{header}_{key}_S4"
                    value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                    current_selection[checkbox_key] = value
            return current_selection
    
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **create_section("Informationsbezogene Auswirkungen für Verbraucher und Endnutzer", informationsbezogene_auswirkungen_für_verbraucher_und_endnutzer),
            **create_section("Persönliche Sicherheit von Verbrauchern und Endnutzern", persönliche_sicherheit_von_verbrauchern_und_endnutzern),
            **create_section("Soziale Inklusion von Verbrauchern und Endnutzern", soziale_inklusion_von_verbrauchern_und_endnutzern),
        }
    
    
    
    def display_E1_Klimawandel(self):
        self.E1_Klimawandel()
        col1, col2 = st.columns([5, 0.8]) # Erstellt zwei Spalten, wobei die zweite Spalte für den Button ist
        with col1:
            pass  
        with col2:  # Dies sorgt dafür, dass der Button in der zweiten Spalte (rechts) angezeigt wird
            button = st.button("Auswahl speichern", key='Button_Klimawandel')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_E2_Umweltverschmutzung(self):
        self.E2_Umweltverschmutzung()
        col1, col2 = st.columns([5, 0.8]) # Erstellt zwei Spalten, wobei die zweite Spalte für den Button ist
        with col1:
            pass  
        with col2:
            button = st.button("Auswahl speichern", key ='Button_Umweltverschmutzung')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_E3_Wasser_und_Meeresressourcen(self):
        self.E3_Wasser_und_Meeresressourcen()
        col1, col2 = st.columns([5, 0.8]) # Erstellt zwei Spalten, wobei die zweite Spalte für den Button ist
        with col1:
            pass  
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_WasserundMeeresressourcen')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_E4_Biodiversität(self):
        self.E4_Biodiversität()
        col1, col2 = st.columns([5, 0.8]) # Erstellt zwei Spalten, wobei die zweite Spalte für den Button ist
        with col1:
            pass  
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Biodiversität')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_E5_Kreislaufwirtschaft(self):
        self.E5_Kreislaufwirtschaft()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Kreislaufwirtschaft')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_S1_Eigene_Belegschaft(self):
        self.S1_Eigene_Belegschaft()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Eigene_Belegschaft')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_S2_Belegschaft_Lieferkette(self):
        self.S2_Belegschaft_Lieferkette()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Belegschaft_Lieferkette')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_S3_Betroffene_Gemeinschaften(self):
        self.S3_Betroffene_Gemeinschaften()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Betroffene_Gemeinschaften')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

    def display_S4_Verbraucher_und_Endnutzer(self):
        self.S4_Verbraucher_und_Endnutzer()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Verbraucher_und_Endnutzer')
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

def display_session_state_contents():
    st.write("Aktueller Session State Inhalt:")
    st.json(st.session_state['yes_no_selection'])

def display_page():
    selection = YesNoSelection()
    tabs = st.tabs(["Klimawandel", "Umweltverschmutzung", "Meeres- und Wasserressourcen", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Belegschaft Lieferkette", "Betroffene Gemeinschaften", "Verbraucher und End-nutzer", "Unternehmenspolitik"])
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
        selection.display_E4_Biologische_Vielfalt_und_Oekosysteme()  
    with tabs[4]:
        st.subheader("Kreislaufwirtschaft")
        selection.display_E5_Kreislaufwirtschaft()
    with tabs[5]:
        st.subheader("Eigene Belegschaft")
        selection.display_S1_Eigene_Belegschaft()
    with tabs[6]:
        st.subheader("Belegschaft Lieferkette")
        selection.display_S2_Arbeitskräfte_in_der_Wertschöpfungskette()
    with tabs[7]:
        st.subheader("Betroffene Gemeinschaften")
    with tabs[8]:
        st.subheader("Verbraucher und End-nutzer")
    with tabs[9]:
        st.subheader("Unternehmenspolitik")

        



