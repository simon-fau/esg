import streamlit as st
import pandas as pd

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
    



    import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def stakeholder_punkte():
    if 'df3' not in st.session_state:
        st.session_state.df3 = pd.DataFrame({
            "Platzierung": [""] * 5,
            "Thema": [""] * 5,
            "Unterthema": [""] * 5,
            "Unter-Unterthema": [""] * 5,
            "NumericalRating": [""] * 5
        })

    with st.sidebar:
        st.markdown("---")
        thema = st.selectbox('Thema auswählen',
        options=[
            'Klimawandel', 
            'Umweltverschmutzung', 
            'Wasser- und Meeresressourcen', 
            'Biologische Vielfalt und Ökosysteme', 
            'Kreislaufwirtschaft',
            'Eigene Belegschaft',
            'Arbeitskräfte in der Wertschöpfungskette',
            'Betroffene Gemeinschaften',
            'Verbraucher und End-nutzer',
            'Unternehmenspolitik'
            ], 
        index=0, 
        key='thema'
    )
    
        if thema == 'Klimawandel':
            unterthema_options = ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie']
        elif thema == 'Umweltverschmutzung':
            unterthema_options = [
                'Luftverschmutzung', 
                'Wasserverschmutzung', 
                'Bodenverschmutzung', 
                'Verschmutzung von lebenden Organismen und Nahrungsressourcen', 
                'Besorgniserregende Stoffe', 
                'Mikroplastik'
            ]
        elif thema == 'Wasser- und Meeresressourcen':
            unterthema_options = ['Wasser', 'Meeresressourcen']
        elif thema == 'Biologische Vielfalt und Ökosysteme':
            unterthema_options = [
                'Direkte Ursachen des Biodiversitätsverlusts', 
                'Auswirkungen auf den Zustand der Arten', 
                'Auswirkungen auf den Umfang und den Zustand von Ökosystemen'
            ]
        elif thema == 'Kreislaufwirtschaft':
            unterthema_options = [
                'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen', 
                'Ressourcenzuflüsse, einschließlich Ressourcennutzung', 
                'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 
                'Abfälle'
            ]
        elif thema == 'Eigene Belegschaft':
            unterthema_options = [
                'Arbeitsbedingungen',
                'Gleichbehandlung und Chancengleichheit für alle',
                'Sonstige arbeitsbezogene Rechte'
            ]
        elif thema == 'Arbeitskräfte in der Wertschöpfungskette':
            unterthema_options = [
                'Arbeitsbedingungen',
                'Gleichbehandlung und Chancengleichheit für alle',
                'Sonstige arbeitsbezogene Rechte'
            ]
        elif thema == 'Betroffene Gemeinschaften':
            unterthema_options = [
                'Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften',
                'Bürgerrechte und politische Rechte von Gemeinschaften',
                'Rechte indigener Völker'
            ]
        elif thema == 'Verbraucher und End-nutzer':
            unterthema_options = [
                'Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer',
                'Persönliche Sicherheit von Verbrauchern und/oder Endnutzern',
                'Soziale Inklusion von Verbrauchern und/oder Endnutzern'
            ]

        elif thema == 'Unternehmenspolitik':
            unterthema_options = [
                'Unternehmenskultur',
                'Schutz von Hinweisgebern (Whistleblowers)',
                'Tierschutz',
                'Politisches Engagement und Lobbytätigkeiten',
                'Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken',
                'Korruption und Bestechung'
            ]

        unterthema = st.selectbox('Unterthema auswählen', options=unterthema_options, index=0, key='unterthema1')
        unter_unterthema = st.text_input('Unter-Unterthema eingeben', key='unter_unterthema1')    
        add_row = st.button('Hinzufügen', key='add_row1')

        if add_row:
            empty_row_index = st.session_state.df3[(st.session_state.df3["Thema"] == "") & (st.session_state.df3["Unterthema"] == "") & (st.session_state.df3["Unter-Unterthema"] == "")].first_valid_index()
            if empty_row_index is not None:
                st.session_state.df3.at[empty_row_index, "Thema"] = thema
                st.session_state.df3.at[empty_row_index, "Unterthema"] = unterthema
                st.session_state.df3.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
            else:
                new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
                st.session_state.df3 = st.session_state.df3._append(new_row, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df3)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    grid_response = AgGrid(
        st.session_state.df3.reset_index(),
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,
        width='100%',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        return_mode=DataReturnMode.__members__['AS_INPUT'],  # Adjust the DataReturnMode as per available options
        selection_mode='multiple'
    )

    add_empty_row = st.button('Leere Zeile hinzufügen', key='add_empty_row')
    if add_empty_row:
        empty_row = {"Thema": "", "Unterthema": "", "Unter-Unterthema": ""}
        st.session_state.df3 = st.session_state.df3._append(empty_row, ignore_index=True)
        st.experimental_rerun()

    delete_rows = st.button('Ausgewählte Zeilen löschen', key='delete_rows')
    if delete_rows:
        selected_rows = grid_response['selected_rows']
        selected_indices = [row['index'] for row in selected_rows]
        st.session_state.df3 = st.session_state.df3.drop(selected_indices)
        st.experimental_rerun()

    save_changes = st.button('Änderungen speichern', key='save_changes')
    if save_changes:
        st.session_state.df3 = grid_response['data'].set_index('index')