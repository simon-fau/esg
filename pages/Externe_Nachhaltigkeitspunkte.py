import streamlit as st  
import pandas as pd  
import pickle  
import os  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode 

#---------------------------------- Sitzungszustand-Management ----------------------------------#

# Konstante für die Pickl, in dem die session_states gespeichert werden
STATE_FILE = 'SessionStates.pkl'

# Funktion zum Laden des gespeicherten Sitzungszustands
def load_session_state():
    if os.path.exists(STATE_FILE):  # Überprüfe, ob die Datei existiert
        with open(STATE_FILE, 'rb') as f:  # Öffne die Datei im Lese- und Binärmodus
            return pickle.load(f)  # Lade den gespeicherten Zustand aus der Datei
    return {}  # Wenn die Datei nicht existiert, gib einen leeren Zustand zurück

# Funktion zum Speichern des aktuellen Sitzungszustands
def save_session_state(state):
    current_state = load_session_state()  # Lade den aktuellen Sitzungszustand
    combined_state = {**current_state, **state}  # Kombiniere den geladenen Zustand mit dem neuen Zustand
    with open(STATE_FILE, 'wb') as f:  # Öffne die Datei im Schreib- und Binärmodus
        pickle.dump(combined_state, f)  # Speichere den kombinierten Zustand in der Datei

# Lade den gespeicherten Sitzungszustand und aktualisiere den aktuellen Zustand
loaded_state = load_session_state()
st.session_state.update(loaded_state)

#---------------------------------- Initialisierung von Session-State-Variablen ----------------------------------#

# Initialisiere die DataFrame 'new_df_copy' im Sitzungszustand, falls sie noch nicht existiert
if 'new_df_copy' not in st.session_state:
    st.session_state.new_df_copy = pd.DataFrame(columns=['Stakeholder', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle'])

# Initialisiere die Variable 'stakeholder_punkte_filtered' im Sitzungszustand, falls sie noch nicht existiert
if 'stakeholder_punkte_filtered' not in st.session_state:
    st.session_state.stakeholder_punkte_filtered = []

# Initialisiere die Tabelle 'Einbezogene_Stakeholder' im Sitzungszustand, falls sie noch nicht existiert
if 'Einbezogene_Stakeholder' not in st.session_state:
    st.session_state.Einbezogene_Stakeholder = []

# Initialisiere die DataFrame 'ranking_table' im Sitzungszustand, falls sie noch nicht existiert
if 'ranking_table' not in st.session_state:
    st.session_state.ranking_table = pd.DataFrame()

# Initialisiere die DataFrame 'stakeholder_punkte_df' im Sitzungszustand mit den definierten Spalten, falls sie noch nicht existiert
if 'stakeholder_punkte_df' not in st.session_state:
    st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'AuswirkungRating', 'FinanzRating', 'Stakeholder Gesamtbew', 'Quelle'])

# Initialisiere die Liste 'uploaded_files' im Sitzungszustand, falls sie noch nicht existiert
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Initialisiere die Liste 'sidebar_companies' im Sitzungszustand, falls sie noch nicht existiert
if 'sidebar_companies' not in st.session_state:
    st.session_state.sidebar_companies = []

# Initialisiere die Liste 'valid_stakeholder' im Sitzungszustand, falls sie noch nicht existiert
if 'valid_stakeholder' not in st.session_state:
    st.session_state.valid_stakeholder = []

#---------------------------------- Erstellen eines Platzhalters zur Vergrößerung vertikaler Abstände ----------------------------------#

def plazhalter():
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

#---------------------------------- Funktionen zur Anpassung von Stakeholder-Daten ----------------------------------#

