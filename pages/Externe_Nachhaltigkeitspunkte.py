import streamlit as st  
import pandas as pd  
import pickle  
import os  
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode 

#---------------------------------- Sitzungszustand-Management ----------------------------------#

# Konstante für die Pickl, in dem die session_states gespeichert werden
STATE_FILE = 'a.pkl'

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


# Initialisiere die Variable 'stakeholder_punkte_filtered' im Sitzungszustand, falls sie noch nicht existiert
if 'stakeholder_punkte_filtered' not in st.session_state:
    st.session_state.stakeholder_punkte_filtered = []

# Initialisiere die Tabelle 'table2' im Sitzungszustand, falls sie noch nicht existiert
if 'table2' not in st.session_state:
    st.session_state.table2 = []

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

# Funktion zur Anpassung der Werte und Stakeholder-Namen in 'stakeholder_punkte_filtered' basierend auf 'new_df_copy' für nicht einbezogene Stakeholder
def adjust_stakeholder_punkte_filtered(new_df_copy, stakeholder_punkte_filtered):
    for idx, row in new_df_copy[new_df_copy['Status'] == 'nicht einbezogen'].iterrows():
        stakeholder_name = row['Stakeholder']  # Extrahiere den Stakeholder-Namen
        thema = row['Thema']  # Extrahiere das Thema
        unterthema = row['Unterthema']  # Extrahiere das Unterthema
        unter_unterthema = row['Unter-Unterthema']  # Extrahiere das Unter-Unterthema

        # Finde übereinstimmende Einträge in 'stakeholder_punkte_filtered'
        matches = stakeholder_punkte_filtered[
            (stakeholder_punkte_filtered['Stakeholder'].str.contains(stakeholder_name)) &
            (stakeholder_punkte_filtered['Thema'] == thema) &
            (stakeholder_punkte_filtered['Unterthema'] == unterthema) &
            (stakeholder_punkte_filtered['Unter-Unterthema'] == unter_unterthema)
        ]
        
        # Aktualisiere die Bewertungen für die gefundenen Übereinstimmungen
        for match_idx, match_row in matches.iterrows():
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Auswirkung'] -= row['Stakeholder Bew Auswirkung']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Bew Finanzen'] -= row['Stakeholder Bew Finanzen']
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder Gesamtbew'] -= row['Stakeholder Gesamtbew']
            
            # Aktualisiere den Stakeholder-Namen, indem der aktuelle Name entfernt wird
            updated_stakeholders = match_row['Stakeholder'].replace(stakeholder_name, '').replace(',,', ',').strip(', ')
            stakeholder_punkte_filtered.at[match_idx, 'Stakeholder'] = updated_stakeholders

    return stakeholder_punkte_filtered  # Gib die angepasste DataFrame zurück


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

# Funktion zur Filterung von Stakeholdern basierend auf ihrer Gültigkeit, sodass nur Stakeholder verwendet werden, die in im Stakeholder-Managemnt (ranking_table) und in der AUswahl (table2) enthalten sind
def filter_stakeholders():
    # Überprüfe, ob 'ranking_table' und 'table2' im Sitzungszustand vorhanden sind
    if 'ranking_table' not in st.session_state or 'table2' not in st.session_state:
        return []

    # Erstelle eine Menge gültiger Stakeholder-Gruppen basierend auf der 'ranking_table'
    valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist())
    
    # Filtere 'table2', um nur gültige Stakeholder-Gruppen zu behalten
    filtered_table2 = [item for item in st.session_state.table2 if item in valid_stakeholders]

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
    # Check if 'stakeholder_punkte_filtered' is in session state
    if 'stakeholder_punkte_filtered' in st.session_state:
        # Check if 'Stakeholder' column exists
        if 'Stakeholder' in st.session_state.stakeholder_punkte_filtered.columns:
            # Remove rows where 'Stakeholder' column is empty or just spaces
            st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_filtered[
                st.session_state.stakeholder_punkte_filtered['Stakeholder'].str.strip() != ''
            ]
            
            # Save updated state
            save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})
            
            # Ensure it's a DataFrame and not empty
            if isinstance(st.session_state.stakeholder_punkte_filtered, pd.DataFrame) and not st.session_state.stakeholder_punkte_filtered.empty:
                response = display_aggrid(st.session_state.stakeholder_punkte_filtered)
                st.session_state.grid_response = response
                save_session_state({'grid_response': st.session_state.grid_response})
            else:
                st.info("No stakeholder data available to display.")
        else:
            st.error("The 'Stakeholder' column is missing in the data.")
    else:
        st.info("No stakeholder data available to display.")


