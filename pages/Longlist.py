import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import altair as alt
import numpy as np
import pickle
import matplotlib.pyplot as plt

#---------------------------------- Sitzungszustand-Management ----------------------------------#

# Funktion zum Speichern des Zustands
def save_state():
    with open('SessionStates.pkl', 'wb') as f:
        pickle.dump(dict(st.session_state), f)

#----------- Abrufen der IROs aus Themenspezifischer ESRS, Interne und Externe Nachhaltigkeitspunkte -------------#

# Abruf der Stakeholder IROs
def stakeholder_Nachhaltigkeitspunkte():
    # Initialisiere DataFrame falls nicht vorhanden
    if 'stakeholder_punkte_filtered' not in st.session_state:
        st.session_state.stakeholder_punkte_filtered = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "Stakeholder Gesamtbew", "Stakeholder Bew Finanzen", "Stakeholder Bew Auswirkung", "Quelle"])	
    
    # Erstelle eine Kopie des DataFrame
    selected_rows_st = st.session_state.stakeholder_punkte_filtered.copy()

    # Speichere die ausgewählten Zeilen im session_state
    st.session_state.selected_rows_st = selected_rows_st
    
    return selected_rows_st

# Abruf der internen Nachhaltigkeitspunkte
def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
    # Erstellen Sie eine Kopie von df2
    df4 = st.session_state.df2.copy()
    df4['Quelle'] = 'Eigene'
    return df4

# Abruf der themenspezifischen ESRS-Nachhaltigkeitspunkte
def Themenspezifische_ESRS():
    # Überprüfen, ob 'relevance_selection' im session_state vorhanden ist
    if 'relevance_selection' in st.session_state:
        relevance_selection = st.session_state['relevance_selection']
        
        # Erstellen eines DataFrames aus den ausgewählten Punkten
        data = []
        for key, value in relevance_selection.items():
            # Ensure value is a boolean and key starts with 'Relevant_'
            if isinstance(value, bool) and value and key.startswith('Relevant_'):
                data.append(extract_data_from_key(key))
        
        selected_points_df = pd.DataFrame(data)
        selected_points_df['Quelle'] = 'Themenspezifische_ESRS Bewertung'
        
        # Speichern des DataFrame 'selected_points_df' im session_state
        st.session_state['selected_points_df'] = selected_points_df
        return selected_points_df
    else:
        # Return an empty DataFrame if 'relevance_selection' is not in session_state
        return pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema", "Quelle"])
    
#---------------------------------- Datenextraktion und Schlüssel-Zuordnung ----------------------------------#

# Extrahiert der Daten basierend auf dem Schlüssel (key)
def extract_data_from_key(key):
    start, end, suffix = determine_key_suffix(key)  # Bestimmt Start- und Endposition basierend auf dem Suffix
    
    if start is not None:
        unterthema = key[start:end].replace('_', ' ') # Entfernt Unterstriche im Schlüssel
        thema, unterthema, unter_unterthema = map_key_to_theme_and_subthemes(key, unterthema) # Zuordnung der Themen und Unterthemen
        return {
            'Thema': thema,
            'Unterthema': unterthema,
            'Unter-Unterthema': unter_unterthema
        }
    else:
         # Falls der Schlüssel nicht gemappt werden kann, Rückgabe von 'Unbekannt'
        return {
            'Thema': 'Unbekannt',
            'Unterthema': 'Unbekannt',
            'Unter-Unterthema': 'Unbekannt'
        }

# Filtered die als "Relevant" markierten Punkte aus dem relevance_selection aus der Themenspezifischen ESRS- Bewertung
def determine_key_suffix(key):
    suffixes = ['E1', 'E2', 'E3', 'E4', 'E5', 'S1', 'S2', 'S3', 'S4', 'G1']  # Mögliche Suffixe
    for suffix in suffixes:
        if key.endswith(suffix):  # Überprüft, ob der Schlüssel mit einem Suffix endet
            start = key.find('Relevant_') + len('Relevant_')  # Startposition nach 'Relevant_'
            end = key.find(f'_{suffix}')  # Endposition vor dem Suffix
            return start, end, suffix
    return None, None, None  # Rückgabe von None, falls kein Suffix gefunden wird