# Funktion zur Anpassung der Werte und Stakeholder-Namen in 'stakeholder_punkte_filtered' 
# basierend auf 'new_df_copy' für nicht einbezogene Stakeholder
def adjust_stakeholder_punkte_filtered(new_df_copy, stakeholder_punkte_filtered):
    # Überprüfen, ob die Spalte 'Status' in 'new_df_copy' vorhanden ist
    if 'Status' not in new_df_copy.columns:
        st.error("Die Spalte 'Status' fehlt in new_df_copy.")  # Fehlermeldung, falls die Spalte fehlt
        return stakeholder_punkte_filtered  # Gib den unveränderten DataFrame zurück
    
    # Iteriere über die Zeilen in 'new_df_copy', bei denen der Status 'nicht einbezogen' ist
    for idx, row in new_df_copy[new_df_copy['Status'] == 'nicht einbezogen'].iterrows():
        # Extrahiere den Namen des Stakeholders, das Thema, Unterthema und Unter-Unterthema aus der aktuellen Zeile
        stakeholder_name = row['Stakeholder']
        thema = row['Thema']
        unterthema = row['Unterthema']
        unter_unterthema = row['Unter-Unterthema']

        # Suche nach übereinstimmenden Einträgen in 'stakeholder_punkte_filtered'
        matches = stakeholder_punkte_filtered[
            (stakeholder_punkte_filtered['Stakeholder'].str.contains(stakeholder_name)) &  # Überprüfen, ob der Stakeholder-Name enthalten ist
            (stakeholder_punkte_filtered['Thema'] == thema) &  # Überprüfen, ob das Thema übereinstimmt
            (stakeholder_punkte_filtered['Unterthema'] == unterthema) &  # Überprüfen, ob das Unterthema übereinstimmt
            (stakeholder_punkte_filtered['Unter-Unterthema'] == unter_unterthema)  # Überprüfen, ob das Unter-Unterthema übereinstimmt
        ]
        
        # Aktualisiere die Werte für die gefundenen Übereinstimmungen
        for match_idx, match_row in matches.iterrows():
            # Subtrahiere die Werte aus 'new_df_copy' von den bestehenden Werten in 'stakeholder_punkte_filtered'
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Auswirkung'] -= row['Stakeholder Bew Auswirkung']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Finanzen'] -= row['Stakeholder Bew Finanzen']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Gesamtbew'] -= row['Stakeholder Gesamtbew']
            
            # Entferne den aktuellen Stakeholder-Namen aus der Liste der Stakeholder, um doppelte Einträge zu vermeiden
            updated_stakeholders = match_row['Stakeholder'].replace(stakeholder_name, '').replace(',,', ',').strip(', ')
            # Aktualisiere den Stakeholder-Namen in der Tabelle
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder'] = updated_stakeholders

    return stakeholder_punkte_filtered  # Gib den angepassten DataFrame zurück

 #---------------------------------- Dienstprogramme für Bewertungen und Filterung ----------------------------------#

# Funktion zur Umwandlung von textbasierten Bewertungen in numerische Werte
def get_numerical_rating(value):
    ratings = {
        'Wesentlich': 3,  # "Wesentlich" hat den höchsten Wert von 3
        'Eher Wesentlich': 2,  # "Eher Wesentlich" hat den Wert von 2
        'Eher nicht Wesentlich': 1,  # "Eher nicht Wesentlich" hat den Wert von 1
        'Nicht Wesentlich': 0  # "Nicht Wesentlich" hat den niedrigsten Wert von 0
    }
    return ratings.get(value, 0)  # Gib den entsprechenden Wert zurück, oder 0, falls der Wert nicht gefunden wird

# Funktion zur Aggregation von Stakeholder-Rankings basierend auf den Bewertungen
def aggregate_rankings(df):
    # Wandle die textbasierten Bewertungen in numerische Werte um
    df['Stakeholder Bew Auswirkung'] = df['Auswirkungsbezogene Bewertung'].apply(get_numerical_rating).astype(int)
    df['Stakeholder Bew Finanzen'] = df['Finanzbezogene Bewertung'].apply(get_numerical_rating).astype(int)
    
    # Berechne die Gesamtbewertung als Summe der beiden Bewertungen
    df['Stakeholder Gesamtbew'] = df['Stakeholder Bew Auswirkung'] + df['Stakeholder Bew Finanzen']
    
    # Fülle leere Felder in den Themen-Spalten mit Standardwerten
    df.fillna({'Thema': 'Unbekannt', 'Unterthema': 'Unbekannt', 'Unter-Unterthema': ''}, inplace=True)
    
    # Gruppiere die Daten nach Thema, Unterthema, Unter-Unterthema und Quelle und aggregiere die Bewertungen
    ranking = df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle']).agg({'Stakeholder Bew Auswirkung': 'sum', 'Stakeholder Bew Finanzen': 'sum', 'Stakeholder Gesamtbew': 'sum'}).reset_index()
    
    # Sortiere die aggregierten Daten nach der Gesamtbewertung in absteigender Reihenfolge
    ranking.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
    
    # Weise Platzierungen basierend auf der Gesamtbewertung zu
    ranking['Platzierung'] = ranking['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
    
    # Gib die relevanten Spalten des Rankings zurück
    return ranking[['Platzierung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']]

# Funktion zur Filterung von Stakeholdern basierend auf ihrer Gültigkeit, sodass nur Stakeholder verwendet werden, die in im Stakeholder-Managemnt (ranking_table) und in der AUswahl (Einbezogene_Stakeholder) enthalten sind
def filter_stakeholders():
    # Überprüfe, ob 'ranking_table' und 'Einbezogene_Stakeholder' im Sitzungszustand vorhanden sind
    if 'ranking_table' not in st.session_state or 'Einbezogene_Stakeholder' not in st.session_state:
        return []

    # Erstelle eine Menge gültiger Stakeholder-Gruppen basierend auf der 'ranking_table'
    valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist())
    
    # Filtere 'Einbezogene_Stakeholder', um nur gültige Stakeholder-Gruppen zu behalten
    filtered_table2 = [item for item in st.session_state.Einbezogene_Stakeholder if item in valid_stakeholders]

    return filtered_table2  # Gib die gefilterte Liste zurück
   
