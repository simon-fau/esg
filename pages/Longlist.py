import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import altair as alt
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Funktion zum Speichern des Zustands
def save_state():
    with open('a.pkl', 'wb') as f:
        pickle.dump(dict(st.session_state), f)

def stakeholder_Nachhaltigkeitspunkte():
    # Initialisiere DataFrame falls nicht vorhanden
    if 'stakeholder_punkte_filtered' not in st.session_state:
        st.session_state.stakeholder_punkte_filtered = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "Stakeholder Gesamtbew.", "Quelle"])	
    
    # Erstelle eine Kopie des DataFrame
    selected_rows_st = st.session_state.stakeholder_punkte_filtered.copy()

    # Speichere die ausgewählten Zeilen im session_state
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
    # Überprüfen, ob 'yes_no_selection' im session_state vorhanden ist
    if 'yes_no_selection' in st.session_state:
        yes_no_selection = st.session_state['yes_no_selection']
        
        # Erstellen eines DataFrames aus den ausgewählten Punkten
        data = []
        for key, value in yes_no_selection.items():
            if value and (key.startswith('Wesentlich') or key.startswith('Eher Wesentlich')):
                data.append(extract_data_from_key(key))
        
        selected_points_df = pd.DataFrame(data)
        selected_points_df['Quelle'] = 'Top-Down Bewertung'
        
        # Speichern des DataFrame 'selected_points_df' im session_state
        st.session_state['selected_points_df'] = selected_points_df
        return selected_points_df

