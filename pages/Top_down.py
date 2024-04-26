import streamlit as st
import pandas as pd

class ProductSelection:
    def __init__(self):
        # Initialize the product selection states if not already present
        self.initialize_state()

    def initialize_state(self):
        climate_change = ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie']
        pollution_topics = ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung',
                            'Verschmutzung von lebenden Organismen und Nahrungsressourcen',
                            'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik']
        water_usage_topics = ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser',
                              'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen']
        biodiversity_topics = ['Klimawandel', 'Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen', 'Direkte Ausbeutung', 
                               'Invasive gebietsfremde Arten', 'Umweltverschmutzung', 'Sonstige', 'Populationsgröße von Arten',
                               'Globales Ausrottungsrisiko von Arten', 'Landdegradation', 'Wüstenbildung', 'Bodenversiegelung', 'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']
        circular_economy = ['Ressourcenzuflüsse, einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle']
        eigene_belegschaft = ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Berufs- und Privatleben', 'Gesundheitsschutz und Sicherheit', 'Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen','Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','Vielfalt', 'Kinderarbeit', 'Zwangsarbeit', 'Angemessene Unterbringung','Datenschutz']
        wertschöpfungskette_belegschaft = ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Berufs- und Privatleben', 'Gesundheitsschutz und Sicherheit', 'Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen','Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','Vielfalt', 'Kinderarbeit', 'Zwangsarbeit', 'Angemessene Unterbringung','Datenschutz']
        betroffene_gemeinschaften = ['Angemessene Unterbringung', 'Angemessene Ernährung', 'Wasser- und Sanitäreinrichtungen', 'Bodenbezogene Auswirkungen', 'Sicherheitsbezogene Auswirkungen', 'Meinungsfreiheit', 'Versammlungsfreiheit', 'Auswirkungen auf Menschenrechtsverteidiger', 'Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung', 'Selbstbestimmung', 'Kulturelle Rechte'] 
        verbraucher_und_endnutzer = ['Datenschutz', 'Meinungsfreiheit', 'Zugang zu (hochwertigen) Informationen', 'Gesundheitsschutz und Sicherheit', 'Persönliche Sicherheit', 'Kinderschutz', 'Nichtdiskriminierung', 'Zugang zu Produkten und Dienstleistungen', 'Verantwortliche Vermarktungspraktiken']
        unternehmenspolitik = ['Unternehmenskultur', 'Schutz von Hinweisgebern (Whistleblowers)', 'Tierschutz', 'Politisches Engagement und Lobbytätigkeiten', 'Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken', 'Vermeidung und Aufdeckung von Korruption und Bestechung einschließlich Schulung', 'Vorkomnisse von Korruption und Bestechung']
        options = {'Wesentlich': False, 'Eher Wesentlich': False,'Eher nicht Wesentlich': False, 'Nicht Wesentlich': False}
        
        for product in climate_change:
            if f'climate_change_{product}' not in st.session_state:
                st.session_state[f'climate_change_{product}'] = options.copy()

        for product in pollution_topics:
            if f'pollution_{product}' not in st.session_state:
                st.session_state[f'pollution_{product}'] = options.copy()

        for product in water_usage_topics:
            if f'water_usage_{product}' not in st.session_state:
                st.session_state[f'water_usage_{product}'] = options.copy()

        for product in biodiversity_topics:
            if f'biodiversity_{product}' not in st.session_state:
                st.session_state[f'biodiversity_{product}'] = options.copy()

        for product in circular_economy:
            if f'kreislaufwirtschaft_{product}' not in st.session_state:
                st.session_state[f'kreislaufwirtschaft_{product}'] = options.copy()

        for product in eigene_belegschaft:
            if f'eigene_belegschaft_{product}' not in st.session_state:
                st.session_state[f'eigene_belegschaft_{product}'] = options.copy()
    
        for product in wertschöpfungskette_belegschaft:
            if f'wertschöpfungskette_belegschaft_{product}' not in st.session_state:
                st.session_state[f'wertschöpfungskette_belegschaft_{product}'] = options.copy()

        for product in betroffene_gemeinschaften:
            if f'betroffene_gemeinschaften_{product}' not in st.session_state:
                st.session_state[f'betroffene_gemeinschaften_{product}'] = options.copy()

        for product in verbraucher_und_endnutzer:
            if f'verbraucher_endnutzer_{product}' not in st.session_state:
                st.session_state[f'verbraucher_endnutzer_{product}'] = options.copy()

        for product in unternehmenspolitik:
            if f'unternehmenspolitik_{product}' not in st.session_state:
                st.session_state[f'unternehmenspolitik_{product}'] = options.copy()

    def create_options_row(self, options, topics, prefix=''):
        for topic in topics:
            row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
            row[0].write(f"{topic}:")
            for i, option in enumerate(options):
                key = f'{prefix}_{topic}_{option}'  # Add the prefix to the key
                current_value = st.session_state[f'{prefix}_{topic}'][option]
                st.session_state[f'{prefix}_{topic}'][option] = row[i+1].checkbox(" ", value=current_value, key=key)

    def display_climate_change(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        climate_change_data = {
            "Klimawandel": ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie']
        }
        st.header('Klimawandel')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in climate_change_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='climate_change')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_climate_change = button_row[1].button("Auswahl speichern", key='climate_change_button_key')
        if submitted_climate_change:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_pollution_topics(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        pollution_data = {
            "Umweltverschmutzung": ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung',
                              'Verschmutzung von lebenden Organismen und Nahrungsressourcen',
                              'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik']
        }
        st.header('Umweltverschmutzung')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in pollution_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='pollution')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_pollution = button_row[1].button("Auswahl speichern", key='pollution_button_key')
        if submitted_pollution:
            st.success("Auswahl erfolgreich gespeichert!")
    
    def display_water_usage_topics(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        water_usage_data = {
            "Wasser- & Meeresressourcen": ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser',
                              'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen']
        }
        st.header('Wasser- & Meeresressourcen')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in water_usage_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='water_usage')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_water_usage = button_row[1].button("Auswahl speichern", key='water_usage_button_key')
        if submitted_water_usage:
            st.success("Auswahl erfolgreich gespeichert!")
    
    def display_biodiversity_topics(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        biodiversity_data = {
            "Direkte Ursachen des Biodiversitätsverlusts": ["Klimawandel", "Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen", "Direkte Ausbeutung", "Invasive gebietsfremde Arten", "Umweltverschmutzung", "Sonstige"],
            "Auswirkungen auf den Zustand der Arten": ["Populationsgröße von Arten", "Globales Ausrottungsrisiko von Arten"],
            "Auswirkungen auf den Umfang und den Zustand von Ökosystemen": ["Landdegradation", "Wüstenbildung", "Bodenversiegelung"],
            "Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen": ["Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen"]
        }
        st.header('Biodiversität')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in biodiversity_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='biodiversity')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_biodiversity = button_row[1].button("Auswahl speichern", key='biodiversity_button_key')
        if submitted_biodiversity:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_circular_economy(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        kreislaufwirtschaft_data = {
            "Kreislaufwirtschaft": ['Ressourcenzuflüsse, einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle']
        }
        st.header('Kreislaufwirtschaft')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in kreislaufwirtschaft_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='kreislaufwirtschaft')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_kreislaufwirtschaft = button_row[1].button("Auswahl speichern", key='kreislaufwirtschaft_button_key')
        if submitted_kreislaufwirtschaft:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_eigene_belegschaft(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        eigene_belegschaft_data = {
            "Arbeitsbedingungen":['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Berufs- und Privatleben', 'Gesundheitsschutz und Sicherheit'],
            "Gleichbehandlung und Chanchengleichheit":['Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen','Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','Vielfalt'],
            "Sonstige arbeitsbezogene Rechte":['Kinderarbeit', 'Zwangsarbeit', 'Angemessene Unterbringung','Datenschutz']
        }
        st.header('Eigene Belegschaft')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in eigene_belegschaft_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                 self.create_options_row(options, topics, prefix='eigene_belegschaft')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_eigene_belegschaft = button_row[1].button("Auswahl speichern", key='eigene_belegschaft_button_key')
        if submitted_eigene_belegschaft:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_wertschöpfungskette_belegschaft(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        wertschöpfungskette_belegschaft_data = {
            "Arbeitsbedingungen":['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Berufs- und Privatleben', 'Gesundheitsschutz und Sicherheit'],
            "Gleichbehandlung und Chanchengleichheit":['Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen','Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','Vielfalt'],
            "Sonstige arbeitsbezogene Rechte":['Kinderarbeit', 'Zwangsarbeit', 'Angemessene Unterbringung','Datenschutz']
        }
        st.header('Wertschöpfungskette Belegschaft')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in wertschöpfungskette_belegschaft_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='wertschöpfungskette_belegschaft')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_eigene_belegschaft = button_row[1].button("Auswahl speichern", key='wertschöpfungskette_belegschaft_button_key')
        if submitted_eigene_belegschaft:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_betroffene_gemeinschaft(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        betroffene_gemeinschaften_data = {
            "Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften": ['Angemessene Unterbringung', 'Angemessene Ernährung', 'Wasser- und Sanitäreinrichtungen', 'Bodenbezogene Auswirkungen', 'Sicherheitsbezogene Auswirkungen'],
            "Bürgerrechte und politische Rechte von Gemeinschaften": ['Meinungsfreiheit', 'Versammlungsfreiheit', 'Auswirkungen auf Menschenrechtsverteidiger'],
            "Rechte indigener Völker": ['Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung', 'Selbstbestimmung', 'Kulturelle Rechte']
        }
        st.header('Betroffene Gemeinschaften')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in betroffene_gemeinschaften_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='betroffene_gemeinschaften')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_betroffene_gemeinschaften = button_row[1].button("Auswahl speichern", key='betroffene_gemeinschaften_button_key')
        if submitted_betroffene_gemeinschaften:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_verbraucher_endnutzer(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        verbraucher_endnutzer_data = {
            "Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer": ['Datenschutz', 'Meinungsfreiheit', 'Zugang zu (hochwertigen) Informationen'],
            "Persönliche Sicherheit von Verbrauchern und/oder Endnutzern": ['Gesundheitsschutz und Sicherheit', 'Persönliche Sicherheit', 'Kinderschutz'],
            "Soziale Inklusion von Verbrauchern und/oder Endnutzern":['Nichtdiskriminierung', 'Zugang zu Produkten und Dienstleistungen', 'Verantwortliche Vermarktungspraktiken']
        }
        st.header('Verbraucher und Endnutzer')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in verbraucher_endnutzer_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='verbraucher_endnutzer')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_verbraucher_endnutzer = button_row[1].button("Auswahl speichern", key='verbraucher_endnutzer_button_key')
        if submitted_verbraucher_endnutzer:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_unternehmenspolitik(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        unternehmenspolitik_data = {
            "Unternehmenspolitik": ['Unternehmenskultur', 'Schutz von Hinweisgebern (Whistleblowers)', 'Tierschutz', 'Politisches Engagement und Lobbytätigkeiten', 'Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken']
        }
        st.header('Unternehmenspolitik')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.33])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        for category, topics in unternehmenspolitik_data.items():
            st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
            if topics:
                self.create_options_row(options, topics, prefix='unternehmenspolitik')
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_unternehmenspolitik = button_row[1].button("Auswahl speichern", key='unternehmenspolitik_button_key')
        if submitted_unternehmenspolitik:
            st.success("Auswahl erfolgreich gespeichert!")


def display_page():
    st.title("Top-Down-Analyse")
    st.markdown("""
        Zur Erstellung einer Liste von potentiellen Nachhaltigekitsthemen, gilt es wesentliche Inhalte zu identifizieren.
        Wählen Sie die entsprechenden Kategorien aus und bewerten Sie die Inhalte anhand deren Wesentlichkeit.       
    """)
    selection = ProductSelection()
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Klimawandel", "Umweltverschmutzung", "Wasser- & Meeresressourcen", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Lieferkette Belegschaft", "Betroffene Gemeinschaften", "Verbraucher & Endnutzer", "Unternehmenspolitik"])
    with tab1:
        selection.display_climate_change()
    with tab2:
        selection.display_pollution_topics()
    with tab3:
        selection.display_water_usage_topics()
    with tab4:
        selection.display_biodiversity_topics()
    with tab5:
        selection.display_circular_economy()
    with tab6:
        selection.display_eigene_belegschaft()
    with tab7:
        selection.display_wertschöpfungskette_belegschaft()
    with tab8:
        selection.display_betroffene_gemeinschaft()
    with tab9:
        selection.display_verbraucher_endnutzer()
    with tab10:
        selection.display_unternehmenspolitik()