#---------------------------------- Darstellung von Tabellen mit AgGrid ----------------------------------#

# Funktion zur Darstellung von Daten in einer AgGrid-Tabelle. Methode als Vorlage für stakeholder_punkte und excel_upload
def display_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)  # Erstelle einen GridOptionsBuilder basierend auf dem DataFrame
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=15)  # Konfiguriere die Seitengröße für die Paginierung
    gb.configure_side_bar()  # Füge eine Seitenleiste für die Konfiguration hinzu
    gb.configure_grid_options(domLayout='autoHeight')  # Stelle das Layout auf 'autoHeight' für dynamische Höhenanpassung ein
    gb.configure_default_column(flex=1, minWidth=100, resizable=True, autoHeight=True)  # Konfiguriere die Standardoptionen für alle Spalten
    
    # Konfiguriere die "Platzierung"-Spalte als erste Spalte und fixiere sie links
    if 'Platzierung' in df.columns:
        gb.configure_column('Platzierung', pinned='left')
    
    # Verstecke die Spalten "Stakeholder" und "Quelle"
    if 'Stakeholder' in df.columns:
        gb.configure_column('Stakeholder', hide=True)

    if 'Quelle' in df.columns:
        gb.configure_column('Quelle', hide=True)
    
    # Erstelle die Grid-Optionen
    grid_options = gb.build()
    
    # Gib die AgGrid-Tabelle mit den erstellten Optionen zurück
    return AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED)

#---------------------------------- Stakeholder-Punkte anzeigen ----------------------------------#

# Funktion zur Anzeige der Stakeholder-Punkte-Tabelle
def stakeholder_punkte():
    # Überprüfen, ob 'stakeholder_punkte_filtered' im Sitzungszustand vorhanden ist
    if 'stakeholder_punkte_filtered' in st.session_state:
        # Sicherstellen, dass es sich um einen DataFrame handelt
        if isinstance(st.session_state.stakeholder_punkte_filtered, pd.DataFrame):
            # Überprüfen, ob die Spalte 'Stakeholder' im DataFrame existiert
            if 'Stakeholder' in st.session_state.stakeholder_punkte_filtered.columns:
                # Entferne Zeilen, in denen die 'Stakeholder'-Spalte leer oder nur Leerzeichen enthält
                st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_filtered[
                    st.session_state.stakeholder_punkte_filtered['Stakeholder'].str.strip() != ''
                ]
                
                # Speichere den aktualisierten Sitzungszustand
                save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})
                
                # Überprüfen, ob der DataFrame nicht leer ist
                if not st.session_state.stakeholder_punkte_filtered.empty:
                    # Zeige die Tabelle mit AgGrid an und speichere die Antwort
                    response = display_aggrid(st.session_state.stakeholder_punkte_filtered)
                    st.session_state.grid_response = response  # Speichere das Ergebnis der Grid-Interaktion
                    save_session_state({'grid_response': st.session_state.grid_response})  # Speichere den aktualisierten Zustand
                else:
                    # Zeige eine Nachricht an, wenn keine Daten vorhanden sind.Diese Rückmeldungen können geändert werden, für den Entwickler als Debugging-Hilfe. Aktuell sind die für den Endnutzer ausgelegt.
                    st.info("Keine Stakeholder-Bewertungen vorhanden.")
            else:
                # Zeige eine Fehlermeldung an, wenn die 'Stakeholder'-Spalte nicht existiert. Diese Rückmeldungen können geändert werden, für den Entwickler als Debugging-Hilfe. Aktuell sind die für den Endnutzer ausgelegt.
                st.info("Keine Stakeholder-Bewertungen vorhanden.")
        else:
            # Zeige eine Fehlermeldung an, wenn die Daten kein DataFrame sind. Diese Rückmeldungen können geändert werden, für den Entwickler als Debugging-Hilfe. Aktuell sind die für den Endnutzer ausgelegt.
            st.info("Keine Stakeholder-Bewertungen vorhanden.")
    else:
        # Zeige eine Nachricht an, wenn keine Stakeholder-Bewertungen im Sitzungszustand vorhanden sind.Diese Rückmeldungen können geändert werden, für den Entwickler als Debugging-Hilfe. Aktuell sind die für den Endnutzer ausgelegt.
        st.info("Keine Stakeholder-Bewertungen vorhanden.")

