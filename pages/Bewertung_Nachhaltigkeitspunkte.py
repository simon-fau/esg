import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pages.Bottom_up_stakeholder import stakeholder_punkte
import altair as alt

def stakeholder_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Bottom_up_stakeholder.py über session_state
    if 'stakeholder_punkte_df' not in st.session_state:
        st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "NumericalRating"])
    df3 = st.session_state.stakeholder_punkte_df.copy()
    df3['Quelle'] = 'Stakeholder'

    # Berechnen Sie die Größe der Klassen
    class_size = (df3['NumericalRating'].max() - df3['NumericalRating'].min()) / 4

    # Fügen Sie zwei Spalten hinzu, wobei die erste Spalte halb so breit ist wie die zweite
    col1, col2 = st.columns([1,3])
    
    # Fügen Sie einen Schieberegler in der ersten Spalte hinzu
    with col1:
        options = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']
        st.text("Grenzwert für die Auswahl der Stakeholderpunkte:")
    
        # Überprüfen, ob 'slider_value' bereits im session_state gespeichert ist, wenn nicht, initialisieren Sie es mit einem Standardwert
        if 'slider_value' not in st.session_state:
            st.session_state.slider_value = options[0]
    
        # Speichern Sie den aktuellen Zustand des Schiebereglers
        current_slider_value = st.session_state.slider_value
    
        # Aktualisieren Sie 'slider_value' im session_state, wenn der Benutzer den Schieberegler bewegt
        st.session_state.slider_value = st.select_slider('', options=options, value=st.session_state.slider_value)
    
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
    
    # Die zweite Spalte bleibt leer
    with col2:
        pass

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

