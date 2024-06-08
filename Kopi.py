import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def display_page():
    # Erstellen eines Beispieldatenrahmens
    data = {
        "ID": [1, 2, 3, 4],
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40]
    }
    df = pd.DataFrame(data)

    # Initialisieren der Spalte 'Bewertet' mit 'Nein' für alle Zeilen
    if 'selected_data' in st.session_state:
        # Update 'Bewertet' basierend auf vorhandenen Bewertungen
        df['Bewertet'] = df['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        df['Bewertet'] = 'Nein'
    
    # Erstellen der Bewertungsauswahl
    bewertung = st.selectbox("Bewertung auswählen:", ["", "Gut", "Mittel", "Schlecht"])

    # Button zum Absenden der Bewertung
    if st.button("Bewertung absenden") and bewertung:
        if 'selected_rows' in st.session_state:
            new_data = pd.DataFrame(st.session_state['selected_rows'])
            # Entfernen der Spalte _selectedRowNodeInfo
            if '_selectedRowNodeInfo' in new_data.columns:
                new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)
            new_data['Bewertung'] = bewertung  # Hinzufügen der Bewertung zu den ausgewählten Zeilen
            
            # Prüfen, ob bereits Daten im Session State gespeichert sind
            if 'selected_data' in st.session_state:
                # Anhängen der neuen Daten an das bestehende DataFrame
                st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
            else:
                # Speichern des neuen DataFrame im Session State
                st.session_state.selected_data = new_data
            
            # Aktualisieren der 'Bewertet' Spalte im Haupt-DataFrame
            df['Bewertet'] = df['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
        
    # Anzeigen des DataFrame, wenn es im Session State gespeichert ist und Inhalt hat
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        st.write("Bewertetes DataFrame:")
        st.dataframe(st.session_state.selected_data)

    # Erstellen der Grid-Optionen
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    grid_options = gb.build()

    # Anzeigen des AgGrid
    grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)

    # Speichern der ausgewählten Zeilen im Session State
    st.session_state['selected_rows'] = grid_response['selected_rows']