#---------------------------------- Seitenleiste und Fortschrittsanzeige ----------------------------------#

# Funktion zur Anzeige von Stakeholdern in der Seitenleiste. 
# Dabei werden nur Stakeholder angezeigt, die in 'valid_stakeholder' enthalten sind
def display_sidebar_items():
    # Entferne ungültige Stakeholder aus der Seitenleiste
    remove_invalid_stakeholders()

    # Zeige die Inhalte in der Seitenleiste an
    with st.sidebar:
        st.markdown("---")  # Trennlinie in der Seitenleiste

        # Multiselect-Box, um Stakeholder auszuwählen, die sowohl in 'Einbezogene_Stakeholder' 
        # als auch in 'sidebar_companies' enthalten sind
        valid_options = [stakeholder for stakeholder in st.session_state.Einbezogene_Stakeholder 
                         if stakeholder in st.session_state.sidebar_companies]
        selected_stakeholders = st.multiselect('Stakeholder-Bewertung entfernen:', valid_options)

        # Button zum Verschieben der ausgewählten Stakeholder von 'Einbezogene_Stakeholder' 
        # nach 'Ausgeschlossene_Stakeholder'
        if st.button('Entfernen'):
            move_stakeholders(selected_stakeholders)  # Verschiebe die ausgewählten Stakeholder

        st.markdown("---")  # Trennlinie in der Seitenleiste
        st.write("**Bereits in Bewertung aufgenommen:**")
        
        # Zeige alle Stakeholder an, die bereits in der Seitenleiste erscheinen
        for item in st.session_state.sidebar_companies:
            st.write(item)  # Zeige den Namen des Stakeholders in der Seitenleiste an

# Funktion zur Anzeige der Fortschrittsanzeige
def display_not_in_sidebar_count():
    filtered_table2 = filter_stakeholders()  # Filtere die gültigen Stakeholder

    if not filtered_table2:
        st.write("**Fortschritt:**")
        st.write("Keine Stakeholder in Bewertung aufgenommen.")  # Zeige eine Nachricht an, wenn keine Stakeholder bewertet wurden
        return
    
    # Zähle die Stakeholder, die noch nicht in der Seitenleiste erscheinen
    count = len([opt for opt in filtered_table2 if opt not in st.session_state.sidebar_companies])
    
    st.write("**Fortschritt:**")
    st.write(f"Anzahl fehlender Stakeholder-Bewertungen: {count}")  # Zeige die Anzahl der fehlenden Bewertungen an
    
    if count == 0:
        st.session_state['checkbox_state_5'] = True  # Setze den Zustand, wenn alle Stakeholder bewertet wurden
    else:
        st.session_state['checkbox_state_5'] = False  # Andernfalls setze den Zustand auf False


#---------------------------------- Status-Update und Datenaktualisierung ----------------------------------#

# Funktion zur Aktualisierung des Status von Stakeholdern in einem DataFrame. 
# Wenn es Änderungen im Stakeholder-Management oder in der Auswahl gibt, wird 'valid_stakeholder' aktualisiert
def update_status(df):
    # Sicherstellen, dass die Spalte 'Stakeholder' im DataFrame existiert, bevor die Funktion ausgeführt wird
    if 'Stakeholder' in df.columns:
        # Prüfen, ob 'Einbezogene_Stakeholder' und 'ranking_table' im Sitzungszustand existieren
        if 'Einbezogene_Stakeholder' in st.session_state and 'ranking_table' in st.session_state:
            # Erstelle eine Menge gültiger Stakeholder aus der 'ranking_table' und 'Einbezogene_Stakeholder'
            valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.Einbezogene_Stakeholder))
            # Aktualisiere die 'Status'-Spalte: 'einbezogen' für gültige Stakeholder, 'nicht einbezogen' für alle anderen
            df['Status'] = df['Stakeholder'].apply(lambda x: 'einbezogen' if x in valid_stakeholders else 'nicht einbezogen')
        else:
            # Falls keine gültigen Stakeholder gefunden werden, setze den Status auf 'nicht einbezogen'
            df['Status'] = 'nicht einbezogen'
    else:
        # Fehlermeldung, falls die Spalte 'Stakeholder' im DataFrame fehlt
        st.error("Die Spalte 'Stakeholder' fehlt im DataFrame.")
    return df  # Gib den aktualisierten DataFrame zurück


