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
        with open('ab.pkl', 'wb') as f:
            pickle.dump(st.session_state['yes_no_selection'], f)

    def load_session_state(self):
        if os.path.exists('ab.pkl'):
            with open('ab.pkl', 'rb') as f:
                st.session_state['yes_no_selection'] = pickle.load(f)

    def E1_Klimawandel(self):
        topics = [
            ("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"),
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
            ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Verschmutzung_von_lebenden_Organismen_und_Nahrungsressourcen"),
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
            ("Ableitung von Wasser", "Ableitung_von_Wasser"),
            ("Ableitung von Wasser in die Ozeane", "Ableitung_von_Wasser_in_die_Ozeane"),
            ("Gewinnung und Nutzung von Meeresressourcen", "Gewinnung_und_Nutzung_von_Meeresressourcen")
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
            ("Land-, Süßwasser- und Meeresnutzungsänderungen", "Land-,_Süßwasser-_und_Meeresnutzungsänderungen"),
            ("Direkte Ausbeutung", "Direkte_Ausbeutung"),
            ("Invasive gebietsfremde Arten", "Invasive_gebietsfremde_Arten"),
            ("Umweltverschmutzung", "Umweltverschmutzung"),
            ("Sonstige", "Sonstige")
        ]
        
        auswirkung_auf_zustand_der_Arten = [
            ("Populationsgröße von Arten", "Populationsgröße_von_Arten"),
            ("Globales Ausrottungsrisiko von Arten", "Globales_Ausrottungsrisiko_von_Arten")
        ]
    
        auswirkung_auf_Oekosysteme = [
            ("Landdegradation", "Landdegradation"),
            ("Wüstenbildung", "Wüstenbildung"),
            ("Bodenversiegelung", "Bodenversiegelung")
        ]
    
        Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistunge = [
            ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", "Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistungen")
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
            ("Ressourcenzuflüsse, einschließlich Ressourcennutzung", "Ressourcenzuflüsse,_einschließlich_Ressourcennutzung"),
            ("Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen", "Ressourcenabflüsse_im_Zusammenhang_mit_Produkten_und_Dienstleistungen"),
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
            ("Angemessene Entlohnung", "Angemessene_Entlohnung"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"),
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"),
        ]

        gleichbehandlung_und_chancengleichheit = [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"),
            ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"),
            ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"),
            ("Vielfalt", "Vielfalt"),
        ]

        sonstige_arbeitsbezogene_rechte = [
            ("Kinderarbeit", "Kinderarbeit"),
            ("Zwangarbeit", "Zwangarbeit"),
            ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"),
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
            ("Angemessene Entlohnung", "Angemessene_Entlohnung"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Beruf und Privatleben", "Vereinbarkeit_von_Beruf_und_Privatleben"),
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"),
        ]

        gleichbehandlung_und_chancengleichheit = [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"),
            ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"),
            ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"),
            ("Vielfalt", "Vielfalt"),
        ]

        sonstige_arbeitsbezogene_rechte = [
            ("Kinderarbeit", "Kinderarbeit"),
            ("Zwangarbeit", "Zwangarbeit"),
            ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"),
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
            ("Angemessene Unterbringungen", "Angemessene_Unterbringungen"),
            ("Angemessene Ernährung", "Angemessene_Ernährung"),
            ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"),
            ("Bodenbezogene Auswirkungen", "Bodenbezogene_Auswirkungen"),
            ("Sicherheitsbezogene Auswirkungen", "Sicherheitsbezogene_Auswirkungen"),
        ]

        bürgerrechte_und_politische_rechte = [
            ("Meinungsfreiheit", "Meinungsfreiheit"),
            ("Versammlungsfreiheit", "Versammlungsfreiheit"),
            ("Auswirkungen auf Menschenrechtsverteidiger", "Auswirkungen_auf_Menschenrechtsverteidiger"),
        ]

        rechte_von_indigenen_völkern = [
            ("Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung", "Freiwillige_und_in_Kenntnis_der_Sachlage_erteilte_vorherige_Zustimmung"),
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
            ("Zugang zu (hochwertigen) Informationen", "Zugang_zu_(hochwertigen)_Informationen"),   
        ]

        persönliche_sicherheit_von_verbrauchern_und_endnutzern = [
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"),
            ("Persönliche Sicherheit", "Persönliche_Sicherheit"),
            ("Kinderschutz", "Kinderschutz"),
        ]

        soziale_inklusion_von_verbrauchern_und_endnutzern = [
            ("Nichtdiskriminierung", "Nichtdiskriminierung"),
            ("Zugang zu Produkten und Dienstleistungen", "Zugang_zu_Produkten_und_Dienstleistungen"),
            ("Verantwortliche Vermarktungspraktiken", "Verantwortliche_Vermarktungspraktiken"),
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

    def G1_Unternehmenspolitik(self):
        topics = [
            ("Unternehmenskultur", "Unternehmenskultur"),
            ("Schutz von Hinweisgebern (Whistleblowers)", "Schutz_von_Hinweisgebern_(Whistleblowers)"),
            ("Tierschutz", "Tierschutz"),
            ("Politisches Engagement und Lobbytätigkeiten", "Politisches_Engagement_und_Lobbytätigkeiten"),
            ("Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken", "Management_der_Beziehungen_zu_Lieferanten,_einschließlich_Zahlungspraktiken"),
            ("Vermeidung und Aufdeckung einschließlich Schulung", "Vermeidung_und_Aufdeckung_einschließlich_Schulung"),
            ("Vorkommnisse", "Vorkommnisse"),
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
                checkbox_key = f"{header}_{key}_G1"
                value = cols[i + 1].checkbox("Select", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key, label_visibility='collapsed')
                current_selection[checkbox_key] = value

        st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}
    
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

    def display_G1_Unternehmenspolitik(self):
        self.G1_Unternehmenspolitik()
        col1, col2 = st.columns([5, 0.8])
        with col1:
            pass
        with col2:
            button = st.button("Auswahl speichern", key = 'Button_Unternehmenspolitik')
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

        