#---------------------------------- Seitenleiste und Fortschrittsanzeige ----------------------------------#

# Funktion zur Anzeige von Stakeholdern in der Seitenleiste. DAbei werden nur Stakeholder angezeigt, die in valid_stakeholder enthalten sind
def display_sidebar_items():
    remove_invalid_stakeholders()
    
    with st.sidebar:
        st.markdown("---")
        st.write("**Bereits in Bewertung aufgenommen:**")
        for item in st.session_state.sidebar_companies:
            st.write(item)

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

# Funktion zur Aktualisierung des Status von Stakeholdern in einem DataFrame. Wenn es änderungen in Stakeholder-Managenmte oder Auswahl gibt, wird valid_stakeholder aktualisiert
def update_status(df):
    if 'table2' in st.session_state and 'ranking_table' in st.session_state:
        # Bestimme gültige Stakeholder basierend auf den Tabellen in der Sitzung
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
        # Aktualisiere den Status basierend auf der Zugehörigkeit der Stakeholder zu den gültigen Gruppen
        df['Status'] = df['Stakeholder'].apply(lambda x: 'einbezogen' if x in valid_stakeholders else 'nicht einbezogen')
    else:
        df['Status'] = 'nicht einbezogen'  # Wenn keine gültigen Stakeholder vorhanden sind, setze den Status auf 'nicht einbezogen'
    return df

