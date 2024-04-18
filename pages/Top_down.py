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
        options = {'Wesentlich': False, 'Teilweise Wesentlich': False, 'Nicht Wesentlich': False}
        for product in climate_change + pollution_topics + water_usage_topics + biodiversity_topics:
            if product not in st.session_state:
                st.session_state[product] = options.copy()

    def create_options_row(self, options, topics):
        for topic in topics:
            row = st.columns([2, 0.3, 0.3, 0.3, 0.1])
            row[0].write(f"{topic}:")
            for i, option in enumerate(options):
                current_value = st.session_state[topic][option]
                st.session_state[topic][option] = row[i+1].checkbox("", value=current_value, key=f"{topic}_{option}")

    def display_climate_change_form(self):
        options = ['Wesentlich', 'Teilweise Wesentlich', 'Nicht Wesentlich']     
        with st.form("my_form"):
            st.header('Klimawandel')
             # Create a row for the headers
            header_row = st.columns([2, 0.3, 0.3, 0.3, 0.1])
            header_row[1].write("Wesentlich")
            header_row[2].write("Teilweise Wesentlich")
            header_row[3].write("Nicht Wesentlich")
            self.create_options_row(options, ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'])
            submitted = st.form_submit_button("Auswahl speichern")
            if submitted:
                st.success("Auswahl erfolgreich gespeichert!")

        # Additional form for pollution topics
        self.display_pollution_form()
        # Additional form for water usage topics
        self.display_water_usage_form()
        self.display_biodiversity_form()

    def display_pollution_form(self):
        options = ['Wesentlich', 'Teilweise Wesentlich', 'Nicht Wesentlich']
        with st.form("pollution_form"):
            st.header('Umweltverschmutzung')
             # Create a row for the headers
            header_row = st.columns([2, 0.3, 0.3, 0.3, 0.1])
            header_row[1].write("Wesentlich")
            header_row[2].write("Teilweise Wesentlich")
            header_row[3].write("Nicht Wesentlich")
            self.create_options_row(options, ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung',
                                              'Verschmutzung von lebenden Organismen und Nahrungsressourcen',
                                              'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik'])
            submitted_pollution = st.form_submit_button("Verschmutzungsauswahl speichern")
            if submitted_pollution:
                st.success("Verschmutzungsauswahl erfolgreich gespeichert!")

    def display_water_usage_form(self):
        options = ['Wesentlich', 'Teilweise Wesentlich', 'Nicht Wesentlich']
        with st.form("water_usage_form"):
            st.header('Wassernutzung')
             # Create a row for the headers
            header_row = st.columns([2, 0.3, 0.3, 0.3, 0.1])
            header_row[1].write("Wesentlich")
            header_row[2].write("Teilweise Wesentlich")
            header_row[3].write("Nicht Wesentlich")
            self.create_options_row(options, ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser',
                                              'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen'])
            submitted_water_usage = st.form_submit_button("Wassernutzungsauswahl speichern")
            if submitted_water_usage:
                st.success("Wassernutzungsauswahl erfolgreich gespeichert!")

    def display_biodiversity_form(self):
        options = ['Wesentlich', 'Teilweise Wesentlich', 'Nicht Wesentlich']
        biodiversity_data = {
            "Direkte Ursachen des Biodiversitätsverlusts": ["Klimawandel", "Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen", "Direkte Ausbeutung", "Invasive gebietsfremde Arten", "Umweltverschmutzung", "Sonstige"],
            "Auswirkungen auf den Zustand der Arten": ["Populationsgröße von Arten", "Globales Ausrottungsrisiko von Arten"],
            "Auswirkungen auf den Umfang und den Zustand von Ökosystemen": ["Landdegradation", "Wüstenbildung", "Bodenversiegelung"],
            "Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen": ["Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen"]
        }
        with st.form("biodiversity_form"):
            st.header('Biodiversität')
             # Create a row for the headers
            header_row = st.columns([2, 0.3, 0.3, 0.3, 0.1])
            header_row[1].write("Wesentlich")
            header_row[2].write("Teilweise Wesentlich")
            header_row[3].write("Nicht Wesentlich")
            for category, topics in biodiversity_data.items():
                st.markdown(f"<h6 style='font-weight: bold;'>{category}</h6>", unsafe_allow_html=True)
                if topics:
                    self.create_options_row(options, topics)
                else:
                    st.write("Keine spezifischen Themen verfügbar.")
            submitted_biodiversity = st.form_submit_button("Biodiversitätsauswahl speichern")
            if submitted_biodiversity:
                st.success("Biodiversitätsauswahl erfolgreich gespeichert!")

def display_page():
    selection = ProductSelection()
    selection.display_climate_change_form()