def submit_bewertung(longlist, ausgewaehlte_werte):
    if st.sidebar.button("Bewertung absenden") and any(ausgewaehlte_werte.values()):
        if 'selected_rows' in st.session_state:
            new_data = pd.DataFrame(st.session_state['selected_rows'])
            if '_selectedRowNodeInfo' in new_data.columns:
                new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)

            # Zuordnung der Slider-Auswahlen zu numerischen Werten für die finanzielle Bewertung
            ausmass_finanziell_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            wahrscheinlichkeit_finanziell_mapping = {
                "Tritt nicht ein": 1, "Unwahrscheinlich": 2, "Eher unwahrscheinlich": 3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
            }
            auswirkung_finanziell_mapping = {
                "Keine": 1, "Sehr gering": 2, "Eher gering": 3, "Eher Hoch": 4, "Hoch": 5, "Sehr hoch": 6
            }
            # Zuordnung der Slider-Auswahlen zu numerischen Werten für die Auswirkungsbewertung
            ausmass_neg_tat_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_neg_tat_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_neg_tat_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            ausmass_neg_pot_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_neg_pot_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_neg_pot_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            wahrscheinlichkeit_neg_pot_mapping = {
                "Tritt nicht ein": 1, "Unwahrscheinlich": 2, "Eher unwahrscheinlich": 3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
            }
            ausmass_pos_tat_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_pos_tat_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            ausmass_pos_pot_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_pos_pot_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_pos_pot_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            
            # Kombinieren der Bewertungen zu einer String-Beschreibung
            auswirkung_string = ' ; '.join(part for part in [
                ausgewaehlte_werte.get('auswirkung_option', ''),
                ausgewaehlte_werte.get('auswirkung_art_option', ''),
                "Ausmaß: " + ausgewaehlte_werte.get('ausmass_neg_tat', '') if ausgewaehlte_werte.get('ausmass_neg_tat') else '',
                "Umfang: " + ausgewaehlte_werte.get('umfang_neg_tat', '') if ausgewaehlte_werte.get('umfang_neg_tat') else '',
                "Behebbarkeit: " + ausgewaehlte_werte.get('behebbarkeit_neg_tat', '') if ausgewaehlte_werte.get('behebbarkeit_neg_tat') else '',
                "Ausmaß: " + ausgewaehlte_werte.get('ausmass_neg_pot', '') if ausgewaehlte_werte.get('ausmass_neg_pot') else '',
                "Umfang: " + ausgewaehlte_werte.get('umfang_neg_pot', '') if ausgewaehlte_werte.get('umfang_neg_pot') else '',
                "Behebbarkeit: " + ausgewaehlte_werte.get('behebbarkeit_neg_pot', '') if ausgewaehlte_werte.get('behebbarkeit_neg_pot') else ''
            ] if part)

            new_data['Auswirkung'] = auswirkung_string
            finanziell_string = f"Ausmaß: {ausgewaehlte_werte.get('ausmass_finanziell', '')} ; Wahrscheinlichkeit: {ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', '')} ; Finanzielle Auswirkung: {ausgewaehlte_werte.get('auswirkung_finanziell', '')}"
            new_data['Finanziell'] = finanziell_string

            # Berechnung des Scores für finanzielle Bewertungen normalized_score = ((produkt - min_produkt) / (max_produkt - min_produkt)) * 99 + 1
            new_data['Score Finanzen'] = ((
                ausmass_finanziell_mapping.get(ausgewaehlte_werte.get('ausmass_finanziell', 'Keine'), 1) *
                wahrscheinlichkeit_finanziell_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', 'Keine'), 1) *
                auswirkung_finanziell_mapping.get(ausgewaehlte_werte.get('auswirkung_finanziell', 'Keine'), 1) - 1) / (216 - 1) * 99 + 1
            )

            # Berechnung Tatsächliche negative Auswirkungen
            tatsaechlich_negativ = ((
                ausmass_neg_tat_mapping.get(ausgewaehlte_werte.get('ausmass_neg_tat', 'Keine'), 1) *
                umfang_neg_tat_mapping.get(ausgewaehlte_werte.get('umfang_neg_tat', 'Keine'), 1) *
                behebbarkeit_neg_tat_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_tat', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
            )
            
            # Berechnung Potenzielle negative Auswirkungen
            potentiell_negativ = ((
                ausmass_neg_pot_mapping.get(ausgewaehlte_werte.get('ausmass_neg_pot', 'Keine'), 1) *
                umfang_neg_pot_mapping.get(ausgewaehlte_werte.get('umfang_neg_pot', 'Keine'), 1) *
                behebbarkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_pot', 'Kein Aufwand'), 1) *
                wahrscheinlichkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', 'Tritt nicht ein'), 1) - 1) / (1296 - 1) * 99 + 1
            )
            
            # Berechnung Tatsächliche positive Auswirkungen
            tatsaechlich_positiv = ((
                ausmass_pos_tat_mapping.get(ausgewaehlte_werte.get('ausmass_pos_tat', 'Keine'), 1) *
                umfang_pos_tat_mapping.get(ausgewaehlte_werte.get('umfang_pos_tat', 'Keine'), 1) - 1) / (36 - 1) * 99 + 1
            )
            
            # Berechnung Potenzielle positive Auswirkungen
            potentiell_positiv = ((
                ausmass_pos_pot_mapping.get(ausgewaehlte_werte.get('ausmass_pos_pot', 'Keine'), 1) *
                umfang_pos_pot_mapping.get(ausgewaehlte_werte.get('umfang_pos_pot', 'Keine'), 1) *
                behebbarkeit_pos_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_pos_pot', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
            )
            
            # Berechnung des Gesamtscores für die Auswirkungsbewertung
            new_data['Score Auswirkung'] = tatsaechlich_negativ * tatsaechlich_positiv * potentiell_negativ * potentiell_positiv

            # Aktualisieren oder Erstellen des `selected_data` DataFrames im Session State
            if 'selected_data' in st.session_state:
                st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
                st.session_state.selected_data.drop_duplicates(subset='ID', keep='last', inplace=True)
            else:
                st.session_state.selected_data = new_data
            
            longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
    return longlist


def display_selected_data():
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        # Füllen Sie fehlende Werte in 'Thema', 'Unterthema' und 'Unter-Unterthema' mit einem leeren String
        for column in ['Thema', 'Unterthema', 'Unter-Unterthema']:
            st.session_state.selected_data[column] = st.session_state.selected_data[column].fillna('')

        # Auswahl der benötigten Spalten
        selected_columns = st.session_state.selected_data[['ID', 'Auswirkung', 'Finanziell', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']]
        
        # Definieren der gridOptions
        gridOptions = {
            'defaultColDef': {
                'resizable': True,
                'width': 150,
                'minWidth': 50
            },
            'columnDefs': [
                {'headerName': 'ID', 'field': 'ID', 'width': 100, 'minWidth': 50},
                {'headerName': 'Auswirkung', 'field': 'Auswirkung', 'flex': 1},
                {'headerName': 'Finanziell', 'field': 'Finanziell', 'flex': 1},
                {'headerName': 'Finanz-Score', 'field': 'Score Finanzen', 'width': 150, 'minWidth': 50},
                {'headerName': 'Auswirkungs-Score', 'field': 'Score Auswirkung', 'width': 150, 'minWidth': 50},
                {'headerName': 'Thema', 'field': 'Thema', 'flex': 1},
                {'headerName': 'Unterthema', 'field': 'Unterthema', 'flex': 1},
                {'headerName': 'Unter-Unterthema', 'field': 'Unter-Unterthema', 'flex': 1}
            ]
        }
        # Erstellen des AgGrid
        AgGrid(selected_columns, gridOptions=gridOptions)

def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)
    gb.configure_pagination()
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    grid_options = gb.build()
    grid_response = AgGrid(longlist, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    st.session_state['selected_rows'] = grid_response['selected_rows']

# Erstellen Sie ein leeres Wörterbuch zur Speicherung von Inhalt-ID-Zuordnungen
content_id_map = {}

# Dies ist die nächste ID, die zugewiesen werden soll
next_id = 1

def merge_dataframes():
    global next_id  # Zugriff auf die globale Variable next_id
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

    # Hinzufügen der 'NumericalRating' Spalte aus 'selected_rows_st'
    combined_df = pd.merge(combined_df, selected_rows_st[['Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating']], on=['Thema', 'Unterthema', 'Unter-Unterthema'], how='left')

    # Entfernen von Duplikaten
    combined_df = combined_df.drop_duplicates(subset=['Thema', 'Unterthema', 'Unter-Unterthema'])

    # Hinzufügen einer 'ID'-Spalte
    combined_df.insert(0, 'ID', range(1, 1 + len(combined_df)))

     # Hinzufügen einer 'ID'-Spalte
    for index, row in combined_df.iterrows():
        content = (row['Thema'], row['Unterthema'], row['Unter-Unterthema'])

        # Überprüfen Sie, ob der Inhalt bereits eine ID hat
        if content in content_id_map:
            # Verwenden Sie die vorhandene ID
            id = content_id_map[content]
        else:
            # Erstellen Sie eine neue ID und speichern Sie die Zuordnung
            id = next_id
            content_id_map[content] = id
            next_id += 1  # Inkrementieren Sie die nächste ID

        # Setzen Sie die ID im DataFrame
        combined_df.at[index, 'ID'] = id
    
    # Erstellen eines session_state von combined_df
    st.session_state.combined_df = combined_df

    # Erstellen eines neuen DataFrame 'longlist', um Probleme mit der Zuordnung von 'selected_rows' zu vermeiden
    longlist = pd.DataFrame(combined_df)

    # Initialisieren der 'Bewertet'-Spalte in 'longlist'
    longlist = initialize_bewertet_column(longlist)

    # Initialize all required variables for ausgewaehlte_werte
    option = auswirkung_option = auswirkung_art_option = ausmass_neg_tat = umfang_neg_tat = behebbarkeit_neg_tat = ''
    ausmass_neg_pot = umfang_neg_pot = behebbarkeit_neg_pot = wahrscheinlichkeit_neg_pot = ''  
    ausmass_pos_tat = umfang_pos_tat = ausmass_pos_pot = umfang_pos_pot = behebbarkeit_pos_pot = ''
    wahrscheinlichkeit_finanziell = ausmass_finanziell = auswirkung_finanziell = ''

    st.sidebar.markdown("---")
    st.sidebar.subheader("Auswirkungsbewertung")
    auswirkung_option = st.sidebar.selectbox('Bitte wählen Sie die Eigenschaft der Auswirkung:', ['Keine Auswirkung','Positive Auswirkung', 'Negative Auswirkung'], index=2, key="auswirkung_option")
    if auswirkung_option == 'Negative Auswirkung':
        auswirkung_art_option = st.sidebar.selectbox('Bitte wählen Sie die Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option")
        if auswirkung_art_option == 'Tatsächliche Auswirkung':
            ausmass_neg_tat = st.sidebar.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_tat")
            umfang_neg_tat = st.sidebar.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_tat")
            behebbarkeit_neg_tat = st.sidebar.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_tat")
        elif auswirkung_art_option == 'Potenzielle Auswirkung':
            ausmass_neg_pot = st.sidebar.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_pot")
            umfang_neg_pot = st.sidebar.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_pot")
            behebbarkeit_neg_pot = st.sidebar.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_pot")
            wahrscheinlichkeit_neg_pot = st.sidebar.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_neg_pot")
    elif auswirkung_option == 'Positive Auswirkung':
        auswirkung_art_option = st.sidebar.selectbox('Bitte wählen Sie die Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option_pos")
        if auswirkung_art_option == 'Tatsächliche Auswirkung':
            ausmass_pos_tat = st.sidebar.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_tat")
            umfang_pos_tat = st.sidebar.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_tat")
        elif auswirkung_art_option == 'Potenzielle Auswirkung':
            ausmass_pos_pot = st.sidebar.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_pot")
            umfang_pos_pot = st.sidebar.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_pot")
            behebbarkeit_pos_pot = st.sidebar.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_pos_pot")
   
    st.sidebar.markdown("---")
    st.sidebar.subheader("Finanzielle Bewertung")
    ausmass_finanziell = st.sidebar.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_finanziell")
    wahrscheinlichkeit_finanziell = st.sidebar.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_finanziell")
    auswirkung_finanziell = st.sidebar.select_slider("Finanzielle Auswirkung:", options=["Keine", "Sehr gering", "Eher gering", "Eher hoch", "Hoch", "Sehr hoch"], key="auswirkung_finanziell")

    # Store selected values
    ausgewaehlte_werte = {
        "option": option,
        "auswirkung_option": auswirkung_option,
        "auswirkung_art_option": auswirkung_art_option,
        "ausmass_neg_tat": ausmass_neg_tat,
        "umfang_neg_tat": umfang_neg_tat,
        "behebbarkeit_neg_tat": behebbarkeit_neg_tat,
        "ausmass_neg_pot": ausmass_neg_pot,
        "umfang_neg_pot": umfang_neg_pot,
        "behebbarkeit_neg_pot": behebbarkeit_neg_pot,
        "wahrscheinlichkeit_neg_pot": wahrscheinlichkeit_neg_pot,
        "ausmass_pos_tat": ausmass_pos_tat,
        "umfang_pos_tat": umfang_pos_tat,
        "ausmass_pos_pot": ausmass_pos_pot,
        "umfang_pos_pot": umfang_pos_pot,
        "behebbarkeit_pos_pot": behebbarkeit_pos_pot,
        "wahrscheinlichkeit_finanziell": wahrscheinlichkeit_finanziell,
        "ausmass_finanziell": ausmass_finanziell,
        "auswirkung_finanziell": auswirkung_finanziell
    }

    # Proceed with the rest of the logic
    longlist = submit_bewertung(longlist, ausgewaehlte_werte)
    display_grid(longlist)
    
    with st.expander("Bewertungen anzeigen"):
        display_selected_data()

def Scatter_chart():
    # Überprüfen Sie, ob 'selected_data' und 'combined_df' initialisiert wurden
    if "selected_data" not in st.session_state or st.session_state.selected_data.empty or "combined_df" not in st.session_state or st.session_state.combined_df.empty:
        return

    # Stellen Sie sicher, dass 'selected_data' ein DataFrame mit den benötigten Spalten ist
    required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']
    if all(column in st.session_state.selected_data.columns for column in required_columns):
        selected_columns = st.session_state.selected_data[required_columns]

        # Innerer Join zwischen selected_columns und combined_df auf der Basis der 'ID'
        selected_columns = pd.merge(selected_columns, st.session_state.combined_df[['ID']], on='ID', how='inner')

        # Erstellen Sie eine neue Spalte 'color', die auf dem Wert der Spalte 'Thema' basiert
        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'green'
            elif theme in ['Eigene Belegschaft', 'Arbeitskräfte in der Wertschöpfungskette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'yellow'
            elif theme == 'Unternehmenspolitik':
                return 'blue'
            else:
                return 'gray'

        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        # Erstellen Sie ein Scatter-Chart mit Altair
        chart = alt.Chart(selected_columns).mark_circle(size=60).encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 100)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 100)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color', scale=None),  # Verwenden Sie die 'color' Spalte für die Farbe der Punkte
            tooltip=required_columns
        )

        # Zeigen Sie das Diagramm in Streamlit an
        st.altair_chart(chart)

def display_page():
    tab1, tab2, tab3 = st.tabs(["Bewertung der Nachhaltigkeitspunkte", "Stakeholder", "Gesamtübersicht"])
    with tab1: 
        merge_dataframes()
        Scatter_chart()
         
    with tab2:
        with st.expander("In Bewertung aufgenommene Stakeholderpunkte"):
            AgGrid(st.session_state.selected_rows_st)
    with tab3:
        st.write("Gesamtübersicht")