display_page()



 # Initialize a list to store topic details
    essential_topics_data = []
    # Anpassung der Inahlte für die Tabelle aus der Top_down.py, für Inhalte nur mit Thema und Unterthema
    for topic, values in st.session_state.items():
        if isinstance(values, dict):
            if values.get('Wesentlich', False) or values.get('Eher Wesentlich', False):
                # Assuming topic names are stored in the format "Thema - Unterthema - Unter-Unterthema"
                topic_details = topic.split(' - ')
                while len(topic_details) < 3:
                    topic_details.append('')
                # Check if the topic starts with "climate_change", "pollution_" or "water_usage_" and change the theme and subtheme accordingly
                if topic_details[0].startswith('climate_change'):
                    topic_details = ['Klimawandel', topic_details[0].replace('climate_change', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('pollution_'):
                    topic_details = ['Umweltverschmutzung', topic_details[0].replace('pollution_', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('water_usage_'):
                    topic_details = ['Wasser- & Meeresressourcen', topic_details[0].replace('water_usage_', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('kreislaufwirtschaft'):
                    topic_details = ['Kreislaufwirtschaft', topic_details[0].replace('kreislaufwirtschaft', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('unternehmenspolitik'):
                    topic_details = ['Unternehmenspolitik', topic_details[0].replace('unternehmenspolitik', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('biodiversity_'):
                    if topic_details[0] in ['biodiversity_Populationsgröße von Arten', 'biodiversity_Globales Ausrottungsrisiko von Arten']:
                        topic_details = ['Biodiversität', 'Auswirkungen auf den Zustand der Arten', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['biodiversity_Landdegradation', 'biodiversity_Wüstenbildung', 'biodiversity_Bodenversiegelung']:
                        topic_details = ['Biodiversität', 'Auswirkungen auf den Umfang und den Zustand von Ökosystemen', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['biodiversity_Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']:
                        topic_details = ['Biodiversität','Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    else:
                        topic_details = ['Biodiversität', 'Direkte Ursachen des Biodiversitätsverlusts', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                elif topic_details[0].startswith('eigene_belegschaft_'):
                    if topic_details[0] in ['eigene_belegschaft_Sichere Beschäftigung', 'eigene_belegschaft_Arbeitszeit', 'eigene_belegschaft_Angemessene Entlohnung', 'eigene_belegschaft_Sozialer Dialog', 'eigene_belegschaft_Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'eigene_belegschaft_Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'eigene_belegschaft_Vereinbarkeit von Berufs- und Privatleben', 'eigene_belegschaft_Gesundheitsschutz und Sicherheit']:
                        topic_details = ['Eigene Belegschaft','Arbeitsbedingungen', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['eigene_belegschaft_Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'eigene_belegschaft_Schulungen und Kompetenzentwicklung', 'eigene_belegschaft_Beschäftigung und Inklusion von Menschen mit Behinderungen', 'eigene_belegschaft_Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','eigene_belegschaft_Vielfalt']:
                        topic_details = ['Eigene Belegschaft','Gleichbehandlung und Chancengleichheit', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['eigene_belegschaft_Kinderarbeit', 'eigene_belegschaft_Zwangsarbeit', 'eigene_belegschaft_Angemessene Unterbringung', 'eigene_belegschaft_Datenschutz']:
                        topic_details = ['Eigene Belegschaft','Sonstige arbeitsbezogene Rechte', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                elif topic_details[0].startswith('wertschöpfungskette_belegschaft_'):
                    if topic_details[0] in ['wertschöpfungskette_belegschaft_Sichere Beschäftigung', 'wertschöpfungskette_belegschaft_Arbeitszeit', 'wertschöpfungskette_belegschaft_Angemessene Entlohnung', 'wertschöpfungskette_belegschaft_Sozialer Dialog', 'wertschöpfungskette_belegschaft_Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'wertschöpfungskette_belegschaft_Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'wertschöpfungskette_belegschaft_Vereinbarkeit von Berufs- und Privatleben', 'wertschöpfungskette_belegschaft_Gesundheitsschutz und Sicherheit']:
                        topic_details = ['Arbeitskräfte in der Wertschöpfungskette','Arbeitsbedingungen', topic_details[0].replace('wertschöpfungskette_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['wertschöpfungskette_belegschaft_Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'wertschöpfungskette_belegschaft_Schulungen und Kompetenzentwicklung', 'wertschöpfungskette_belegschaft_Beschäftigung und Inklusion von Menschen mit Behinderungen', 'wertschöpfungskette_belegschaft_Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','wertschöpfungskette_belegschaft_Vielfalt']:
                        topic_details = ['Arbeitskräfte in der Wertschöpfungskette','Gleichbehandlung und Chancengleichheit', topic_details[0].replace('wertschöpfungskette_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['wertschöpfungskette_belegschaft_Kinderarbeit', 'wertschöpfungskette_belegschaft_Zwangsarbeit', 'wertschöpfungskette_belegschaft_Angemessene Unterbringung', 'wertschöpfungskette_belegschaft_Datenschutz']:
                        topic_details = ['Arbeitskräfte in der Wertschöpfungskette','Sonstige arbeitsbezogene Rechte', topic_details[0].replace('wertschöpfungskette_belegschaft_', '').strip().replace('_', ' ')] 
                elif topic_details[0].startswith('betroffene_gemeinschaften_'):
                    if topic_details[0] in ['betroffene_gemeinschaften_Angemessene Unterbringung', 'betroffene_gemeinschaften_Angemessene Ernährung', 'betroffene_gemeinschaften_Wasser- und Sanitäreinrichtungen', 'betroffene_gemeinschaften_Bodenbezogene Auswirkungen', 'betroffene_gemeinschaften_Sicherheitsbezogene Auswirkungen']:
                        topic_details = ['Betroffene Gemeinschaften','Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften', topic_details[0].replace('betroffene_gemeinschaften_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['betroffene_gemeinschaften_Meinungsfreiheit', 'betroffene_gemeinschaften_Versammlungsfreiheit', 'betroffene_gemeinschaften_Auswirkungen auf Menschenrechtsverteidiger']:
                        topic_details = ['Betroffene Gemeinschaften','Bürgerrechte und politische Rechte von Gemeinschaften', topic_details[0].replace('betroffene_gemeinschaften_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['betroffene_gemeinschaften_Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung', 'betroffene_gemeinschaften_Selbstbestimmung', 'betroffene_gemeinschaften_Kulturelle Rechte' ]:
                        topic_details = ['Betroffene Gemeinschaften','Rechte indigener Völker', topic_details[0].replace('betroffene_gemeinschaften_', '').strip().replace('_', ' ')] 
                elif topic_details[0].startswith('verbraucher_endnutzer_'):
                    if topic_details[0] in ['verbraucher_endnutzer_Datenschutz', 'verbraucher_endnutzer_Meinungsfreiheit', 'verbraucher_endnutzer_Faire Geschäftspraktiken', 'verbraucher_endnutzer_Zugang zu (hochwertigen) Informationen']:
                        topic_details = ['Verbraucher und Endnutzer','Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer', topic_details[0].replace('verbraucher_endnutzer_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['verbraucher_endnutzer_Gesundheitsschutz und Sicherheit', 'verbraucher_endnutzer_Persönliche Sicherheit', 'verbraucher_endnutzer_Kinderschutz']:
                        topic_details = ['Verbraucher und Endnutzer','Persönliche Sicherheit von Verbrauchern und/oder Endnutzern', topic_details[0].replace('verbraucher_endnutzer_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['verbraucher_endnutzer_Nichtdiskriminierung', 'verbraucher_endnutzer_Zugang zu Produkten und Dienstleistungen', 'verbraucher_endnutzer_Verantwortliche Vermarktungspraktiken' ]:
                        topic_details = ['Verbraucher und Endnutzer','Soziale Inklusion von Verbrauchern und/oder Endnutzern', topic_details[0].replace('verbraucher_endnutzer_', '').strip().replace('_', ' ')] 
                
                # Append to the list with importance level
                essential_topics_data.append(topic_details + ['Wesentlich' if values.get('Wesentlich', False) else 'Eher Wesentlich'])

    # Create a DataFrame from the collected data
    df_essential = pd.DataFrame(essential_topics_data, columns=['Thema', 'Unterthema', 'Unter-Unterthema', 'Wichtigkeit'])
    df_essential['Quelle'] = 'Top-down'
    return df_essential