# Zuordnung von Thema und Unterthema basierend auf dem Schlüssel
def map_key_to_theme_and_subthemes(key, unterthema_raw):
    thema_map = {
        # Zuordnung der Themen auf Basis der Suffixe
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

# ---------- Zuordnung der Themen und Unterthemen basierend auf dem Schlüssel ----------#

# Zuordnung von Biodiversität
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

# Zuordnung der eigenen Belegschaft
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

# Zuordnung der Belegschaft Lieferkette
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

# Zuordnung der betroffenen Gemeinschaften
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

# Zuordnung der Verbraucher und Endnutzer
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

#---------------------------------- Bewertung der IROs ----------------------------------#

# Initialisiert die 'Bewertet'-Spalte im 'longlist'-DataFrame
def initialize_bewertet_column(longlist):
    # Überprüft, ob 'selected_data' im session_state vorhanden ist
    if 'selected_data' in st.session_state:
        # Setzt die 'Bewertet'-Spalte auf 'Ja', wenn die ID in den ausgewählten Daten enthalten ist, ansonsten auf 'Nein'
        longlist['Bewertet'] = longlist['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        # Wenn keine ausgewählten Daten vorhanden sind, wird die gesamte Spalte auf 'Nein' gesetzt
        longlist['Bewertet'] = 'Nein'
    return longlist  # Gibt den aktualisierten DataFrame zurück

# Funktion zum Absenden der Bewertung
def submit_bewertung(longlist, ausgewaehlte_werte):
    # Wenn der Button "Bewertung absenden" in der Sidebar gedrückt wird
    if st.sidebar.button("📤 Bewertung absenden"):
        # Überprüft, ob in den ausgewählten Werten mindestens eine Checkbox aktiviert ist
        if not any(ausgewaehlte_werte.values()):
            st.error("Bitte wählen Sie eine Checkbox in der Liste aus.")  # Zeigt eine Fehlermeldung an
            return longlist  # Gibt den ursprünglichen DataFrame zurück

        # Überprüft, ob im session_state mindestens eine ausgewählte Zeile vorhanden ist
        if 'selected_rows' not in st.session_state or not st.session_state['selected_rows']:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")  # Fehlermeldung
            return longlist  # Gibt den ursprünglichen DataFrame zurück

        # Erzeugt einen neuen DataFrame basierend auf den ausgewählten Zeilen
        new_data = pd.DataFrame(st.session_state['selected_rows'])
        # Entfernt die Spalte '_selectedRowNodeInfo', falls vorhanden
        if '_selectedRowNodeInfo' in new_data.columns:
            new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)

        # Mappings zur Umwandlung der Slider-Werte in numerische Werte für die finanzielle Bewertung (Skala 0-5)
        ausmass_finanziell_mapping = {
            "Sehr gering": 0, "Gering": 1, "Mäßig": 2, "Durchschnittlich": 3, "Erhöht": 4, "Stark": 5, "Extrem": 6
        }
        wahrscheinlichkeit_finanziell_mapping = {
            "Tritt nicht ein": 0, "Unwahrscheinlich": 1, "Eher unwahrscheinlich": 2, "Möglich":3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
        }

        # Mappings zur Umwandlung der Slider-Werte in numerische Werte für die negative Tat-Auswirkungsbewertung (Skala 0-5)
        ausmass_neg_tat_mapping = {
             "Sehr gering": 0, "Gering": 1, "Mäßig": 2, "Durchschnittlich": 3, "Erhöht": 4, "Stark": 5, "Extrem": 6
        }
        umfang_neg_tat_mapping = {
            "Punktuell": 0, "Lokal": 1, "Subregional": 2, "Regional":3,  "National": 4, "International": 5, "Global": 6
        }
        behebbarkeit_neg_tat_mapping = {
            "Kein Aufwand": 0, "Minimaler Aufwand": 1, "Geringer Aufwand": 2, "Mäßiger Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
        }

        # Mappings zur Umwandlung der Slider-Werte für potenzielle negative Auswirkungen (Skala 0-5)
        ausmass_neg_pot_mapping = {
             "Sehr gering": 0, "Gering": 1, "Mäßig": 2, "Durchschnittlich": 3, "Erhöht": 4, "Stark": 5, "Extrem": 6
        }
        umfang_neg_pot_mapping = {
            "Punktuell": 0, "Lokal": 1, "Subregional": 2, "Regional":3,  "National": 4, "International": 5, "Global": 6
        }
        behebbarkeit_neg_pot_mapping = {
            "Kein Aufwand": 0, "Minimaler Aufwand": 1, "Geringer Aufwand": 2, "Mäßiger Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
        }
        wahrscheinlichkeit_neg_pot_mapping = {
            "Tritt nicht ein": 0, "Unwahrscheinlich": 1, "Eher unwahrscheinlich": 2, "Möglich":3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
        }

        # Mappings zur Umwandlung der Slider-Werte für tatsächliche und potenzielle positive Auswirkungen (Skala 0-5)
        ausmass_pos_tat_mapping = {
             "Sehr gering": 0, "Gering": 1, "Mäßig": 2, "Durchschnittlich": 3, "Erhöht": 4, "Stark": 5, "Extrem": 6
        }
        umfang_pos_tat_mapping = {
           "Punktuell": 0, "Lokal": 1, "Subregional": 2, "Regional":3,  "National": 4, "International": 5, "Global": 6
        }
        ausmass_pos_pot_mapping = {
             "Sehr gering": 0, "Gering": 1, "Mäßig": 2, "Durchschnittlich": 3, "Erhöht": 4, "Stark": 5, "Extrem": 6
        }
        umfang_pos_pot_mapping = {
            "Punktuell": 0, "Lokal": 1, "Subregional": 2, "Regional":3,  "National": 4, "International": 5, "Global": 6
        }
        behebbarkeit_pos_pot_mapping = {
           "Kein Aufwand": 0, "Minimaler Aufwand": 1, "Geringer Aufwand": 2, "Mäßiger Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
        }

        # Kombiniert alle Bewertungen zu einem String für die Auswirkungsbewertung
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

        new_data['Auswirkung'] = auswirkung_string  # Fügt die Auswirkungsbewertung in den DataFrame ein

        # Kombiniert alle Bewertungen zu einem String für die finanzielle Bewertung
        finanziell_string = f"{ausgewaehlte_werte.get('art_finanziell', '')} ; {ausgewaehlte_werte.get('ausmass_finanziell', '')} ; {ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', '')}"
        new_data['Finanziell'] = finanziell_string  # Fügt die finanzielle Bewertung in den DataFrame ein

        # Berechnung des Scores für die finanzielle Bewertung (addition statt Multiplikation)
        new_data['Score Finanzen'] = np.round((
            (ausmass_finanziell_mapping.get(ausgewaehlte_werte.get('ausmass_finanziell', 'Sehr gering'), 0) +
            wahrscheinlichkeit_finanziell_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', 'Tritt nicht ein'), 0)) / 12 * 1000
            ), 1)

        # Berechnung Tatsächliche negative Auswirkungen (addition statt Multiplikation)
        tatsaechlich_negativ = np.round((
            (ausmass_neg_tat_mapping.get(ausgewaehlte_werte.get('ausmass_neg_tat', 'Sehr gering'), 0) +
            umfang_neg_tat_mapping.get(ausgewaehlte_werte.get('umfang_neg_tat', 'Punktuell'), 0) +
            behebbarkeit_neg_tat_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_tat', 'Kein Aufwand'), 0)) / 18 * 1000
            ), 1)

        # Berechnung Potenzielle negative Auswirkungen (addition statt Multiplikation)
        potentiell_negativ = np.round((
            (ausmass_neg_pot_mapping.get(ausgewaehlte_werte.get('ausmass_neg_pot', 'Sehr gering'), 0) +
            umfang_neg_pot_mapping.get(ausgewaehlte_werte.get('umfang_neg_pot', 'Punktuell'), 0) +
            behebbarkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_pot', 'Kein Aufwand'), 0) +
            wahrscheinlichkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', 'Tritt nicht ein'), 0)) / 24 * 1000
            ), 1)

        # Berechnung Tatsächliche positive Auswirkungen (addition statt Multiplikation)
        tatsaechlich_positiv = np.round((
            (ausmass_pos_tat_mapping.get(ausgewaehlte_werte.get('ausmass_pos_tat', 'Sehr gering'), 0) +
            umfang_pos_tat_mapping.get(ausgewaehlte_werte.get('umfang_pos_tat', 'Punktuell'), 0)) / 12 * 1000
            ), 1)

        # Berechnung Potenzielle positive Auswirkungen (addition statt Multiplikation)
        potentiell_positiv = np.round((
            (ausmass_pos_pot_mapping.get(ausgewaehlte_werte.get('ausmass_pos_pot', 'Sehr gering'), 0) +
            umfang_pos_pot_mapping.get(ausgewaehlte_werte.get('umfang_pos_pot', 'Punktuell'), 0) +
            behebbarkeit_pos_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_pos_pot', 'Kein Aufwand'), 0)) / 18 * 1000
            ), 1)

        # Berechnung des Gesamtscores für die Auswirkungsbewertung (Addition statt Multiplikation)
        new_data['Score Auswirkung'] = tatsaechlich_negativ + tatsaechlich_positiv + potentiell_negativ + potentiell_positiv

        # Aktualisiert den `selected_data` DataFrame im session_state
        if 'selected_data' in st.session_state:
            st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
            # Entfernt doppelte Einträge basierend auf der ID-Spalte
            st.session_state.selected_data.drop_duplicates(subset='ID', keep='last', inplace=True)
        else:
            # Erstellt neuen `selected_data` DataFrame, wenn er noch nicht vorhanden ist
            st.session_state.selected_data = new_data

        # Aktualisiert die 'Bewertet'-Spalte basierend auf den IDs im `selected_data` DataFrame
        longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        st.success("Bewertung abgesendet")  # Zeigt eine Erfolgsmeldung an

    return longlist  # Gibt den aktualisierten DataFrame zurück



# Funktion zum Löschen von Bewertungen
def delete_bewertung(longlist):
    st.sidebar.markdown("---")  # Trennlinie in der Sidebar
    st.sidebar.write("**Bewertungen löschen**")  # Titel in der Sidebar

    # Überprüfen, ob es bereits ausgewählte Daten gibt
    if 'selected_data' in st.session_state:
        selected_data_ids = st.session_state.selected_data['ID'] if 'ID' in st.session_state.selected_data.columns else []

        # Button zum Löschen von Bewertungen
        if st.sidebar.button("Bewertung löschen"):
            # Überprüfen, ob Zeilen ausgewählt wurden
            if 'selected_rows' in st.session_state and st.session_state['selected_rows']:
                # Extrahieren der IDs der ausgewählten Zeilen
                selected_row_ids = [row['ID'] for row in st.session_state['selected_rows']]
                # Filtern der zu löschenden Zeilen in den gespeicherten Daten
                rows_to_delete = st.session_state.selected_data[st.session_state.selected_data['ID'].isin(selected_row_ids)]
                
                # Wenn keine Bewertung vorhanden ist, die gelöscht werden kann
                if rows_to_delete.empty or all(longlist[longlist['ID'].isin(selected_row_ids)]['Bewertet'] == 'Nein'):
                    st.error("Keine Bewertung zum Löschen vorhanden.")  # Fehlermeldung
                else:
                    # Entfernen der ausgewählten Zeilen aus dem `selected_data` DataFrame
                    st.session_state.selected_data = st.session_state.selected_data[~st.session_state.selected_data['ID'].isin(selected_row_ids)]
                    # Aktualisieren der 'Bewertet'-Spalte in der Longlist
                    longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
                    
                    # Wenn alle Bewertungen gelöscht wurden, wird der `selected_columns` DataFrame geleert
                    if st.session_state.selected_data.empty:
                        st.session_state['selected_columns'] = pd.DataFrame()

                    st.success("Bewertung erfolgreich gelöscht.")  # Erfolgsmeldung
            else:
                st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung löschen.")  # Fehlermeldung, wenn keine Zeile ausgewählt wurde

    return longlist  # Rückgabe der aktualisierten Longlist

# Funktion zur Anzeige der ausgewählten Daten
def display_selected_data():
    # Überprüfen, ob es ausgewählte Daten gibt und ob diese nicht leer sind
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        # Fehlende Werte in den Spalten 'Thema', 'Unterthema' und 'Unter-Unterthema' mit einem leeren String füllen
        for column in ['Thema', 'Unterthema', 'Unter-Unterthema']:
            st.session_state.selected_data[column] = st.session_state.selected_data[column].fillna('')

        # Auswahl der benötigten Spalten aus dem `selected_data` DataFrame
        selected_columns = st.session_state.selected_data[['ID', 'Auswirkung', 'Finanziell', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']]

        # Wenn die `combined_df` Daten existieren und die benötigten Spalten enthalten, diese hinzufügen
        if 'combined_df' in st.session_state and all(col in st.session_state.combined_df.columns for col in ['Stakeholder Gesamtbew', 'Stakeholder Bew Finanzen', 'Stakeholder Bew Auswirkung']):
            combined_df_with_numerical_ratings = st.session_state.combined_df[['ID', 'Stakeholder Gesamtbew', 'Stakeholder Bew Finanzen', 'Stakeholder Bew Auswirkung']]
            # Zusammenführen der Daten basierend auf der 'ID'-Spalte
            selected_columns = pd.merge(selected_columns, combined_df_with_numerical_ratings, on='ID', how='left')
        
        # Speichern der `selected_columns` im session_state
        st.session_state['selected_columns'] = selected_columns

# Funktion zur Anzeige der Bewertungen
def Bewertungsanzeige():
    # Überprüfen, ob `selected_columns` im session_state existiert und nicht leer ist
    if 'selected_columns' not in st.session_state or st.session_state['selected_columns'].empty:
        st.info('Keine Bewertung vorhanden. Bitte fügen Sie eine Bewertung hinzu.')  # Info-Meldung, wenn keine Bewertung vorhanden ist
        return  # Beendet die Funktion, wenn keine Bewertung existiert

    # Überprüfen, ob eine Longlist vorhanden ist
    if 'longlist' not in st.session_state:
        st.info('Keine Longlist vorhanden. Bitte fügen Sie eine Longlist hinzu.')  # Info-Meldung, wenn keine Longlist vorhanden ist
        return  # Beendet die Funktion, wenn keine Longlist existiert

    # Extrahiert die IDs aus der Longlist
    longlist_ids = st.session_state['longlist']['ID'].unique()
    # Filtern der `selected_columns` basierend auf den IDs, die in der Longlist existieren
    selected_columns = st.session_state['selected_columns']
    selected_columns = selected_columns[selected_columns['ID'].isin(longlist_ids)]
    # Speichern der gefilterten `selected_columns` im session_state
    st.session_state['selected_columns'] = selected_columns

    # Dropdown zur Auswahl einer ID
    selected_id = st.selectbox('ID auswählen', selected_columns['ID'].unique())

    # Filtern der Zeile mit der ausgewählten ID
    selected_row = selected_columns[selected_columns['ID'] == selected_id]

    # Wenn die gefilterte Zeile nicht leer ist
    if not selected_row.empty:
        # Speichern der ausgewählten Bewertung im session_state
        st.session_state['selected_evaluation'] = selected_row

        # Aufteilen des 'Auswirkung'-Strings in einzelne Teile
        auswirkung_parts = selected_row['Auswirkung'].values[0].split(';')

        # Aufteilen des 'Finanziell'-Strings in einzelne Teile
        finanziell_parts = selected_row['Finanziell'].values[0].split(';')

        # Mapping der Teile von 'Auswirkung' zu spezifischen Bezeichnungen
        auswirkung_mapping = {
            1: 'Eigenschaft',
            2: 'Art',
            3: 'Ausmaß',
            4: 'Umfang',
            5: 'Behebarkeit',
            6: 'Wahrscheinlichkeit'
        }

        # Mapping der Teile von 'Finanziell' zu spezifischen Bezeichnungen
        finanziell_mapping = {
            1: 'Art',
            2: 'Ausmaß',
            3: 'Wahrscheinlichkeit'
            
        }

        # Erstellen von drei Spalten zur Anzeige der Details
        col1, col2, col3 = st.columns([1, 1, 1])

        # Anzeige der Auswirkung
        with col1:
            st.write("**Auswirkung**")
            for i, part in enumerate(auswirkung_parts, start=1):
                if i in auswirkung_mapping:
                    st.write(f'{auswirkung_mapping[i]}:', part.strip())  # Zeigt die entsprechenden Teile der Auswirkung an
                else:
                    st.write(f'Auswirkung Teil {i}:', part.strip())  # Zeigt sonst die Auswirkungsteile ohne Mapping an
            st.write('Score:', selected_row['Score Auswirkung'].values[0])  # Zeigt den Score für die Auswirkung

        # Anzeige der Finanziellen Bewertung
        with col2:
            st.write("**Finanziell**")
            for i, part in enumerate(finanziell_parts, start=1):
                if i in finanziell_mapping:
                    st.write(f'{finanziell_mapping[i]}:', part.strip())  # Zeigt die entsprechenden Teile der finanziellen Bewertung an
                else:
                    st.write(f'Finanziell Teil {i}:', part.strip())  # Zeigt sonst die Finanziellen Teile ohne Mapping an
            st.write('Score:', selected_row['Score Finanzen'].values[0])  # Zeigt den Score für die finanzielle Bewertung

        # Weitere Aktionen oder Informationen können in der dritten Spalte angezeigt werden
        with col3:
            pass  # Hier könnten zusätzliche Informationen oder Aktionen hinzugefügt werden

        # Speichern der Bewertung in der Liste `all_evaluations` im session_state
        if 'all_evaluations' not in st.session_state:
            st.session_state['all_evaluations'] = []  # Initialisiert die Liste, wenn sie nicht existiert

        # Speichern der Bewertung in einem Dictionary
        evaluation = {
            'ID': selected_row['ID'].values[0],
            'Auswirkung': selected_row['Auswirkung'].values[0],
            'Score Auswirkung': selected_row['Score Auswirkung'].values[0],
            'Finanziell': selected_row['Finanziell'].values[0],
            'Score Finanzen': selected_row['Score Finanzen'].values[0]
        }

        # Hinzufügen der Bewertung zur Liste `all_evaluations`
        st.session_state['all_evaluations'].append(evaluation)

    # Zustand speichern nach jeder Änderung
    save_state()  # Speichert den aktuellen Zustand im session_state


#---------------------------------- Anzeigen der Longlist im Aggrid ----------------------------------#

def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)  # Erzeugt eine GridOptionsBuilder-Instanz basierend auf dem DataFrame `longlist`
    gb.configure_side_bar() # Fügt eine Sidebar hinzu, die Optionen für Filter und Einstellungen enthält
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)  # Konfiguriert die Zeilenauswahl auf 'single' (nur eine Zeile gleichzeitig wählbar)
    gb.configure_column('ID', width=70) # Konfiguriert die Spalte 'ID' mit einer festen Breite von 70 Pixeln
    gb.configure_column('Bewertet',  width=80) # Konfiguriert die Spalte 'Bewertet' mit einer festen Breite von 80 Pixeln
    gb.configure_column('Thema',  width=200) # Konfiguriert die Spalte 'Thema' mit einer festen Breite von 200 Pixeln
    grid_options = gb.build()
    grid_response = AgGrid(
        longlist,  # Der DataFrame, der als Grid angezeigt werden soll
        gridOptions=grid_options,  # Die erstellten Grid-Optionen
        enable_enterprise_modules=True,  # Aktiviert die Enterprise-Module für zusätzliche Funktionen
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Das Grid wird aktualisiert, wenn sich das Modell ändert
        fit_columns_on_grid_load=True  # Die Spalten werden beim Laden des Grids automatisch angepasst
    )
    st.session_state['selected_rows'] = grid_response['selected_rows']

#----------------- Zusammenführung der IROs aus interene, exterene, themen. ESRS. etc. ---------------#

# Erstellen Sie ein leeres Wörterbuch zur Speicherung von Inhalt-ID-Zuordnungen
content_id_map = {}

# Funktion zum Zusammenführen der verschiedenen DataFrames und Verwaltung der IDs
def merge_dataframes():
    global next_id  # Verwenden einer globalen Variablen, um die ID über Sitzungen hinweg zu speichern

    # Initialisiert das content_id_map im session_state, falls es noch nicht existiert
    if 'content_id_map' not in st.session_state:
        st.session_state.content_id_map = {}
    content_id_map = st.session_state.content_id_map

    # Abrufen der Daten aus verschiedenen Quellen (Themenspezifische_ESRS, Stakeholder, Eigene)
    selected_points_df = Themenspezifische_ESRS()
    selected_rows_st = stakeholder_Nachhaltigkeitspunkte()
    df4 = eigene_Nachhaltigkeitspunkte()

    # Kombinieren aller Daten in einem DataFrame
    combined_df = pd.concat([selected_points_df, df4, selected_rows_st], ignore_index=True)

    # Entfernen von Zeilen, die nur NaN-Werte enthalten
    combined_df = combined_df.dropna(how='all')

    # Entfernen von Leerzeichen in den Spalten 'Thema', 'Unterthema' und 'Unter-Unterthema'
    combined_df['Thema'] = combined_df['Thema'].str.strip()
    combined_df['Unterthema'] = combined_df['Unterthema'].str.strip()
    combined_df['Unter-Unterthema'] = combined_df['Unter-Unterthema'].str.strip()

    # Entfernen von Zeilen ohne Thema
    combined_df = combined_df.dropna(subset=['Thema'])

    # Gruppieren nach 'Thema', 'Unterthema' und 'Unter-Unterthema' und Zusammenführen der 'Quelle'-Werte
    combined_df = combined_df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema']).agg({'Quelle': lambda x: ' & '.join(sorted(set(x)))}).reset_index()

    # Hinzufügen der Stakeholder-Bewertungen in den kombinierten DataFrame
    combined_df = pd.merge(combined_df, selected_rows_st[['Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Gesamtbew', 'Stakeholder Bew Finanzen', 'Stakeholder Bew Auswirkung']], on=['Thema', 'Unterthema', 'Unter-Unterthema'], how='left')

    # Entfernen von Duplikaten
    combined_df = combined_df.drop_duplicates(subset=['Thema', 'Unterthema', 'Unter-Unterthema'])

    # Hinzufügen einer 'ID'-Spalte
    combined_df.insert(0, 'ID', None)

    # Bestimmen der nächsten verfügbaren ID
    if 'combined_df' in st.session_state and not st.session_state.combined_df.empty:
        max_existing_id = st.session_state.combined_df['ID'].max()  # Maximal vorhandene ID finden
        next_id = max(max_existing_id + 1, next_id)
    else:
        next_id = 1  # Beginnt bei 1, falls noch keine IDs vorhanden sind

    # Zuweisen der IDs zu den Einträgen
    for index, row in combined_df.iterrows():
        content = (row['Thema'], row['Unterthema'], row['Unter-Unterthema'])  # Erstellen eines Identifikators

        # Überprüfen, ob der Inhalt bereits eine ID hat
        if content in content_id_map:
            id = content_id_map[content]  # Existierende ID verwenden
        else:
            id = next_id  # Neue ID zuweisen
            content_id_map[content] = id  # Speichern der Zuordnung
            next_id += 1  # Erhöhen der ID für den nächsten Eintrag

        # Setzen der ID im DataFrame
        combined_df.at[index, 'ID'] = id

    # Speichern des kombinierten DataFrames im session_state
    st.session_state.combined_df = combined_df

    # Kopie des DataFrames ohne Bewertungen und Quellen für die Longlist erstellen
    combined_df_without_numerical_rating_and_source = st.session_state.combined_df.drop(columns=['Stakeholder Gesamtbew', 'Stakeholder Bew Finanzen', 'Stakeholder Bew Auswirkung', 'Quelle'])
    st.session_state['combined_df_without_numerical_rating_and_source'] = combined_df_without_numerical_rating_and_source  # Speichern im session_state

    # Erstellung eines neuen DataFrames 'longlist' für die Anzeige
    longlist = pd.DataFrame(combined_df_without_numerical_rating_and_source)

    # Initialisieren der 'Bewertet'-Spalte in der Longlist
    longlist = initialize_bewertet_column(longlist)

    # Speichern der Longlist im session_state
    st.session_state['longlist'] = longlist
    save_state()  # Zustand speichern

    # Initialisieren der Variablen für Bewertungen
    option = auswirkung_option = auswirkung_art_option = ausmass_neg_tat = umfang_neg_tat = behebbarkeit_neg_tat = ''
    ausmass_neg_pot = umfang_neg_pot = behebbarkeit_neg_pot = wahrscheinlichkeit_neg_pot = ''
    ausmass_pos_tat = umfang_pos_tat = ausmass_pos_pot = umfang_pos_pot = behebbarkeit_pos_pot = ''
    art_finanziell = wahrscheinlichkeit_finanziell = ausmass_finanziell  = ''

    # Sidebar für die Bewertungsoptionen
    st.sidebar.markdown('---')
    st.sidebar.write("**Bewertungen hinzufügen**")
    with st.sidebar:
        # Abschnitt für Auswirkungsbewertung
        with st.expander("Auwirkungsbewertung"):
            auswirkung_option = st.selectbox('Eigenschaft der Auswirkung:', ['Negative Auswirkung', 'Positive Auswirkung', 'Keine Auswirkung'], index=2, key="auswirkung_option")
            if auswirkung_option == 'Negative Auswirkung':
                # Weitere Optionen für negative Auswirkung
                auswirkung_art_option = st.selectbox('Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option")      
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    # Slider für tatsächliche negative Auswirkungen
                    ausmass_neg_tat = st.select_slider("Ausmaß:", options=["Sehr gering", "Gering", "Mäßig", "Durchschnittlich", "Erhöht", "Stark", "Extrem"], key="ausmass_neg_tat")
                    umfang_neg_tat = st.select_slider("Umfang:", options=["Punktuell", "Lokal", "Subregional", "Regional", "National", "International", "Global"], key="umfang_neg_tat")
                    behebbarkeit_neg_tat = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Minimaler Aufwand", "Geringer Aufwand", "Mäßiger Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    # Slider für potenzielle negative Auswirkungen
                    ausmass_neg_pot = st.select_slider("Ausmaß:", options=["Sehr gering", "Gering", "Mäßig", "Durchschnittlich", "Erhöht", "Stark", "Extrem"], key="ausmass_neg_pot")
                    umfang_neg_pot = st.select_slider("Umfang:", options=["Punktuell", "Lokal", "Subregional", "Regional", "National", "International", "Global"], key="umfang_neg_pot")
                    behebbarkeit_neg_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Minimaler Aufwand", "Geringer Aufwand", "Mäßiger Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_pot")
                    wahrscheinlichkeit_neg_pot = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Möglich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_neg_pot")
            elif auswirkung_option == 'Positive Auswirkung':
                # Optionen für positive Auswirkungen
                auswirkung_art_option = st.selectbox('Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option_pos")
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    # Slider für tatsächliche positive Auswirkungen
                    ausmass_pos_tat = st.select_slider("Ausmaß:", options=["Sehr gering", "Gering", "Mäßig", "Durchschnittlich", "Erhöht", "Stark", "Extrem"], key="ausmass_pos_tat")
                    umfang_pos_tat = st.select_slider("Umfang:", options=["Punktuell", "Lokal", "Subregional", "Regional", "National", "International", "Global"], key="umfang_pos_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    # Slider für potenzielle positive Auswirkungen
                    ausmass_pos_pot = st.select_slider("Ausmaß:", options=["Sehr gering", "Gering", "Mäßig", "Durchschnittlich", "Erhöht", "Stark", "Extrem"], key="ausmass_pos_pot")
                    umfang_pos_pot = st.select_slider("Umfang:", options=["Punktuell", "Lokal", "Subregional", "Regional", "National", "International", "Global"], key="umfang_pos_pot")
                    behebbarkeit_pos_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Minimaler Aufwand", "Geringer Aufwand", "Mäßiger Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_pos_pot")
    
        # Abschnitt für finanzielle Bewertung
        with st.expander("Finanzielle Bewertung"):
            art_finanziell = st.selectbox("Eigenschaft der Auswirkung:", ['Chance', 'Risiko', 'Keine Auswirkung'], index=2, key="art_finanziell")
            if art_finanziell != 'Keine Auswirkung':
                # Slider für finanzielle Auswirkungen
                ausmass_finanziell = st.select_slider("Ausmaß:", options=["Sehr gering", "Gering", "Mäßig", "Durchschnittlich", "Erhöht", "Stark", "Extrem"], key="ausmass_finanziell")
                wahrscheinlichkeit_finanziell = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Möglich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_finanziell")
                

    # Speichern der ausgewählten Werte in einem Dictionary
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
    }

    # Verschachtelte Funktion zum Zählen bewerteter Punkte
    def count_bewertete_punkte():
        if 'longlist' in st.session_state:
            # Überprüfen, ob die Longlist leer ist
            if st.session_state.longlist.empty:
                st.write("Keine Inhalte vorhanden")
                st.session_state['checkbox_state_6'] = False
                return  # Beendet die Funktion, wenn die Longlist leer ist
    
            # Zählen der bewerteten Punkte
            yes_count = st.session_state.longlist[st.session_state.longlist['Bewertet'] == 'Ja'].shape[0]
            total_count = st.session_state.longlist.shape[0]
            # Berechnung des Prozentsatzes
            if total_count > 0:
                percentage = (yes_count / total_count) * 100
            else:
                percentage = 0
    
            # Überprüfen, ob alle Punkte bewertet wurden
            if yes_count == total_count:
                st.write("Abgeschlossen ✔")
                st.session_state['checkbox_state_6'] = True
            else:
                st.write(f"{yes_count} von {total_count} Punkten bewertet.")
                st.session_state['checkbox_state_6'] = False
        else:
            st.write("Keine Inhalte vorhanden")
            st.session_state['checkbox_state_6'] = False

    # Bewertung, Löschen und Anzeigen der Longlist
    longlist = submit_bewertung(longlist, ausgewaehlte_werte)
    longlist = delete_bewertung(longlist)
    
    # Struktur für die Anzeige der Seite
    col1, col2 = st.columns([5, 1])
    with col1:
        st.header("Bewertung der Nachhaltigkeitspunkte (Longlist)")
    with col2:
        container = st.container(border=False)
        with container:
            count_bewertete_punkte()  # Zeigt den Bewertungsfortschritt an
    
    st.markdown("""
        Die Longlist enthält alle Punkte, die für die Bewertung berücksichtigt werden sollen, nachdem Sie alle vorherigen Schritte durchlaufen haben. Um eine Bewertung vorzunehmen, markieren Sie die Checkbox des gewünschten Punktes und wählen Sie die entsprechenden Bewertungskriterien in der Sidebar aus. Unterhalb der Longlist können Sie die bereits vorgenommenen Bewertungen einsehen und gegebenenfalls löschen. 
        Die Spalte "Bewertet" hilft Ihnen dabei, den Überblick zu behalten, welche Inhalte bereits bewertet wurden.
    """)
                
    # Anzeige der Longlist als Grid
    display_grid(longlist)
    save_state()  # Zustand speichern

# Initialisieren der next_id für die Verwaltung von IDs
if 'next_id' not in st.session_state:
    st.session_state.next_id = 1
next_id = st.session_state.next_id


def reset_session_state_keys():
    keys_to_reset = [
        "auswirkung_option", "auswirkung_art_option", "auswirkung_art_option_pos",
        "ausmass_neg_tat", "umfang_neg_tat", "behebbarkeit_neg_tat",
        "ausmass_neg_pot", "umfang_neg_pot", "behebbarkeit_neg_pot", "wahrscheinlichkeit_neg_pot",
        "ausmass_pos_tat", "umfang_pos_tat", "ausmass_pos_pot", "umfang_pos_pot", "behebbarkeit_pos_pot",
        "art_finanziell", "wahrscheinlichkeit_finanziell", "ausmass_finanziell"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]


#---------------------------------- Anzeigen für die Übersicht und aktuellen Stand ----------------------------------#

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
    nein_bewertung = total_bewertungen - ja_bewertungen

    # Anzeigen des Prozentsatzes mit einer Fortschrittsleiste
    st.write("sind in der Longlist enthalten.")
    st.write("Insgesamt wurden **" + str(ja_bewertungen) + "** Punkte bewertet.")
    st.write(f'Es fehlen noch: {nein_bewertung} Punkte.')
    st.progress(ja_prozent)


def bewertung_Uebersicht_Nein():
    # Zählen der Anzahl der Bewertungen in der Longlist
    bewertung_counts = st.session_state['longlist']['Bewertet'].value_counts()

    # Berechnen des Prozentsatzes der "Nein"-Bewertungen
    total_bewertungen = bewertung_counts.sum()
    nein_bewertungen = bewertung_counts.get('Nein', 0)
    nein_prozent = int((nein_bewertungen / total_bewertungen) * 100) if total_bewertungen > 0 else 0

    if nein_prozent == 0 and not st.session_state['longlist'].empty:
        st.session_state['checkbox_state_6'] = True
    else:
        st.session_state['checkbox_state_6'] = False
    
    return nein_prozent

# Anzahl der Punkte in der Longlist für die Darstellung in der Übersicht
def anzahl_punkte_Longlist():
    count = 0  # Standardwert auf 0 setzen
    if 'combined_df' in st.session_state and not st.session_state.combined_df.empty:
        count = len(st.session_state.combined_df)
    st.metric(label="**Longlist**", value=count)

# Funktion, die zählt wie viele themespezifische Punkte in der Longlist sind. Inhalte werden aufgenommen wenn combined_df "Themenspezifische_ESRS|Themenspezifische_ESRS Bewertung|Themenspezifische_ESRS & Themenspezifische_ESRS Bewertung" enthält. 
def count_top_down_points():
    count = 0
    if 'combined_df' in st.session_state:
        combined_df = st.session_state.combined_df
        # Filtern der Zeilen, die die angegebenen Schlüsselwörter enthalten
        count = combined_df[combined_df['Quelle'].str.contains("Themenspezifische_ESRS|Themenspezifische_ESRS Bewertung|Themenspezifische_ESRS & Themenspezifische_ESRS Bewertung", na=False)].shape[0]
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
    
# Funktio, die zählt wie viele Stakeholderpunkte in der Longlist sind. "~combined_df" bedeutet, dass alle Zeilen aus der Longlist genommen werden, die nicht "Themenspezifische_ESRS|Themenspezifische_ESRS Bewertung|Themenspezifische_ESRS..." sind
def count_stakeholder_points():
    count = 0
    if 'combined_df' in st.session_state:
        combined_df = st.session_state.combined_df
        # Filtern der Zeilen, die die angegebenen Schlüsselwörter enthalten
        count = combined_df[~combined_df['Quelle'].str.contains("Themenspezifische_ESRS|Themenspezifische_ESRS Bewertung|Themenspezifische_ESRS & Themenspezifische_ESRS Bewertung|Intern|Eigene|Eigene & Intern", na=False)].shape[0]
        # Ausgabe der Anzahl als st.metric
        st.metric(label="davon externe Punkte:", value=count)

# ---------------------------------- Anzeigen der Longlist Seite ----------------------------------#

def display_page():
    merge_dataframes()
    display_selected_data()
    
    with st.expander("Bewertungen"):
        Bewertungsanzeige()
    st.write(st.session_state['longlist'])
    st.write(st.session_state['selected_data'])
    st.write(st.session_state['selected_columns'])
    st.write(st.session_state['selected_evaluation'])