# Funktion zur Aktualisierung der Kopie der neuen Daten und Anpassung der Stakeholder-Punkte
def refresh_new_df_copy():
    # Überprüfen, ob 'new_df_copy' im Sitzungszustand existiert und ob es ein DataFrame ist
    if 'new_df_copy' in st.session_state and isinstance(st.session_state.new_df_copy, pd.DataFrame):
        # Sicherstellen, dass die Spalte 'Stakeholder' existiert
        if 'Stakeholder' not in st.session_state.new_df_copy.columns:
            st.error("Die Spalte 'Stakeholder' fehlt in new_df_copy.")  # Fehlermeldung, wenn die Spalte fehlt
            return
        
        # Sicherstellen, dass die Spalte 'Status' existiert, indem der Status aktualisiert wird
        if 'Status' not in st.session_state.new_df_copy.columns:
            st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
        
        # Nun die Stakeholder-Punkte basierend auf dem Status anpassen
        st.session_state.stakeholder_punkte_filtered = adjust_stakeholder_punkte_filtered(
            st.session_state.new_df_copy,
            st.session_state.stakeholder_punkte_filtered
        )
        # Den aktualisierten Sitzungszustand speichern
        save_session_state({'new_df_copy': st.session_state.new_df_copy,
                            'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})
    else:
        # Fehlermeldung, wenn 'new_df_copy' fehlt oder kein gültiger DataFrame ist
        st.error("new_df_copy fehlt oder ist kein gültiger DataFrame.")


# Funktion zum Entfernen von Einträgen eines Stakeholders aus 'new_df_copy' und 'stakeholder_punkte_filtered'
def remove_stakeholder_entries(stakeholder_name):
    # Überprüfen, ob 'new_df_copy' im Sitzungszustand existiert
    if 'new_df_copy' in st.session_state:
        # Entferne alle Einträge in 'new_df_copy', die dem angegebenen Stakeholder zugeordnet sind
        st.session_state.new_df_copy = st.session_state.new_df_copy[
            ~st.session_state.new_df_copy['Stakeholder'].str.contains(stakeholder_name, case=False, na=False)
        ]
        # Speichere den aktualisierten Zustand
        save_session_state({'new_df_copy': st.session_state.new_df_copy})

    # Überprüfen, ob 'stakeholder_punkte_filtered' im Sitzungszustand existiert
    if 'stakeholder_punkte_filtered' in st.session_state:
        # Entferne alle Einträge in 'stakeholder_punkte_filtered', die dem angegebenen Stakeholder zugeordnet sind
        st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_filtered[
            ~st.session_state.stakeholder_punkte_filtered['Stakeholder'].str.contains(stakeholder_name, case=False, na=False)
        ]
        # Speichere den aktualisierten Zustand
        save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

    # Überprüfen, ob 'stakeholder_punkte_df' im Sitzungszustand existiert
    if 'stakeholder_punkte_df' in st.session_state:
        # Entferne alle Einträge in 'stakeholder_punkte_df', die dem angegebenen Stakeholder zugeordnet sind
        st.session_state.stakeholder_punkte_df = st.session_state.stakeholder_punkte_df[
            ~st.session_state.stakeholder_punkte_df['Stakeholder'].str.contains(stakeholder_name, case=False, na=False)
        ]
        # Speichere den aktualisierten Zustand
        save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})


#---------------------------------- Funktion zum Hinzufügen eines Stakeholders ----------------------------------#

