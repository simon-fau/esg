import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pages.Bottom_up_stakeholder import stakeholder_punkte
import altair as alt
import numpy as np

def stakeholder_Nachhaltigkeitspunkte():
    # Initialisiere DataFrame falls nicht vorhanden
    if 'stakeholder_punkte_df' not in st.session_state:
        st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "NumericalRating"])
    
    # Erstelle eine Kopie des DataFrame
    df3 = st.session_state.stakeholder_punkte_df.copy()
    df3['Quelle'] = 'Stakeholder'

    # Berechne die Größe der Klassen
    class_size = calculate_class_size(df3)

    # Erstelle die Layout-Spalten
    col1, col2 = st.columns([1.2, 3])
    with col1:
        # Füge den Schieberegler zur ersten Spalte hinzu
        add_slider()
    
    # Berechne die ausgewählten Zeilen basierend auf der Auswahl im Schieberegler
    selected_rows_st = calculate_selected_rows(df3, class_size)

    # Speichere die ausgewählten Zeilen im session_state
    st.session_state.selected_rows_st = selected_rows_st
    
    return selected_rows_st

def calculate_class_size(df):
    # Berechne die Größe der Klassen
    return (df['NumericalRating'].max() - df['NumericalRating'].min()) / 4

def add_slider():
    options = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']
    st.text("Grenzwert für die Auswahl der Stakeholderpunkte:")

    # Initialisiere 'slider_value' falls nicht vorhanden
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = options[0]

    # Speichere den aktuellen Zustand des Schiebereglers
    current_slider_value = st.select_slider('', options=options, value=st.session_state.slider_value)

    # Aktualisiere 'slider_value' im session_state bei Button-Klick
    if st.button('Auswahl übernehmen'):
        st.session_state.slider_value = current_slider_value
        st.experimental_rerun()

    st.markdown("""
        <style>
        .st-emotion-cache-183lzff,
        .st-emotion-cache-1inwz65 {
            font-family: "Source Sans Pro", sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)

def calculate_selected_rows(df, class_size):
    # Berechne die Anzahl der ausgewählten Zeilen basierend auf der Auswahl
    if st.session_state.slider_value == 'Wesentlich':
        return df[df['NumericalRating'] > 3 * class_size + df['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher Wesentlich':
        return df[df['NumericalRating'] > 2 * class_size + df['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher nicht wesentlich':
        return df[df['NumericalRating'] > class_size + df['NumericalRating'].min()]
    else:  # Nicht Wesentlich
        return df[df['NumericalRating'] > 0]


def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
    # Erstellen Sie eine Kopie von df2
    df4 = st.session_state.df2.copy()
    df4['Quelle'] = 'Eigene'
    return df4

def Top_down_Nachhaltigkeitspunkte():
    # Überprüfen, ob 'yes_no_selection' im session_state vorhanden ist
    if 'yes_no_selection' in st.session_state:
        yes_no_selection = st.session_state['yes_no_selection']
        
        # Erstellen eines DataFrames aus den ausgewählten Punkten
        data = []
        for key, value in yes_no_selection.items():
            if value and (key.startswith('Wesentlich') or key.startswith('Eher Wesentlich')):
                data.append(extract_data_from_key(key))
        
        selected_points_df = pd.DataFrame(data)
        selected_points_df['Quelle'] = 'Top Down'
        
        # Speichern des DataFrame 'selected_points_df' im session_state
        st.session_state['selected_points_df'] = selected_points_df
        return selected_points_df

def extract_data_from_key(key):
    # Initialisiere start und end basierend auf dem Key
    start, end, suffix = determine_key_suffix(key)
    
    if start is not None:
        unterthema = key[start:end].replace('_', ' ')
        thema, unterthema, unter_unterthema = map_key_to_theme_and_subthemes(key, unterthema)
        return {
            'Thema': thema,
            'Unterthema': unterthema,
            'Unter-Unterthema': unter_unterthema
        }

def determine_key_suffix(key):
    suffixes = ['E1', 'E2', 'E3', 'E4', 'E5', 'S1', 'S2', 'S3', 'S4', 'G1']
    for suffix in suffixes:
        if key.endswith(suffix):
            start = key.find('Wesentlich_') + len('Wesentlich_') if 'Wesentlich_' in key else key.find('Eher_Wesentlich_') + len('Eher_Wesentlich_')
            end = key.find(f'_{suffix}')
            return start, end, suffix
    return None, None, None

def map_key_to_theme_and_subthemes(key, unterthema_raw):
    thema_map = {
        'E1': 'Klimawandel',
        'E2': 'Umweltverschmutzung',
        'E3': 'Meeres- und Wasserressourcen',
        'E4': 'Biodiversität',
        'E5': 'Kreislaufwirtschaft',
        'S1': 'Eigene Belegschaft',
        'S2': 'Belegschaft Lieferkette',
        'S3': 'Betroffene Gemeinschaften',
        'S4': 'Verbraucher und Endnutzer',
        'G1': 'Unternehmenspolitik'
    }
    if key.endswith('E4'):
        return map_biodiversity_key(key, unterthema_raw)
    elif key.endswith('S1'):
        return map_workforce_key('Eigene Belegschaft', unterthema_raw)
    elif key.endswith('S2'):
        return map_workforce_key('Belegschaft Lieferkette', unterthema_raw)
    elif key.endswith('S3'):
        return map_community_key(unterthema_raw)
    elif key.endswith('S4'):
        return map_consumer_key(unterthema_raw)
    else:
        return thema_map[key[-2:]], unterthema_raw, ''

def map_biodiversity_key(key, unterthema_raw):
    unterthema_map = {
        'Direkte Ursachen des Biodiversitätsverlusts': ['Klimawandel', 'Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen', 'Direkte Ausbeutung', 'Invasive gebietsfremde Arten', 'Umweltverschmutzung', 'Sonstige'],
        'Auswirkungen auf den Zustand der Arten': ['Populationsgröße von Arten', 'Globales Ausrottungsrisiko von Arten'],
        'Auswirkungen auf den Umfang und den Zustand von Ökosystemen': ['Landdegradation', 'Wüstenbildung', 'Bodenversiegelung'],
        'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen': ['Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Biodiversität', unterthema, unterthema_raw

def map_workforce_key(thema, unterthema_raw):
    unterthema_map = {
        'Arbeitsbedingungen': ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Beruf und Privatleben', 'Gesundheitsschutz und Sicherheit'],
        'Gleichbehandlung und Chancengleichheit für alle': ['Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen', 'Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz', 'Vielfalt'],
        'Sonstige arbeitsbezogene Rechte': ['Kinderarbeit', 'Zwangarbeit', 'Angemessene Unterbringungen', 'Datenschutz']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return thema, unterthema, unterthema_raw

def map_community_key(unterthema_raw):
    unterthema_map = {
        'Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften': ['Angemessene Unterbringungen', 'Angemessene Ernährung', 'Wasser- und Sanitäreinrichtungen', 'Bodenbezogene Auswirkungen', 'Sicherheitsbezogene Auswirkungen'],
        'Bürgerrechte und politische Rechte von Gemeinschaften': ['Meinungsfreiheit', 'Versammlungsfreiheit', 'Auswirkungen auf Menschenrechtsverteidiger'],
        'Rechte von indigenen Völkern': ['Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung', 'Selbstbestimmung', 'Kulturelle Rechte']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Betroffene Gemeinschaften', unterthema, unterthema_raw

def map_consumer_key(unterthema_raw):
    unterthema_map = {
        'Informationsbezogene Auswirkungen für Verbraucher und Endnutzer': ['Datenschutz', 'Meinungsfreiheit', 'Zugang zu (hochwertigen) Informationen'],
        'Persönliche Sicherheit von Verbrauchern und Endnutzern': ['Gesundheitsschutz und Sicherheit', 'Persönliche Sicherheit', 'Kinderschutz'],
        'Soziale Inklusion von Verbrauchern und Endnutzern': ['Nichtdiskriminierung', 'Selbstbestimmung', 'Zugang zu Produkten und Dienstleistungen', 'Verantwortliche Vermarktungspraktiken']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Verbraucher und Endnutzer', unterthema, unterthema_raw


def initialize_bewertet_column(longlist):
    # Initialisiert die 'Bewertet'-Spalte im 'longlist'-DataFrame
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
                ausgewaehlte_werte.get('ausmass_neg_tat', '') if ausgewaehlte_werte.get('ausmass_neg_tat') else '',
                ausgewaehlte_werte.get('umfang_neg_tat', '') if ausgewaehlte_werte.get('umfang_neg_tat') else '',
                ausgewaehlte_werte.get('behebbarkeit_neg_tat', '') if ausgewaehlte_werte.get('behebbarkeit_neg_tat') else '',
                ausgewaehlte_werte.get('ausmass_neg_pot', '') if ausgewaehlte_werte.get('ausmass_neg_pot') else '',
                ausgewaehlte_werte.get('umfang_neg_pot', '') if ausgewaehlte_werte.get('umfang_neg_pot') else '',
                ausgewaehlte_werte.get('behebbarkeit_neg_pot', '') if ausgewaehlte_werte.get('behebbarkeit_neg_pot') else '',
                ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', '') if ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot') else '',
                ausgewaehlte_werte.get('ausmass_pos_tat', '') if ausgewaehlte_werte.get('ausmass_pos_tat') else '',
                ausgewaehlte_werte.get('umfang_pos_tat', '') if ausgewaehlte_werte.get('umfang_pos_tat') else '',
                ausgewaehlte_werte.get('ausmass_pos_pot', '') if ausgewaehlte_werte.get('ausmass_pos_pot') else '',
                ausgewaehlte_werte.get('umfang_pos_pot', '') if ausgewaehlte_werte.get('umfang_pos_pot') else '',
                ausgewaehlte_werte.get('behebbarkeit_pos_pot', '') if ausgewaehlte_werte.get('behebbarkeit_pos_pot') else ''
            ] if part)

            new_data['Auswirkung'] = auswirkung_string
            finanziell_string = f"{ausgewaehlte_werte.get('ausmass_finanziell', '')} ; {ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', '')} ; {ausgewaehlte_werte.get('auswirkung_finanziell', '')}"
            new_data['Finanziell'] = finanziell_string
            
            # Berechnung des Scores für finanzielle Bewertungen normalized_score = ((produkt - min_produkt) / (max_produkt - min_produkt)) * 99 + 1
            new_data['Score Finanzen'] = np.round((
                                        ausmass_finanziell_mapping.get(ausgewaehlte_werte.get('ausmass_finanziell', 'Keine'), 1) *
                                        wahrscheinlichkeit_finanziell_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', 'Keine'), 1) *
                                        auswirkung_finanziell_mapping.get(ausgewaehlte_werte.get('auswirkung_finanziell', 'Keine'), 1) - 1) / (216 - 1) * 99 + 1
                                        , 1)
            
            # Berechnung Tatsächliche negative Auswirkungen
            tatsaechlich_negativ = np.round(((
                ausmass_neg_tat_mapping.get(ausgewaehlte_werte.get('ausmass_neg_tat', 'Keine'), 1) *
                umfang_neg_tat_mapping.get(ausgewaehlte_werte.get('umfang_neg_tat', 'Keine'), 1) *
                behebbarkeit_neg_tat_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_tat', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Potenzielle negative Auswirkungen
            potentiell_negativ = np.round(((
                ausmass_neg_pot_mapping.get(ausgewaehlte_werte.get('ausmass_neg_pot', 'Keine'), 1) *
                umfang_neg_pot_mapping.get(ausgewaehlte_werte.get('umfang_neg_pot', 'Keine'), 1) *
                behebbarkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_pot', 'Kein Aufwand'), 1) *
                wahrscheinlichkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', 'Tritt nicht ein'), 1) - 1) / (1296 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Tatsächliche positive Auswirkungen
            tatsaechlich_positiv = np.round(((
                ausmass_pos_tat_mapping.get(ausgewaehlte_werte.get('ausmass_pos_tat', 'Keine'), 1) *
                umfang_pos_tat_mapping.get(ausgewaehlte_werte.get('umfang_pos_tat', 'Keine'), 1) - 1) / (36 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Potenzielle positive Auswirkungen
            potentiell_positiv = np.round(((
                ausmass_pos_pot_mapping.get(ausgewaehlte_werte.get('ausmass_pos_pot', 'Keine'), 1) *
                umfang_pos_pot_mapping.get(ausgewaehlte_werte.get('umfang_pos_pot', 'Keine'), 1) *
                behebbarkeit_pos_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_pos_pot', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
                ), 1)
            
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

def delete_bewertung(longlist):
    if st.sidebar.button("Bewertung löschen"):
        if 'selected_rows' in st.session_state and 'selected_data' in st.session_state:
            selected_row_ids = [row['ID'] for row in st.session_state['selected_rows']]
            st.session_state.selected_data = st.session_state.selected_data[~st.session_state.selected_data['ID'].isin(selected_row_ids)]
            longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung löschen.")
    return longlist


def display_selected_data():
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        # Füllen Sie fehlende Werte in 'Thema', 'Unterthema' und 'Unter-Unterthema' mit einem leeren String
        for column in ['Thema', 'Unterthema', 'Unter-Unterthema']:
            st.session_state.selected_data[column] = st.session_state.selected_data[column].fillna('')

        # Auswahl der benötigten Spalten
        selected_columns = st.session_state.selected_data[['ID', 'Auswirkung', 'Finanziell', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']]

        # Extrahieren Sie die Spalte 'NumericalRating' aus 'combined_df' und fügen Sie sie zu 'selected_columns' hinzu
        if 'combined_df' in st.session_state and 'NumericalRating' in st.session_state.combined_df.columns:
            combined_df_with_numerical_rating = st.session_state.combined_df[['ID', 'NumericalRating']]
            selected_columns = pd.merge(selected_columns, combined_df_with_numerical_rating, on='ID', how='left')
        
        # Speichern Sie 'selected_columns' in 'st.session_state'
        st.session_state['selected_columns'] = selected_columns

def bewertung():
    if 'selected_columns' in st.session_state and not st.session_state.selected_columns.empty:
        selected_columns = st.session_state['selected_columns']

        # Create a selectbox for IDs
        selected_id = st.selectbox('ID auswählen', selected_columns['ID'].unique())

        # Filter the row with the selected ID
        selected_row = selected_columns[selected_columns['ID'] == selected_id]

        if not selected_row.empty:

            # Split the 'Auswirkung' string into parts by ';'
            auswirkung_parts = selected_row['Auswirkung'].values[0].split(';')

            # Split the 'Finanziell' string into parts by ';'
            finanziell_parts = selected_row['Finanziell'].values[0].split(';')

            # Display each part of 'Auswirkung'
            auswirkung_mapping = {
                1: 'Eigenschaft',
                2: 'Art',
                3: 'Ausmaß',
                4: 'Umfang',
                5: 'Behebarkeit',
                6: 'Wahrscheinlichkeit'
            }

            # Display each part of 'Finanziell'
            finanziell_mapping = {
                1: 'Ausmaß',
                2: 'Wahrscheinlichkeit',
                3: 'Finanzielle Auswirkung'
            }

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write("**Auswirkung**")
            
                for i, part in enumerate(auswirkung_parts, start=1):
                    if i in auswirkung_mapping:
                        st.write(f'{auswirkung_mapping[i]}:', part.strip())
                    else:
                        st.write(f'Auswirkung Teil {i}:', part.strip())

                st.write('Score:', selected_row['Score Auswirkung'].values[0])

            with col2:
                st.write("**Finanziell**")

                for i, part in enumerate(finanziell_parts, start=1):
                    if i in finanziell_mapping:
                        st.write(f'{finanziell_mapping[i]}:', part.strip())
                    else:
                        st.write(f'Finanziell Teil {i}:', part.strip())

                st.write('Score:', selected_row['Score Finanzen'].values[0])
            
            with col3:

                return
           
def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)
    gb.configure_side_bar()
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    gb.configure_column('ID', minWidth=50, maxWidth=100, width=70) 
    gb.configure_column('Bewertet', minWidth=100, maxWidth=100, width=80)
    gb.configure_column('Thema', minWidth=150, maxWidth=250, width=200)
    gb.configure_column('Quelle', minWidth=50, maxWidth=150, width=140)
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
    selected_points_df = Top_down_Nachhaltigkeitspunkte()
    selected_rows_st = stakeholder_Nachhaltigkeitspunkte()

    # Kombinieren der Daten in einem DataFrame
    combined_df = pd.concat([selected_points_df, df4, selected_rows_st], ignore_index=True)

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

    #Erstellung einer Kopie von combined_df ohne NumericalRating zur Darstellung der Longlist mit lediglich relevanten Spalten
    combined_df_without_numerical_rating = st.session_state.combined_df.drop(columns='NumericalRating')
    # Speichern Sie die neue DataFrame in 'st.session_state'
    st.session_state['combined_df_without_numerical_rating'] = combined_df_without_numerical_rating

    # Erstellen eines neuen DataFrame 'longlist', um Probleme mit der Zuordnung von 'selected_rows' zu vermeiden
    longlist = pd.DataFrame(combined_df_without_numerical_rating)

    # Initialisieren der 'Bewertet'-Spalte in 'longlist'
    longlist = initialize_bewertet_column(longlist)

    # Initialize all required variables for ausgewaehlte_werte
    option = auswirkung_option = auswirkung_art_option = ausmass_neg_tat = umfang_neg_tat = behebbarkeit_neg_tat = ''
    ausmass_neg_pot = umfang_neg_pot = behebbarkeit_neg_pot = wahrscheinlichkeit_neg_pot = ''  
    ausmass_pos_tat = umfang_pos_tat = ausmass_pos_pot = umfang_pos_pot = behebbarkeit_pos_pot = ''
    wahrscheinlichkeit_finanziell = ausmass_finanziell = auswirkung_finanziell = ''

    st.sidebar.markdown('---')
    with st.sidebar:
        with st.expander("Auwirkungsbewertung"):
            auswirkung_option = st.selectbox('Eigenschaft der Auswirkung:', ['Negative Auswirkung','Positive Auswirkung', 'Keine Auswirkung'], index=2, key="auswirkung_option")
            if auswirkung_option == 'Negative Auswirkung':
                auswirkung_art_option = st.selectbox('Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option")      
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    ausmass_neg_tat = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_tat")
                    umfang_neg_tat = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_tat")
                    behebbarkeit_neg_tat = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    ausmass_neg_pot = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_pot")
                    umfang_neg_pot = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_pot")
                    behebbarkeit_neg_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_pot")
                    wahrscheinlichkeit_neg_pot = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_neg_pot")
            elif auswirkung_option == 'Positive Auswirkung':
                auswirkung_art_option = st.selectbox('Bitte wählen Sie die Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option_pos")
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    ausmass_pos_tat = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_tat")
                    umfang_pos_tat = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    ausmass_pos_pot = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_pot")
                    umfang_pos_pot = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_pot")
                    behebbarkeit_pos_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_pos_pot")
    
        with st.expander("Finanzielle Bewertung"):
            ausmass_finanziell = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_finanziell")
            wahrscheinlichkeit_finanziell = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_finanziell")
            auswirkung_finanziell = st.select_slider("Finanzielle Auswirkung:", options=["Keine", "Sehr gering", "Eher gering", "Eher hoch", "Hoch", "Sehr hoch"], key="auswirkung_finanziell")
   
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
    longlist = delete_bewertung(longlist)
    display_grid(longlist)
    

def Scatter_chart():
    # Überprüfen Sie, ob 'selected_data' und 'combined_df' initialisiert wurden
    if "selected_data" not in st.session_state or st.session_state.selected_data.empty or "combined_df" not in st.session_state or st.session_state.combined_df.empty:
        return

    # Stellen Sie sicher, dass 'selected_data' ein DataFrame mit den benötigten Spalten ist
    required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']
    if all(column in st.session_state.selected_data.columns for column in required_columns):
        selected_columns = st.session_state.selected_data[required_columns]

        # Innerer Join zwischen selected_columns und combined_df auf der Basis der 'ID'
        selected_columns = pd.merge(selected_columns, st.session_state.combined_df[['ID', 'NumericalRating']], on='ID', how='inner')

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

        # Normalisieren Sie die 'NumericalRating' Werte auf den Bereich [100, 600] und speichern Sie sie in der neuen Spalte 'size'
        min_rating = st.session_state.combined_df['NumericalRating'].min()
        max_rating = st.session_state.combined_df['NumericalRating'].max()
        selected_columns['size'] = ((selected_columns['NumericalRating'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        
        # Füllen Sie fehlende Werte in der 'size' Spalte mit 100
        selected_columns['size'] = selected_columns['size'].fillna(100)
        
        # Erstellen Sie ein Scatter-Chart mit Altair
        chart = alt.Chart(selected_columns, width=800, height=600).mark_circle().encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 100)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 100)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['green', 'yellow', 'blue', 'gray'],
                range=['green', 'yellow', 'blue', 'gray']
            ), legend=alt.Legend(
                title="Thema",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Environmental', 'Social', 'Governance', 'Sonstige']
            )),
            size=alt.Size('size', scale=alt.Scale(range=[100, 1000]), legend=None),  # Keine Legende für die Größe der Punkte
            tooltip=required_columns
        )
        
        # Zeigen Sie das Diagramm in Streamlit an
        st.altair_chart(chart)

def display_page():
    tab1, tab2, tab3, tab4 = st.tabs(["Bewertung der Nachhaltigkeitspunkte", "Graphische Übersicht", "Stakeholder", "Gesamtübersicht"])
    with tab1:    
            merge_dataframes()
            display_selected_data()   
            
            with st.expander("Bewertungen"):
                bewertung()
    with tab2:
        st.write("Graphische Übersicht")
        Scatter_chart()
         
    with tab3:
        with st.expander("In Bewertung aufgenommene Stakeholderpunkte"):
            AgGrid(st.session_state.selected_rows_st)
    with tab4:
        st.write("Gesamtübersicht")