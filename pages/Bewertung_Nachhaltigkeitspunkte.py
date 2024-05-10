import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pages.Bottom_up_stakeholder import stakeholder_punkte

def stakeholder_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Bottom_up_stakeholder.py über session_state
    if 'stakeholder_punkte_df' not in st.session_state:
        st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "NumericalRating"])
    df3 = st.session_state.stakeholder_punkte_df.copy()
    df3['Quelle'] = 'Stakeholder'

    # Berechnen Sie die Größe der Klassen
    class_size = (df3['NumericalRating'].max() - df3['NumericalRating'].min()) / 4

    # Fügen Sie einen Schieberegler in der Seitenleiste hinzu
    options = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']
    st.sidebar.markdown("---")
    st.sidebar.text("Grenzwert für die Auswahl der Stakeholderpunkte:")
    
    # Überprüfen, ob 'slider_value' bereits im session_state gespeichert ist, wenn nicht, initialisieren Sie es mit einem Standardwert
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = options[0]
    
    # Speichern Sie den aktuellen Zustand des Schiebereglers
    current_slider_value = st.session_state.slider_value
    
    # Aktualisieren Sie 'slider_value' im session_state, wenn der Benutzer den Schieberegler bewegt
    st.session_state.slider_value = st.sidebar.select_slider('', options=options, value=st.session_state.slider_value)
    
    # Wenn der Wert des Schiebereglers geändert wurde, führen Sie st.experimental_rerun() aus, um die Seite neu zu laden
    if st.session_state.slider_value != current_slider_value:
        st.experimental_rerun()
    
    st.markdown("""
        <style>
        .st-emotion-cache-183lzff,
        .st-emotion-cache-1inwz65 {
            font-family: "Source Sans Pro", sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)
    
    
    # Berechnen Sie die Anzahl der ausgewählten Zeilen basierend auf der Auswahl
    if st.session_state.slider_value == 'Wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > 3 * class_size + df3['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher Wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > 2 * class_size + df3['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher nicht wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > class_size + df3['NumericalRating'].min()]
    else:  # Nicht Wesentlich
        selected_rows_st = df3[df3['NumericalRating'] > 0]
    
    # Speichern Sie die ausgewählten Zeilen im session_state
    st.session_state.selected_rows_st = selected_rows_st
    
    return selected_rows_st

def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
    # Erstellen Sie eine Kopie von df2
    df4 = st.session_state.df2.copy()
    df4['Quelle'] = 'Eigene'
    return df4

def Top_down_Nachhaltigkeitspunkte():
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

def initialize_bewertet_column(longlist):
    if 'selected_data' in st.session_state:
        longlist['Bewertet'] = longlist['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        longlist['Bewertet'] = 'Nein'
    return longlist

def submit_bewertung(longlist, bewertung):
    if st.button("Bewertung absenden") and bewertung:
        if 'selected_rows' in st.session_state:
            new_data = pd.DataFrame(st.session_state['selected_rows'])
            if '_selectedRowNodeInfo' in new_data.columns:
                new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)
            new_data['Bewertung'] = bewertung
            if 'selected_data' in st.session_state:
                st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
            else:
                st.session_state.selected_data = new_data
            longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
    return longlist

def display_selected_data():
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        st.write("Bewertetes DataFrame:")
        st.dataframe(st.session_state.selected_data)

def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    grid_options = gb.build()
    grid_response = AgGrid(longlist, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    st.session_state['selected_rows'] = grid_response['selected_rows']

def merge_dataframes():
    # Abrufen der Daten von verschiedenen Quellen
    df4 = eigene_Nachhaltigkeitspunkte()
    df_essential = Top_down_Nachhaltigkeitspunkte()
    selected_rows_st = stakeholder_Nachhaltigkeitspunkte()

    # Kombinieren der Daten in einem DataFrame
    combined_df = pd.concat([df_essential, df4, selected_rows_st], ignore_index=True)

    # Entfernen von Zeilen, die nur NaN-Werte enthalten
    combined_df = combined_df.dropna(how='all')

    # Entfernen von führenden und nachfolgenden Leerzeichen in den Spalten 'Thema', 'Unterthema' und 'Unter-Unterthema'
    combined_df['Thema'] = combined_df['Thema'].str.strip()
    combined_df['Unterthema'] = combined_df['Unterthema'].str.strip()
    combined_df['Unter-Unterthema'] = combined_df['Unter-Unterthema'].str.strip()

    # Entfernen von Zeilen, in denen das 'Thema' NaN ist
    combined_df = combined_df.dropna(subset=['Thema'])

    # Gruppieren der Daten nach 'Thema', 'Unterthema' und 'Unter-Unterthema' und Zusammenführen der 'Quelle'-Werte
    combined_df = combined_df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema']).agg({'Quelle': lambda x: ' & '.join(sorted(set(x)))}).reset_index()

    # Entfernen von Duplikaten und Sortieren der Daten
    combined_df = combined_df.drop_duplicates(subset=['Thema', 'Unterthema', 'Unter-Unterthema']).sort_values(by=['Thema', 'Unterthema', 'Unter-Unterthema'])

    # Hinzufügen einer 'ID'-Spalte
    combined_df.insert(0, 'ID', range(1, 1 + len(combined_df)))

    # Erstellen eines neuen DataFrame 'longlist', um Probleme mit der Zuordnung von 'selected_rows' zu vermeiden
    longlist = pd.DataFrame(combined_df)

    # Initialisieren der 'Bewertet'-Spalte in 'longlist'
    longlist = initialize_bewertet_column(longlist)

    # Erstellen einer Auswahlbox für die Bewertung
    bewertung = st.selectbox("Bewertung auswählen:", ["", "Gut", "Mittel", "Schlecht"])

    # Einreichen der Bewertung und Aktualisieren der 'longlist'
    longlist = submit_bewertung(longlist, bewertung)

    # Anzeigen der ausgewählten Daten
    display_selected_data()

    # Anzeigen der 'longlist' in einem Grid
    display_grid(longlist)

def display_page():
    tab1, tab2, tab3 = st.tabs(["Eigene Nachhaltigkeitspunkte", "Stakeholder", "Gesamtübersicht"])
    with tab1: 
        merge_dataframes()   
    with tab2:
        stakeholder_punkte()
    with tab3:
        st.write("Gesamtübersicht")