# Funktion zum Hinzufügen eines Stakeholders und Sicherstellen, dass keine alten Daten erhalten bleiben
def re_add_stakeholder(stakeholder_name, new_data):
    # Zuerst alle bestehenden Daten für diesen Stakeholder entfernen
    remove_stakeholder_entries(stakeholder_name)
    
    # Neue Daten für 'new_df_copy' hinzufügen oder erstellen
    if 'new_df_copy' in st.session_state:
        st.session_state.new_df_copy = pd.concat([st.session_state.new_df_copy, new_data], ignore_index=True)  # Füge die neuen Daten hinzu
    else:
        st.session_state.new_df_copy = new_data.copy()  # Erstelle 'new_df_copy', wenn es noch nicht existiert

    # Neue Daten für 'stakeholder_punkte_filtered' hinzufügen oder erstellen
    if 'stakeholder_punkte_filtered' in st.session_state:
        st.session_state.stakeholder_punkte_filtered = pd.concat([st.session_state.stakeholder_punkte_filtered, new_data], ignore_index=True)
    else:
        st.session_state.stakeholder_punkte_filtered = new_data.copy()

    # Den aktualisierten Sitzungszustand speichern
    save_session_state({'new_df_copy': st.session_state.new_df_copy,
                        'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})


#---------------------------------- Funktion zum Entfernen ungültiger Stakeholder ----------------------------------#

# Funktion zum Entfernen ungültiger Stakeholder aus der Seitenleiste und aus dem Sitzungszustand
def remove_invalid_stakeholders():
    # Überprüfen, ob 'Einbezogene_Stakeholder' und 'ranking_table' im Sitzungszustand existieren
    if 'Einbezogene_Stakeholder' in st.session_state and 'ranking_table' in st.session_state:
        # Bestimmen der gültigen Stakeholder, basierend auf der 'ranking_table' und den 'Einbezogene_Stakeholder'
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.Einbezogene_Stakeholder))
        
        # Filtere die 'sidebar_companies', um nur gültige Stakeholder zu behalten
        removed_stakeholders = [item for item in st.session_state.sidebar_companies if item not in valid_stakeholders]
        st.session_state.sidebar_companies = [item for item in st.session_state.sidebar_companies if item in valid_stakeholders]
        save_session_state({'sidebar_companies': st.session_state.sidebar_companies})  # Speichere den aktualisierten Zustand der Seitenleiste
        
        # Entferne die Einträge der entfernten Stakeholder aus 'new_df_copy' und 'stakeholder_punkte_filtered'
        for stakeholder in removed_stakeholders:
            remove_stakeholder_entries(stakeholder)

        # Aktualisiere die neue Datenkopie
        refresh_new_df_copy()


#---------------------------------- Aktualisierung der neuen Datenkopie ----------------------------------#