# Funktion zur Aktualisierung der Kopie der neuen Daten und Anpassung der Stakeholder-Punkte
def refresh_new_df_copy():
    if 'new_df_copy' in st.session_state and 'stakeholder_punkte_filtered' in st.session_state:
        # Aktualisiere den Status der neuen Datenkopie
        st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
        # Passe die gefilterten Stakeholder-Punkte basierend auf der neuen Datenkopie an
        st.session_state.stakeholder_punkte_filtered = adjust_stakeholder_punkte_filtered(
            st.session_state.new_df_copy,
            st.session_state.stakeholder_punkte_filtered
        )
        
        # Speichere den aktualisierten Zustand
        save_session_state({'new_df_copy': st.session_state.new_df_copy,
                            'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

# Funktion zum Entfernen ungültiger Stakeholder aus der Seitenleiste
def remove_invalid_stakeholders():
    if 'table2' in st.session_state and 'ranking_table' in st.session_state:
        # Bestimme gültige Stakeholder
        valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
        # Filtere die Seitenleisten-Unternehmen, um nur gültige Stakeholder beizubehalten
        st.session_state.sidebar_companies = [item for item in st.session_state.sidebar_companies if item in valid_stakeholders]
        # Speichere den aktualisierten Zustand
        save_session_state({'sidebar_companies': st.session_state.sidebar_companies})
        # Aktualisiere die neue Datenkopie
        refresh_new_df_copy()

#---------------------------------- Excel-Datei hochladen und Daten verarbeiten ----------------------------------#

# Funktion zum Hochladen einer Excel-Datei und Verarbeiten der enthaltenen Daten
def excel_upload():
    plazhalter()
    uploaded_file = st.file_uploader("Laden Sie hier die Excel-Dateien der Stakeholder hoch", type=['xlsx'])  # Zeige einen Datei-Uploader für Excel-Dateien an
    
    if uploaded_file:
        df_list = []
        # Iteriere durch die erwarteten Arbeitsblätter in der Excel-Datei
        for sheet_name in ['Top-Down', 'Intern', 'Extern']:
            try:
                # Lese die relevanten Spalten aus jedem Arbeitsblatt in einen DataFrame
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl', usecols=['Thema', 'Unterthema', 'Unter-Unterthema', 'Auswirkungsbezogene Bewertung', 'Finanzbezogene Bewertung'])
                df['Quelle'] = sheet_name  # Füge die Quelle hinzu, um das Arbeitsblatt zu identifizieren
                df_list.append(df)  # Füge den DataFrame zur Liste hinzu
            except ValueError:
                st.info(f"Blatt '{sheet_name}' nicht in {uploaded_file.name} gefunden.")  # Zeige eine Nachricht an, wenn das Arbeitsblatt nicht gefunden wird
        
        if df_list:
            # Kombiniere die DataFrames aus allen Arbeitsblättern
            combined_df = pd.concat(df_list, ignore_index=True)
            # Aggregiere die Rankings basierend auf den kombinierten Daten
            st.session_state.ranking_df = aggregate_rankings(combined_df)
            # Speichere den aggregierten Zustand
            save_session_state({'ranking_df': st.session_state.ranking_df})
            plazhalter()
            
            # Erstelle einen Expander für die Vorschau der hochgeladenen Daten
            with st.expander("Vorschau der hochgeladenen Daten"):
                # Zeige die aggregierten Daten in einer Vorschau an
                response = display_aggrid(st.session_state.ranking_df)
                st.session_state.grid_response = response
                save_session_state({'grid_response': st.session_state.grid_response})

            if 'table2' not in st.session_state:
                st.session_state.table2 = []

            # Bestimme die gültigen Stakeholder und biete eine Auswahl an
            valid_stakeholders = set(st.session_state.ranking_table['Gruppe'].tolist()).intersection(set(st.session_state.table2))
            options = [opt for opt in valid_stakeholders if opt not in st.session_state.sidebar_companies]

            selected_option = st.selectbox('Wählen Sie den zugehörigen Stakeholder aus:', options)
            st.session_state.selected_option = selected_option
            save_session_state({'selected_option': st.session_state.selected_option})

            if st.button('Punkte übernehmen'):
                if st.session_state.selected_option:
                    # Füge die ausgewählte Option zur Seitenleiste hinzu
                    st.session_state.sidebar_companies.append(st.session_state.selected_option)
                    save_session_state({'sidebar_companies': st.session_state.sidebar_companies})

                    relevant_columns = ['Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung', 'Stakeholder Bew Finanzen', 'Stakeholder Gesamtbew', 'Quelle']
                    new_df = st.session_state.ranking_df[relevant_columns]
                    new_df = new_df[new_df['Stakeholder Gesamtbew'] >= 1]
                    
                    new_df['Stakeholder'] = st.session_state.selected_option

                    if 'new_df_copy' not in st.session_state:
                        st.session_state.new_df_copy = new_df.copy()
                    else:
                        # Entferne vorhandene Einträge des Stakeholders und füge die neuen hinzu
                        st.session_state.new_df_copy = st.session_state.new_df_copy[
                            st.session_state.new_df_copy['Stakeholder'] != st.session_state.selected_option
                        ]
                        st.session_state.new_df_copy = pd.concat([st.session_state.new_df_copy, new_df], ignore_index=True)
                    
                    st.session_state.new_df_copy = update_status(st.session_state.new_df_copy)
                    save_session_state({'new_df_copy': st.session_state.new_df_copy})

                    if not st.session_state.stakeholder_punkte_df.empty:
                        # Führe eine Fusion der DataFrames durch, um die Stakeholder-Bewertungen zu aktualisieren
                        merged_df = pd.merge(
                            st.session_state.stakeholder_punkte_df, new_df, 
                            on=['Thema', 'Unterthema', 'Unter-Unterthema', 'Quelle'], how='outer', suffixes=('_x', '_y')
                        )

                        merged_df['Stakeholder Bew Auswirkung'] = merged_df['Stakeholder Bew Auswirkung_x'].add(merged_df['Stakeholder Bew Auswirkung_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Bew Finanzen'] = merged_df['Stakeholder Bew Finanzen_x'].add(merged_df['Stakeholder Bew Finanzen_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder Gesamtbew'] = merged_df['Stakeholder Gesamtbew_x'].add(merged_df['Stakeholder Gesamtbew_y'], fill_value=0).astype(int)
                        merged_df['Stakeholder'] = merged_df.apply(lambda row: ', '.join(filter(None, [row.get('Stakeholder_x', ''), row.get('Stakeholder_y', '')])), axis=1)
                        merged_df.drop(columns=['Stakeholder Bew Auswirkung_x', 'Stakeholder Bew Auswirkung_y', 'Stakeholder Bew Finanzen_x', 'Stakeholder Bew Finanzen_y', 'Stakeholder Gesamtbew_x', 'Stakeholder Gesamtbew_y', 'Stakeholder_x', 'Stakeholder_y'], inplace=True)
                        st.session_state.stakeholder_punkte_df = merged_df
                    else:
                        st.session_state.stakeholder_punkte_df = new_df

                    # Sortiere die Stakeholder-Punkte nach Gesamtbewertung und weise Platzierungen zu
                    st.session_state.stakeholder_punkte_df.sort_values(by='Stakeholder Gesamtbew', ascending=False, inplace=True)
                    st.session_state.stakeholder_punkte_df['Platzierung'] = st.session_state.stakeholder_punkte_df['Stakeholder Gesamtbew'].rank(method='min', ascending=False).astype(int)
                    save_session_state({'stakeholder_punkte_df': st.session_state.stakeholder_punkte_df})

                    st.session_state.stakeholder_punkte_filtered = st.session_state.stakeholder_punkte_df
                    save_session_state({'stakeholder_punkte_filtered': st.session_state.stakeholder_punkte_filtered})

                    st.success("Stakeholder Punkte erfolgreich übernommen")

                    st.session_state.uploaded_file = None
                    save_session_state({'uploaded_file': st.session_state.uploaded_file})
                    st.experimental_rerun()
                else:
                    if not options:
                        st.info("Punkte können nicht übernommen werden. Bitte fügen Sie den entsprechenden Stakeholder unter hinzu und/oder nehmen sie diesen explizit in die Bewertung auf.")
                    else:
                        st.success("Stakeholder Punkte erfolgreich übernommen")

    # new_df_copy ist ein DataFrame, der alle Inhalte eines jeden Stakeholders speichert, um bei entfernen eines Stakeholders noch die INhlate und dessen Bewertungen
    if 'new_df_copy' in st.session_state:
        refresh_new_df_copy()

#---------------------------------- Hauptseite anzeigen ----------------------------------#

# Funktion zur Anzeige der Hauptseite
def display_page():

    # Aktualisiere die neue Datenkopie und andere notwendige Sitzungsdaten
    refresh_new_df_copy()
    
    # Erstelle zwei Spalten für das Layout
    col1, col2 = st.columns([3, 1.3])
    with col1:
        st.header("Stakeholder-Management")  # Setze den Hauptheader der Seite
    with col2:
        container = st.container(border=True)
        with container:
            display_not_in_sidebar_count()  # Zeige die Anzahl fehlender Stakeholder-Bewertungen an
    
    # Füge eine Beschreibung der Seite hinzu
    st.markdown("""
        Hier können Sie Stakeholder-Bewertungen verwalten und aktualisieren. Laden Sie hierzu die von den Stakeholdern bereitgestellten Excel_Datein hoch und fügen Sie diese zur Bewertung hinzu. Von jeder hochgeladenen Excel wird Ihnen eine Vorschau der bewerteten Punkte angezeigt. Diesen Punkten müssen Sie dann die entsprechenden Stakeholder über die Selectbox zuordnen.
        Im Tab "Übersicht Stakeholderbewertung" können Sie die aggregierten Stakeholder-Bewertungen einsehen.
    """)

    # Erstelle Tabs für die Auswahl und das Ranking der Stakeholderbewertung
    tab1, tab2 = st.tabs(["Hochladen der Bewertungen", "Übersicht der Bewertung"])
    with tab1:
        excel_upload()  # Ermögliche das Hochladen und Verarbeiten von Excel-Dateien
        display_sidebar_items()  # Zeige die bereits bewerteten Stakeholder in der Seitenleiste an

    with tab2:
        stakeholder_punkte()  # Zeige die Stakeholder-Punkte in einer Tabelle an
