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
        options = {'Wesentlich': False, 'Eher Wesentlich': False,'Eher nicht Wesentlich': False, 'Nicht Wesentlich': False}
        for product in climate_change + pollution_topics + water_usage_topics + biodiversity_topics:
            if product not in st.session_state:
                st.session_state[product] = options.copy()

    def create_options_row(self, options, topics):
        for topic in topics:
            row = st.columns([2, 0.3, 0.3, 0.4, 0.3])
            row[0].write(f"{topic}:")
            for i, option in enumerate(options):
                current_value = st.session_state[topic][option]
                st.session_state[topic][option] = row[i+1].checkbox(" ", value=current_value, key=f"{topic}_{option}")

    def display_climate_change_form(self):
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

    def display_pollution_form(self):
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

    def display_water_usage_form(self):
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

    def display_biodiversity_form(self):
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

def display_page():
    selection = ProductSelection()
    tab1, tab2, tab3, tab4 = st.tabs(["Klimawandel", "Umeltverschmutzung", "Wassernutzung", "Biodiversität"])
    with tab1:
        selection.display_climate_change_form()
    with tab2:
        selection.display_pollution_form()
    with tab3:
        selection.display_water_usage_form()
    with tab4:
        selection.display_biodiversity_form()