# Aktualisiere 'new_df_copy' durch Status-Update und Anpassung der Stakeholder-Punkte
def refresh_new_df_copy():
    if 'new_df_copy' in st.session_state and 'stakeholder_punkte_filtered' in st.session_state:
        # Aktualisiere den Status in 'new_df_copy'
        st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
        
        # Passen Sie die Stakeholder-Punkte in 'stakeholder_punkte_filtered' basierend auf den neuen Daten an
        st.session_state.stakeholder_punkte_filtered = adjust_stakeholder_punkte_filtered(
            st.session_state.new_df_copy,
            st.session_state.stakeholder_punkte_filtered
        )
        
        # Speichern des aktualisierten Sitzungszustands
        save_session_state({'new_df_copy': st.session_state.new_df_copy,
                            'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})


#---------------------------------- Excel-Datei hochladen und Daten verarbeiten ----------------------------------#

# Funktion zum Hochladen einer Excel-Datei und Verarbeiten der enthaltenen Daten
def excel_upload():
    plazhalter()  # Füge vertikale Abstände im UI ein
    uploaded_file = st.file_uploader("Laden Sie hier die Excel-Dateien der Stakeholder hoch", type=['xlsx'])  # Zeige einen Datei-Uploader für Excel-Dateien an
    
    if uploaded_file:
        df_list = []
        # Iteriere durch die erwarteten Arbeitsblätter in der Excel-Datei
        for sheet_name in ['Themenspezifische ESRS', 'Interne Nachhaltigkeitspunkte', 'Externe Nachhaltigkeitspunkte']:
            try:
                # Lese die relevanten Spalten aus jedem Arbeitsblatt in einen DataFrame
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl', 
                                   usecols=['Thema', 'Unterthema', 'Unter-Unterthema', 'Auswirkungsbezogene Bewertung', 'Finanzbezogene Bewertung'])
                df['Quelle'] = sheet_name  # Füge die Quelle hinzu, um das Arbeitsblatt zu identifizieren
                df_list.append(df)  # Füge den DataFrame zur Liste hinzu
            except ValueError:
                # Zeige eine Nachricht an, wenn das Arbeitsblatt nicht gefunden wird
                st.info(f"Blatt '{sheet_name}' nicht in {uploaded_file.name} gefunden.")
        
        if df_list:
            # Kombiniere die DataFrames aus allen Arbeitsblättern
            combined_df = pd.concat(df_list, ignore_index=True)
            
            # Sicherstellen, dass die 'Stakeholder'-Spalte vorhanden ist, und falls nicht, erstelle sie
            if 'Stakeholder' not in combined_df.columns:
                combined_df['Stakeholder'] = ''  # Erstelle eine leere 'Stakeholder'-Spalte

            # Aggregiere die Rankings basierend auf den kombinierten Daten
            st.session_state.ranking_df = aggregate_rankings(combined_df)
            save_session_state({'ranking_df': st.session_state.ranking_df})
            plazhalter()

            # Erstelle einen Expander für die Vorschau der hochgeladenen Daten
            with st.expander("Vorschau der hochgeladenen Daten"):
                # Zeige die aggregierten Daten in einer Vorschau an
                response = display_aggrid(st.session_state.ranking_df)
                st.session_state.grid_response = response
                save_session_state({'grid_response': st.session_state.grid_response})

            # Initialisiere 'Einbezogene_Stakeholder', falls es noch nicht existiert
            if 'Einbezogene_Stakeholder' not in st.session_state:
                st.session_state.Einbezogene_Stakeholder = []

            # Bestimme die gültigen Stakeholder und biete eine Auswahl an
            valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.Einbezogene_Stakeholder))
            options = [opt for opt in valid_stakeholders if opt not in st.session_state.sidebar_companies]

            # Selectbox zur Auswahl eines Stakeholders
            selected_option = st.selectbox('Wählen Sie den zugehörigen Stakeholder aus:', options)
            st.session_state.selected_option = selected_option
            save_session_state({'selected_option': st.session_state.selected_option})

            # Button zum Übernehmen der Punkte
            if st.button('Punkte übernehmen'):
                if st.session_state.selected_option:
                    # Füge die ausgewählte Option zur Seitenleiste hinzu
                    st.session_state.sidebar_companies.append(st.session_state.selected_option)
                    save_session_state({'sidebar_companies': st.session_state.sidebar_companies})

                    # Relevante Spalten definieren und die Daten auf Grundlage der Bewertung filtern
                    relevant_columns = ['Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']
                    new_df = st.session_state.ranking_df[relevant_columns]
                    new_df = new_df[new_df['Stakeholder Gesamtbew'] >= 1]  # Filtere nur relevante Daten
                    
                    new_df['Stakeholder'] = st.session_state.selected_option  # Setze den Stakeholder-Namen

                    # Aktualisiere 'new_df_copy' oder erstelle es, wenn es nicht existiert
                    if 'new_df_copy' not in st.session_state:
                        st.session_state.new_df_copy = new_df.copy()
                    else:
                        # Sicherstellen, dass die Spalte 'Stakeholder' in 'new_df_copy' existiert
                        if 'Stakeholder' not in st.session_state.new_df_copy.columns:
                            st.session_state.new_df_copy['Stakeholder'] = ''

                        # Entferne vorhandene Einträge des ausgewählten Stakeholders
                        st.session_state.new_df_copy = st.session_state.new_df_copy[
                            st.session_state.new_df_copy['Stakeholder'] != st.session_state.selected_option
                        ]
                        # Füge die neuen Daten hinzu
                        st.session_state.new_df_copy = pd.concat([st.session_state.new_df_copy, new_df], ignore_index=True)

                    # Aktualisiere den Status in 'new_df_copy'
                    st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
                    save_session_state({'new_df_copy': st.session_state.new_df_copy})

                    # Falls 'stakeholder_punkte_df' nicht leer ist, führe eine Fusion der Daten durch
                    if not st.session_state.stakeholder_punkte_df.empty:
                        merged_df = pd.merge(
                            st.session_state.stakeholder_punkte_df, new_df, 
                            on=['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle'], how='outer', suffixes=('_x', '_y')
                        )

                        # Füge die Bewertungen zusammen
                        merged_df['Stakeholder Bew Auswirkung'] = merged_df['Stakeholder Bew Auswirkung_x'].add(merged_df['Stakeholder Bew Auswirkung_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Bew Finanzen'] = merged_df['Stakeholder Bew Finanzen_x'].add(merged_df['Stakeholder Bew Finanzen_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Gesamtbew'] = merged_df['Stakeholder Gesamtbew_x'].add(merged_df['Stakeholder Gesamtbew_y'], fill_value=0).astype(int)

                        # Kombiniere und bereinige das 'Stakeholder'-Feld
                        merged_df['Stakeholder'] = merged_df.apply(
                            lambda row: ', '.join(filter(lambda x: pd.notna(x) and x != 'nan', 
                                                        [str(row.get('Stakeholder_x', '')), str(row.get('Stakeholder_y', ''))])), 
                            axis=1
                        )

                        # Entferne überflüssige Spalten
                        merged_df.drop(columns=['Stakeholder Bew Auswirkung_x', 'Stakeholder Bew Auswirkung_y', 'Stakeholder Bew Finanzen_x', 'Stakeholder Bew Finanzen_y', 'Stakeholder Gesamtbew_x', 'Stakeholder Gesamtbew_y', 'Stakeholder_x', 'Stakeholder_y'], inplace=True)
                        st.session_state.stakeholder_punkte_df = merged_df  # Aktualisiere den Haupt-DataFrame
                    else:
                        st.session_state.stakeholder_punkte_df = new_df  # Setze die Daten, falls keine vorherigen Daten vorhanden sind

                    # Sortiere die Stakeholder-Punkte nach Gesamtbewertung und weise Platzierungen zu
                    st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
                    st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
                    save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})

                    # Setze den gefilterten DataFrame
                    st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_df
                    save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

                    st.success("Stakeholder Punkte erfolgreich übernommen")  # Erfolgsmeldung

                    # Setze die hochgeladene Datei zurück und lade die Seite neu
                    st.session_state.uploaded_file = None
                    save_session_state({'uploaded_file': st.session_state.uploaded_file})
                    st.rerun()
                else:
                    if not options:
                        st.info("Punkte können nicht übernommen werden. Bitte fügen Sie den entsprechenden Stakeholder hinzu und/oder nehmen sie diesen explizit in die Bewertung auf.")
                    else:
                        st.success("Stakeholder Punkte erfolgreich übernommen")  # Erfolgsmeldung für erfolgreichen Transfer der Punkte

    # Aktualisiere die Datenkopie, falls vorhanden
    if 'new_df_copy' in st.session_state:
        refresh_new_df_copy()  # Rufe die Funktion zum Aktualisieren der Datenkopie auf


