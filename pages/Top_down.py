import streamlit as st

class ProductSelection:
    def __init__(self):
        # Initialize the product selection states if not already present
        self.initialize_state()

    def initialize_state(self):
        # Ensure each product has all options initialized in the session state
        climate_change = ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie']
        pollution_topics = ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung',
                            'Verschmutzung von lebenden Organismen und Nahrungsressourcen',
                            'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik']
        water_usage_topics = ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser',
                              'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen']
        biodiversity_topics = ['Klimawandel', 'Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen', 'Direkte Ausbeutung', 
                               'Invasive gebietsfremde Arten', 'Umweltverschmutzung', 'Sonstige', 'Populationsgröße von Arten',
                               'Globales Ausrottungsrisiko von Arten', 'Landdegradation', 'Wüstenbildung', 'Bodenversiegelung', 'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']
        kreislaufwirtschaft = ['Ressourcenzuflüsse einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle']
        eigene_belegschaft = ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Berufs- und Privatleben', 'Gesundheitsschutz und Sicherheit', 'Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen','Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','Vielfalt', 'Kinderarbeit', 'Zwangsarbeit', 'Angemessene Unterbringung','Datenschutz']
        options = {'Wesentlich': False, 'Eher Wesentlich': False,'Eher nicht Wesentlich': False, 'Nicht Wesentlich': False}
        for product in climate_change + pollution_topics + water_usage_topics + biodiversity_topics + kreislaufwirtschaft + eigene_belegschaft:
            if product not in st.session_state:
                st.session_state[product] = options.copy()

    def create_options_row(self, options, topics):
        for topic in topics:
            row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
            row[0].write(f"{topic}:")
            for i, option in enumerate(options):
                current_value = st.session_state[topic][option]
                st.session_state[topic][option] = row[i+1].checkbox(" ", value=current_value, key=f"{topic}_{option}")

    def display_climate_change(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']     
        st.header('Klimawandel')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        self.create_options_row(options, ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'])
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted = button_row[1].button("Auswahl speichern", key='climate_change_button_key')
        if submitted:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_pollution(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        st.header('Umweltverschmutzung')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        self.create_options_row(options, ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung',
                                              'Verschmutzung von lebenden Organismen und Nahrungsressourcen',
                                              'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik'])
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_pollution = button_row[1].button("Auswahl speichern", key='pollution_button_key')
        if submitted_pollution:
            st.success("Auswahl erfolgreich gespeichert!")      

    def display_water_usage(self):
        options = ['Wesentlich', 'Eher Wesentlich', 'Eher nicht Wesentlich', 'Nicht Wesentlich']
        st.header('Wassernutzung')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        self.create_options_row(options, ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser',
                                              'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen'])
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_water_usage = button_row[1].button("Auswahl speichern", key='water_usage_button_key')
        if submitted_water_usage:
            st.success("Auswahl erfolgreich gespeichert!")

    def display_biodiversity(self):
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
                self.create_options_row(options, topics)
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
        st.header('Kreislaufwirtschaft')
        # Create a row for the headers
        header_row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")
        self.create_options_row(options, ['Ressourcenzuflüsse einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle'])
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted = button_row[1].button("Auswahl speichern", key='circular_economy_button_key')
        if submitted:
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
                self.create_options_row(options, topics)
            else:
                st.write("Keine spezifischen Themen verfügbar.")
        
        # Create some empty space
        st.markdown("<br>"*2, unsafe_allow_html=True)
        # Create a row for the button
        button_row = st.columns([4, 1])
        submitted_eigene_belegschaft = button_row[1].button("Auswahl speichern", key='eigene_belegschaft_button_key')
        if submitted_eigene_belegschaft:
            st.success("Auswahl erfolgreich gespeichert!")

def display_page():
    st.title("Top-Down-Analyse")
    st.markdown("""
        Zur Erstellung einer Liste von potentiellen Nachhaltigekitsthemen, gilt es wesentliche Inhalte zu identifizieren.
        Wählen Sie die entsprechenden Kategorien aus und bewerten Sie die Inhalte anhand deren Wesentlichkeit.
        
    """)
    selection = ProductSelection()
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Klimawandel", "Umeltverschmutzung", "Wassernutzung", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Wertschöpfungskette Belegschaft"])
    with tab1:
        selection.display_climate_change()
    with tab2:
        selection.display_pollution()
    with tab3:
        selection.display_water_usage()
    with tab4:
        selection.display_biodiversity()
    with tab5:
        selection.display_circular_economy()
    with tab6:
        selection.display_eigene_belegschaft()
    with tab7:
        selection.display_wertschöpfungskette_belegschaft()