def extract_data_from_key(key):
    start, end, suffix = determine_key_suffix(key)
    
    if start is not None:
        unterthema = key[start:end].replace('_', ' ')
        thema, unterthema, unter_unterthema = map_key_to_theme_and_subthemes(key, unterthema)
        return {
            'Thema': thema,
            'Unterthema': unterthema,
            'Unter-Unterthema': unter_unterthema
        }
    else:
        return {
            'Thema': 'Unbekannt',
            'Unterthema': 'Unbekannt',
            'Unter-Unterthema': 'Unbekannt'
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
        return map_biodiversity_key(unterthema_raw)
    elif key.endswith('S1'):
        return map_own_workforce_key(unterthema_raw)
    elif key.endswith('S2'):
        return map_valuechain_workforce_key(unterthema_raw)
    elif key.endswith('S3'):
        return map_community_key(unterthema_raw)
    elif key.endswith('S4'):
        return map_consumer_key(unterthema_raw)
    else:
        return thema_map.get(key[-2:], 'Unbekannt'), unterthema_raw, ''

def map_biodiversity_key(unterthema_raw):
    unterthema_map = {
        'Direkte Ursachen des Biodiversitätsverlusts': ['Klimawandel', 'Land- Süßwasser- und Meeresnutzungsänderungen', 'Direkte Ausbeutung', 'Invasive gebietsfremde Arten', 'Umweltverschmutzung', 'Sonstige'],
        'Auswirkungen auf den Zustand der Arten': ['Populationsgröße von Arten', 'Globales Ausrottungsrisiko von Arten'],
        'Auswirkungen auf den Umfang und den Zustand von Ökosystemen': ['Landdegradation', 'Wüstenbildung', 'Bodenversiegelung'],
        'Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen': ['Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Biodiversität', unterthema, unterthema_raw
    return 'Biodiversität', 'Unbekannt', 'Unbekannt'

def map_own_workforce_key(unterthema_raw):
    unterthema_map = {
        'Arbeitsbedingungen': ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Beruf und Privatleben', 'Gesundheitsschutz und Sicherheit'],
        'Gleichbehandlung und Chancengleichheit für alle': ['Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen', 'Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz', 'Vielfalt'],
        'Sonstige arbeitsbezogene Rechte': ['Kinderarbeit', 'Zwangarbeit', 'Wasser- und Sanitäreinrichtungen', 'Angemessene Unterbringungen', 'Datenschutz']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Eigene Belegschaft', unterthema, unterthema_raw
    return 'Eigene Belegschaft', 'Unbekannt', 'Unbekannt'

def map_valuechain_workforce_key(unterthema_raw):
    unterthema_map = {
        'Arbeitsbedingungen': ['Sichere Beschäftigung', 'Arbeitszeit', 'Angemessene Entlohnung', 'Sozialer Dialog', 'Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'Vereinbarkeit von Beruf und Privatleben', 'Gesundheitsschutz und Sicherheit'],
        'Gleichbehandlung und Chancengleichheit für alle': ['Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'Schulungen und Kompetenzentwicklung', 'Beschäftigung und Inklusion von Menschen mit Behinderungen', 'Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz', 'Vielfalt'],
        'Sonstige arbeitsbezogene Rechte': ['Kinderarbeit', 'Zwangarbeit', 'Wasser- und Sanitäreinrichtungen', 'Angemessene Unterbringungen', 'Datenschutz']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Belegschaft Lieferkette', unterthema, unterthema_raw
    return 'Belegschaft Lieferkette', 'Unbekannt', 'Unbekannt'

def map_community_key(unterthema_raw):
    unterthema_map = {
        'Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften': ['Angemessene Unterbringungen', 'Angemessene Ernährung', 'Wasser- und Sanitäreinrichtungen', 'Bodenbezogene Auswirkungen', 'Sicherheitsbezogene Auswirkungen'],
        'Bürgerrechte und politische Rechte von Gemeinschaften': ['Meinungsfreiheit', 'Versammlungsfreiheit', 'Auswirkungen auf Menschenrechtsverteidiger'],
        'Rechte von indigenen Völkern': ['Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung', 'Selbstbestimmung', 'Kulturelle Rechte']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Betroffene Gemeinschaften', unterthema, unterthema_raw
    return 'Betroffene Gemeinschaften', 'Unbekannt', 'Unbekannt'

def map_consumer_key(unterthema_raw):
    unterthema_map = {
        'Informationsbezogene Auswirkungen für Verbraucher und Endnutzer': ['Datenschutz', 'Meinungsfreiheit', 'Zugang zu (hochwertigen) Informationen'],
        'Persönliche Sicherheit von Verbrauchern und Endnutzern': ['Gesundheitsschutz und Sicherheit', 'Persönliche Sicherheit', 'Kinderschutz'],
        'Soziale Inklusion von Verbrauchern und Endnutzern': ['Nichtdiskriminierung', 'Selbstbestimmung', 'Zugang zu Produkten und Dienstleistungen', 'Verantwortliche Vermarktungspraktiken']
    }
    for unterthema, values in unterthema_map.items():
        if unterthema_raw in values:
            return 'Verbraucher und Endnutzer', unterthema, unterthema_raw
    return 'Verbraucher und Endnutzer', 'Unbekannt', 'Unbekannt'

def extract_data_from_key(key):
    start, end, suffix = determine_key_suffix(key)
    
    if start is not None:
        unterthema = key[start:end].replace('_', ' ')
        thema, unterthema, unter_unterthema = map_key_to_theme_and_subthemes(key, unterthema)
        return {
            'Thema': thema,
            'Unterthema': unterthema,
            'Unter-Unterthema': unter_unterthema
        }
    else:
        return {
            'Thema': 'Unbekannt',
            'Unterthema': 'Unbekannt',
            'Unter-Unterthema': 'Unbekannt'
        }

def initialize_bewertet_column(longlist):
    # Initialisiert die 'Bewertet'-Spalte im 'longlist'-DataFrame
    if 'selected_data' in st.session_state:
        longlist['Bewertet'] = longlist['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        longlist['Bewertet'] = 'Nein'
    return longlist

def submit_bewertung(longlist, ausgewaehlte_werte):
    if st.sidebar.button("📤 Bewertung absenden"):
        # Überprüfen, ob ausgewaehlte_werte mindestens einen gültigen Wert enthält
        if not any(ausgewaehlte_werte.values()):
            st.error("Bitte wählen Sie eine Checkbox in der Liste aus.")
            return longlist

        # Überprüfen, ob ausgewählte Zeilen im Session State vorhanden sind
        if 'selected_rows' not in st.session_state or not st.session_state['selected_rows']:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
            return longlist

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
        finanziell_string = f"{ausgewaehlte_werte.get('art_finanziell', '')} ; {ausgewaehlte_werte.get('ausmass_finanziell', '')} ; {ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', '')} ; {ausgewaehlte_werte.get('auswirkung_finanziell', '')}"
        new_data['Finanziell'] = finanziell_string

        # Berechnung des Scores für finanzielle Bewertungen
        new_data['Score Finanzen'] = np.round((
            ausmass_finanziell_mapping.get(ausgewaehlte_werte.get('ausmass_finanziell', 'Keine'), 1) *
            wahrscheinlichkeit_finanziell_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', 'Keine'), 1) *
            auswirkung_finanziell_mapping.get(ausgewaehlte_werte.get('auswirkung_finanziell', 'Keine'), 1) - 1) / (215) * 999 + 1
            , 1)

        # Berechnung Tatsächliche negative Auswirkungen
        tatsaechlich_negativ = np.round(((
            ausmass_neg_tat_mapping.get(ausgewaehlte_werte.get('ausmass_neg_tat', 'Keine'), 1) *
            umfang_neg_tat_mapping.get(ausgewaehlte_werte.get('umfang_neg_tat', 'Keine'), 1) *
            behebbarkeit_neg_tat_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_tat', 'Kein Aufwand'), 1) - 1) / (215) * 999 + 1
            ), 1)

        # Berechnung Potenzielle negative Auswirkungen
        potentiell_negativ = np.round(((
            ausmass_neg_pot_mapping.get(ausgewaehlte_werte.get('ausmass_neg_pot', 'Keine'), 1) *
            umfang_neg_pot_mapping.get(ausgewaehlte_werte.get('umfang_neg_pot', 'Keine'), 1) *
            behebbarkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_pot', 'Kein Aufwand'), 1) *
            wahrscheinlichkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', 'Tritt nicht ein'), 1) - 1) / (1295) * 999 + 1
            ), 1)

        # Berechnung Tatsächliche positive Auswirkungen
        tatsaechlich_positiv = np.round(((
            ausmass_pos_tat_mapping.get(ausgewaehlte_werte.get('ausmass_pos_tat', 'Keine'), 1) *
            umfang_pos_tat_mapping.get(ausgewaehlte_werte.get('umfang_pos_tat', 'Keine'), 1) - 1) / (35) * 999 + 1
            ), 1)

        # Berechnung Potenzielle positive Auswirkungen
        potentiell_positiv = np.round(((
            ausmass_pos_pot_mapping.get(ausgewaehlte_werte.get('ausmass_pos_pot', 'Keine'), 1) *
            umfang_pos_pot_mapping.get(ausgewaehlte_werte.get('umfang_pos_pot', 'Keine'), 1) *
            behebbarkeit_pos_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_pos_pot', 'Kein Aufwand'), 1) - 1) / (215) * 999 + 1
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
        st.success("Bewertung abgesendet")
   
    return longlist

def delete_bewertung(longlist):
    st.sidebar.markdown("---")
    st.sidebar.write("**Bewertungen löschen**")
    
    if 'selected_data' in st.session_state:
        selected_data_ids = st.session_state.selected_data['ID'] if 'ID' in st.session_state.selected_data.columns else []

        # Button zum Löschen einer spezifischen Bewertung
        if st.sidebar.button("🗑️ Bewertung löschen"):
            if 'selected_rows' in st.session_state and st.session_state['selected_rows']:
                selected_row_ids = [row['ID'] for row in st.session_state['selected_rows']]
                rows_to_delete = st.session_state.selected_data[st.session_state.selected_data['ID'].isin(selected_row_ids)]
                
                if rows_to_delete.empty or all(longlist[longlist['ID'].isin(selected_row_ids)]['Bewertet'] == 'Nein'):
                    st.error("Keine Bewertung zum Löschen vorhanden.")
                else:
                    st.session_state.selected_data = st.session_state.selected_data[~st.session_state.selected_data['ID'].isin(selected_row_ids)]
                    longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
                    
                    if st.session_state.selected_data.empty:
                        st.session_state['selected_columns'] = pd.DataFrame()

                    st.success("Bewertung erfolgreich gelöscht.")
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

        # Extrahieren Sie die Spalte 'Stakeholder Gesamtbew.' aus 'combined_df' und fügen Sie sie zu 'selected_columns' hinzu
        if 'combined_df' in st.session_state and 'Stakeholder Gesamtbew.' in st.session_state.combined_df.columns:
            combined_df_with_numerical_rating = st.session_state.combined_df[['ID', 'Stakeholder Gesamtbew.']]
            selected_columns = pd.merge(selected_columns, combined_df_with_numerical_rating, on='ID', how='left')
        
        # Speichern Sie 'selected_columns' in 'st.session_state'
        st.session_state['selected_columns'] = selected_columns

# Zeigt Bertungen nur an, wenn diese auch in der Longlist vorhanden sind
def Bewertungsanzeige():
    if 'selected_columns' not in st.session_state or st.session_state['selected_columns'].empty:
        st.info('Keine Bewertung vorhanden. Bitte fügen Sie eine Bewertung hinzu.')
        return  # Beendet die Funktion, wenn keine Bewertung vorhanden ist

    if 'longlist' not in st.session_state:
        st.info('Keine Longlist vorhanden. Bitte fügen Sie eine Longlist hinzu.')
        return  # Beendet die Funktion, wenn keine Longlist vorhanden ist

    longlist_ids = st.session_state['longlist']['ID'].unique()
    selected_columns = st.session_state['selected_columns']
    selected_columns = selected_columns[selected_columns['ID'].isin(longlist_ids)]
    st.session_state['selected_columns'] = selected_columns

    # Create a selectbox for IDs
    selected_id = st.selectbox('ID auswählen', selected_columns['ID'].unique())

    # Filter the row with the selected ID
    selected_row = selected_columns[selected_columns['ID'] == selected_id]

    if not selected_row.empty:
        # Speichern der ausgewählten Bewertung im Session State
        st.session_state['selected_evaluation'] = selected_row

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
            1: 'Art',
            2: 'Ausmaß',
            3: 'Wahrscheinlichkeit',
            4: 'Finanzielle Auswirkung'
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
            # Hier können weitere Informationen oder Aktionen hinzugefügt werden
            pass

        # Hinzufügen der Bewertung zum session state 'all_evaluations'
        if 'all_evaluations' not in st.session_state:
            st.session_state['all_evaluations'] = []

        evaluation = {
            'ID': selected_row['ID'].values[0],
            'Auswirkung': selected_row['Auswirkung'].values[0],
            'Score Auswirkung': selected_row['Score Auswirkung'].values[0],
            'Finanziell': selected_row['Finanziell'].values[0],
            'Score Finanzen': selected_row['Score Finanzen'].values[0]
        }

        st.session_state['all_evaluations'].append(evaluation)

        # Erstellen und Anzeigen eines DataFrame mit allen Bewertungen
        evaluations_df = pd.DataFrame(st.session_state['all_evaluations'])
        #st.write("**Alle Bewertungen**")
        #st.dataframe(evaluations_df)

    # Zustand speichern nach jeder Änderung
    save_state()

def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)
    gb.configure_side_bar()
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    gb.configure_column('ID', width=70) 
    gb.configure_column('Bewertet',  width=80)
    gb.configure_column('Thema',  width=200)
    grid_options = gb.build()
    grid_response = AgGrid(longlist, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    st.session_state['selected_rows'] = grid_response['selected_rows']

# Erstellen Sie ein leeres Wörterbuch zur Speicherung von Inhalt-ID-Zuordnungen
content_id_map = {}

# Dies ist die nächste ID, die zugewiesen werden soll
next_id = 1

# Define the nested function
def count_bewertete_punkte():
    if 'longlist' in st.session_state:
        # Erstellen einer Kopie des DataFrames
        longlist_copy = st.session_state.longlist.copy()
        # Zählen der Zeilen, die in der Spalte 'Bewertung' den Wert 'Ja' haben
        yes_count = longlist_copy[longlist_copy['Bewertet'] == 'Ja'].shape[0]
        # Gesamtanzahl der Zeilen
        total_count = longlist_copy.shape[0]
        # Berechnung des Prozentsatzes
        if total_count > 0:
            percentage = (yes_count / total_count) * 100
        else:
            percentage = 0
        # Ausgabe des Prozentsatzes als st.metric
        st.write(f"Sie haben {yes_count} von {total_count} Punkten bewertet.")

def merge_dataframes():
    global next_id
    if 'content_id_map' not in st.session_state:
        st.session_state.content_id_map = {}
    content_id_map = st.session_state.content_id_map

    # Abrufen der Daten von verschiedenen Quellen
    selected_points_df = Top_down_Nachhaltigkeitspunkte()
    selected_rows_st = stakeholder_Nachhaltigkeitspunkte()
    df4 = eigene_Nachhaltigkeitspunkte()

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

    # Hinzufügen der 'Stakeholder Gesamtbew.' Spalte aus 'selected_rows_st'
    combined_df = pd.merge(combined_df, selected_rows_st[['Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Gesamtbew.']], on=['Thema', 'Unterthema', 'Unter-Unterthema'], how='left')

    # Entfernen von Duplikaten
    combined_df = combined_df.drop_duplicates(subset=['Thema', 'Unterthema', 'Unter-Unterthema'])

    # Hinzufügen einer 'ID'-Spalte
    combined_df.insert(0, 'ID', None)

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
    

    # Erstellung einer Kopie von combined_df ohne Stakeholder Gesamtbew. und Quelle zur Darstellung der Longlist mit lediglich relevanten Spalten
    combined_df_without_numerical_rating_and_source = st.session_state.combined_df.drop(columns=['Stakeholder Gesamtbew.', 'Quelle'])
    # Speichern Sie die neue DataFrame in 'st.session_state'
    st.session_state['combined_df_without_numerical_rating_and_source'] = combined_df_without_numerical_rating_and_source
    

    # Erstellen eines neuen DataFrame 'longlist', um Probleme mit der Zuordnung von 'selected_rows' zu vermeiden
    longlist = pd.DataFrame(combined_df_without_numerical_rating_and_source)

    # Initialisieren der 'Bewertet'-Spalte in 'longlist'
    longlist = initialize_bewertet_column(longlist)

    st.session_state['longlist'] = longlist
    save_state()

    # Initialize all required variables for ausgewaehlte_werte
    option = auswirkung_option = auswirkung_art_option = ausmass_neg_tat = umfang_neg_tat = behebbarkeit_neg_tat = ''
    ausmass_neg_pot = umfang_neg_pot = behebbarkeit_neg_pot = wahrscheinlichkeit_neg_pot = ''  
    ausmass_pos_tat = umfang_pos_tat = ausmass_pos_pot = umfang_pos_pot = behebbarkeit_pos_pot = ''
    art_finanziell = wahrscheinlichkeit_finanziell = ausmass_finanziell = auswirkung_finanziell = ''

    st.sidebar.markdown('---')
    st.sidebar.write("**Bewertungen hinzufügen**")
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
            art_finanziell = st.selectbox("Eigenschaft der Auswirkung:", ['Chance', 'Risiko', 'Keine Auswirkung'], index=2, key="art_finanziell")
            if art_finanziell != 'Keine Auswirkung':
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
        "art_finanziell": art_finanziell,
        "wahrscheinlichkeit_finanziell": wahrscheinlichkeit_finanziell,
        "ausmass_finanziell": ausmass_finanziell,
        "auswirkung_finanziell": auswirkung_finanziell
    }

    # Define the nested function
    def count_bewertete_punkte():
        if 'longlist' in st.session_state:
            # Zählen der Zeilen, die in der Spalte 'Bewertung' den Wert 'Ja' haben
            yes_count = st.session_state.longlist[st.session_state.longlist['Bewertet'] == 'Ja'].shape[0]
            # Gesamtanzahl der Zeilen
            total_count = st.session_state.longlist.shape[0]
            # Berechnung des Prozentsatzes
            if total_count > 0:
                percentage = (yes_count / total_count) * 100
            else:
                percentage = 0
            
            # Überprüfen, ob yes_count gleich total_count ist
            if yes_count == total_count:
                st.write("Abgeschlossen ✔")
                st.session_state['checkbox_state_6'] = True
            else:
                st.write(f"Sie haben {yes_count} von {total_count} Punkten bewertet.")
                st.session_state['checkbox_state_6'] = False

    # Proceed with the rest of the logic
    longlist = submit_bewertung(longlist, ausgewaehlte_werte)
    longlist = delete_bewertung(longlist)
    
    # Anzeige und Struktur der Seite in merge_dataframes, um immer aktuelle session states zu haben und dabei korrekte übergabe von Daten
    col1, col2 = st.columns([5, 1])
    with col1:
        st.header("Bewertung der Nachhaltigkeitspunkte (Longlist)")
    with col2:
        container = st.container(border=True)
        with container:
                count_bewertete_punkte()
                
    display_grid(longlist)
    save_state()

# Set initial next_id if not present
if 'next_id' not in st.session_state:
    st.session_state.next_id = 1

next_id = st.session_state.next_id

def reset_session_state_keys():
    keys_to_reset = [
        "auswirkung_option", "auswirkung_art_option", "auswirkung_art_option_pos",
        "ausmass_neg_tat", "umfang_neg_tat", "behebbarkeit_neg_tat",
        "ausmass_neg_pot", "umfang_neg_pot", "behebbarkeit_neg_pot", "wahrscheinlichkeit_neg_pot",
        "ausmass_pos_tat", "umfang_pos_tat", "ausmass_pos_pot", "umfang_pos_pot", "behebbarkeit_pos_pot",
        "art_finanziell", "wahrscheinlichkeit_finanziell", "ausmass_finanziell", "auswirkung_finanziell"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def bewertung_Uebersicht():
    if 'longlist' not in st.session_state or st.session_state['longlist'].empty:
        st.write('0% der Inhalte der Longlist wurden bewertet.')
        st.progress(0)
        return  # Beendet die Funktion, wenn keine Longlist vorhanden ist

    # Zählen der Anzahl der Bewertungen in der Longlist
    bewertung_counts = st.session_state['longlist']['Bewertet'].value_counts()

    # Berechnen des Prozentsatzes der "Ja"-Bewertungen
    total_bewertungen = bewertung_counts.sum()
    ja_bewertungen = bewertung_counts.get('Ja', 0)
    ja_prozent = int((ja_bewertungen / total_bewertungen) * 100) if total_bewertungen > 0 else 0

    # Anzeigen des Prozentsatzes mit einer Fortschrittsleiste
    st.write(f'davon wurden {ja_prozent}% bewertet')
    st.progress(ja_prozent)

# Anzahl der Punkte in der Longlist für die Darstellung in der Übersicht
def anzahl_punkte_Longlist():
    count = 0  # Standardwert auf 0 setzen
    if 'combined_df' in st.session_state and not st.session_state.combined_df.empty:
        count = len(st.session_state.combined_df)
    st.metric(label="Anzahl der Punkte in der Longlist:", value=count)

# Funktion, die zählt wie viele themespezifische Punkte in der Longlist sind. Inhalte werden aufgenommen wenn combined_df "Top-Down|Top-Down Bewertung|Top-Down & Top-Down Bewertung" enthält. 
def count_top_down_points():
    count = 0
    if 'combined_df' in st.session_state:
        combined_df = st.session_state.combined_df
        # Filtern der Zeilen, die die angegebenen Schlüsselwörter enthalten
        count = combined_df[combined_df['Quelle'].str.contains("Top-Down|Top-Down Bewertung|Top-Down & Top-Down Bewertung", na=False)].shape[0]
        # Ausgabe der Anzahl als st.metric
        st.metric(label="davon aus themenspezifischer ESRS:", value=count)
        
# Funktion, die zählt wie viele interne Punkte in der Longlist sind. Inhalte werden aufgenommen wenn combined_df "Intern|Eigene|Eigene & Intern" enthält
def count_internal_points():
    count = 0
    if 'combined_df' in st.session_state:
        combined_df = st.session_state.combined_df
        # Filtern der Zeilen, die die angegebenen Schlüsselwörter enthalten
        count = combined_df[combined_df['Quelle'].str.contains("Intern|Eigene|Eigene & Intern", na=False)].shape[0]
        # Ausgabe der Anzahl als st.metric
        st.metric(label="davon interne Punkte:", value=count)
    
# Funktio, die zählt wie viele Stakeholderpunkte in der Longlist sind. "~combined_df" bedeutet, dass alle Zeilen aus der Longlist genommen werden, die nicht "Top-Down|Top-Down Bewertung|Top-Down..." sind
def count_stakeholder_points():
    count = 0
    if 'combined_df' in st.session_state:
        combined_df = st.session_state.combined_df
        # Filtern der Zeilen, die die angegebenen Schlüsselwörter enthalten
        count = combined_df[~combined_df['Quelle'].str.contains("Top-Down|Top-Down Bewertung|Top-Down & Top-Down Bewertung|Intern|Eigene|Eigene & Intern", na=False)].shape[0]
        # Ausgabe der Anzahl als st.metric
        st.metric(label="davon externe Punkte:", value=count)

# Methode, die die Anzahl der bewerteten Punkte in der Longlist zählt und den Prozentsatz berechnet für die Übersicht
def count_bewertete_punkte_übersicht():
    if 'longlist' in st.session_state:
        # Erstellen einer Kopie des DataFrames
        longlist_copy_2 = st.session_state.longlist.copy()
        # Zählen der Zeilen, die in der Spalte 'Bewertung' den Wert 'Ja' haben
        yes_count = longlist_copy_2[longlist_copy_2['Bewertet'] == 'Ja'].shape[0]
        # Gesamtanzahl der Zeilen
        total_count = longlist_copy_2.shape[0]
        # Berechnung des Prozentsatzes
        if total_count > 0:
            percentage = (yes_count / total_count) * 100
        else:
            percentage = 0
        # Ausgabe des Prozentsatzes als st.metric
        st.metric(label="Prozentsatz der 'Ja'-Bewertungen:", value=f"{percentage:.2f}%")

def display_page():

    merge_dataframes()
    display_selected_data()
    
    with st.expander("Bewertungen"):
        Bewertungsanzeige()
    

    