def refresh_session_state():
    # Force save all session states to ensure they are updated
    save_session_state({'new_df_copy': st.session_state.get('new_df_copy', pd.DataFrame())})
    save_session_state({'stakeholder_punkte_filtered': st.session_state.get('stakeholder_punkte_filtered', pd.DataFrame())})
    save_session_state({'stakeholder_punkte_df': st.session_state.get('stakeholder_punkte_df', pd.DataFrame())})

# Funktion zum Verschieben von Stakeholdern von Einbezogene_Stakeholder nach Ausgeschlossene_Stakeholder
def move_stakeholders(selected_stakeholders):
    if selected_stakeholders:
        # Stakeholder aus Einbezogene_Stakeholder entfernen und zu Ausgeschlossene_Stakeholder hinzufügen
        st.session_state.Einbezogene_Stakeholder = [stakeholder for stakeholder in st.session_state.Einbezogene_Stakeholder if stakeholder not in selected_stakeholders]
        st.session_state.Ausgeschlossene_Stakeholder.extend(selected_stakeholders)
        
        # Speichern des aktualisierten Sitzungszustands
        save_session_state({'Einbezogene_Stakeholder': st.session_state.Einbezogene_Stakeholder, 'Ausgeschlossene_Stakeholder': st.session_state.Ausgeschlossene_Stakeholder})
        
        # Erfolgsmeldung anzeigen und die Seite neu laden
        st.success(f"{len(selected_stakeholders)} Stakeholder erfolgreich verschoben!")
        st.rerun()

#---------------------------------- Hauptseite anzeigen ----------------------------------#

# Main function to display the page content
def display_page():
    
    # Update the new data copy and other necessary session data
    refresh_new_df_copy()
    
    # Create two columns for layout
    col1, col2 = st.columns([3, 1.3])
    with col1:
        st.header("Stakeholder-Management")  # Set the main header of the page
    with col2:
        container = st.container(border=True)
        with container:
            display_not_in_sidebar_count()  # Show the count of missing stakeholder evaluations
    
    # Add a description of the page
    st.markdown("""
        Hier können Sie Stakeholder-Bewertungen verwalten und aktualisieren. Laden Sie hierzu die von den Stakeholdern bereitgestellten Excel_Datein hoch und fügen Sie diese zur Bewertung hinzu. Von jeder hochgeladenen Excel wird Ihnen eine Vorschau der bewerteten Punkte angezeigt. Diesen Punkten müssen Sie dann die entsprechenden Stakeholder über die Selectbox zuordnen.
        Im Tab "Übersicht Stakeholderbewertung" können Sie die aggregierten Stakeholder-Bewertungen einsehen.
    """)

    # Create tabs for stakeholder rating selection and ranking
    tab1, tab2 = st.tabs(["Hochladen der Bewertungen", "Übersicht der Bewertung"])
    with tab1:
        excel_upload()  # Allow uploading and processing of Excel files
        display_sidebar_items()  # Show already rated stakeholders in the sidebar

    with tab2:
        stakeholder_punkte()  # Display stakeholder points in a table
    
    refresh_session_state()  # Refresh the session state to ensure all data is up to date