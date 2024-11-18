import streamlit as st
import pickle

# Konstante für den Dateinamen des Sitzungszustands (wo die Daten gespeichert werden)
STATE_FILE = 'SessionStates.pkl'

# Funktion zum Speichern des aktuellen Sitzungszustands in einer Datei
def save_state():
    # Öffnen der Datei im Schreibmodus und Speichern des Session-States
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(dict(st.session_state), f)

# Funktion zur Initialisierung des Session-States
def initialize_session_state():
    # Überprüfen, ob 'ranking_table' im Session-State existiert und ob sie leer ist
    if 'ranking_table' not in st.session_state or st.session_state['ranking_table'].empty:
        st.info("Noch keine Stakeholder hinzugefügt.")
        return False
    
    # Wenn 'Ausgeschlossene_Stakeholder' noch nicht existiert, wird sie initialisiert
    if 'Ausgeschlossene_Stakeholder' not in st.session_state:
        st.session_state['Ausgeschlossene_Stakeholder'] = st.session_state['ranking_table']['Gruppe'].tolist()
    
    # Wenn 'Einbezogene_Stakeholder' noch nicht existiert, wird sie als leere Liste initialisiert
    if 'Einbezogene_Stakeholder' not in st.session_state:
        st.session_state['Einbezogene_Stakeholder'] = []

    # Initialisierung des Checkbox-Zustands, falls nicht vorhanden
    if 'checkbox_state_2' not in st.session_state:
        st.session_state['checkbox_state_2'] = False
    
    # Aktualisierung der Liste der ausgeschlossenen Stakeholder (falls neue hinzugekommen sind)
    update_ausgeschlossene_Stakeholder()

    return True

# Funktion zum Bereinigen der Tabellen (Entfernen ungültiger Einträge)
def clean_up_tables():
    # Nur gültige Gruppen, die in der 'ranking_table' vorhanden sind, werden beibehalten
    valid_groups = set(st.session_state['ranking_table']['Gruppe'].tolist())
    
    # Entfernen ungültiger Einträge aus 'Ausgeschlossene_Stakeholder'
    st.session_state.Ausgeschlossene_Stakeholder = [item for item in st.session_state.get('Ausgeschlossene_Stakeholder', []) if item in valid_groups]
    
    # Entfernen ungültiger Einträge aus 'Einbezogene_Stakeholder'
    st.session_state.Einbezogene_Stakeholder = [item for item in st.session_state.get('Einbezogene_Stakeholder', []) if item in valid_groups]

# Funktion zum Aktualisieren der Liste der ausgeschlossenen Stakeholder
def update_ausgeschlossene_Stakeholder():
    # Liste der aktuellen Gruppen in der 'ranking_table'
    current_ranking = st.session_state['ranking_table']['Gruppe'].tolist()
    
    # Hinzufügen neuer Gruppen zu 'Ausgeschlossene_Stakeholder', die weder in 'Ausgeschlossene_Stakeholder' noch in 'Einbezogene_Stakeholder' sind
    new_items = [item for item in current_ranking if item not in st.session_state.Ausgeschlossene_Stakeholder and item not in st.session_state.Einbezogene_Stakeholder]
    st.session_state.Ausgeschlossene_Stakeholder.extend(new_items)

# Funktion zur Anzeige der nicht in die Bewertung aufgenommenen Stakeholder
def display_not_in_evaluation():
    st.write("**Nicht in Bewertung aufgenommene Stakeholder:**")
    # Kopieren der 'ranking_table' aus dem Session-State
    ranking_table = st.session_state['ranking_table'].copy()
    
    # Überprüfen, ob die Tabelle eine 'Score'-Spalte enthält
    if 'Score' in ranking_table.columns:
        # Entfernen der Prozentanzeige (falls vorhanden) für die 'Score'-Spalte
        ranking_table['Score'] = ranking_table['Score'].apply(lambda x: x)
        
        # Filtern der Stakeholder, die in 'Ausgeschlossene_Stakeholder' sind (nicht in die Bewertung aufgenommen)
        not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.Ausgeschlossene_Stakeholder)]
        
        # Anzeige der Tabelle mit 'Ranking', 'Gruppe' und 'Score' (mit einer Fortschrittsanzeige für den Score)
        st.dataframe(not_in_evaluation[['Ranking', 'Gruppe', 'Score']],
                     column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, 
                     hide_index=True,
                     width=800)
    else:
        # Falls keine 'Score'-Spalte vorhanden ist, nur 'Ranking' und 'Gruppe' anzeigen
        not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.Ausgeschlossene_Stakeholder)]
        st.dataframe(not_in_evaluation[['Ranking', 'Gruppe']],
                     hide_index=True,
                     width=800)

# Funktion zur Anzeige der in die Bewertung aufgenommenen Stakeholder
def display_in_evaluation():
    st.write("**In Bewertung aufgenommene Stakeholder:**")
    
    # Überprüfen, ob es Stakeholder in 'Einbezogene_Stakeholder' gibt
    if st.session_state.Einbezogene_Stakeholder:
        # Auswahl der Stakeholder aus der 'ranking_table', die in 'Einbezogene_Stakeholder' sind
        table_right_df = st.session_state['ranking_table'][st.session_state['ranking_table']['Gruppe'].isin(st.session_state.Einbezogene_Stakeholder)]
        
        # Überprüfen, ob die Tabelle eine 'Score'-Spalte enthält
        if 'Score' in table_right_df.columns:
            # Entfernen der Prozentanzeige für die 'Score'-Spalte
            table_right_df['Score'] = table_right_df['Score'].apply(lambda x: x)
            
            # Anzeige der Tabelle mit 'Ranking', 'Gruppe' und 'Score' (mit Fortschrittsanzeige)
            st.dataframe(table_right_df[['Ranking', 'Gruppe', 'Score']],
                         column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, 
                         hide_index=True,
                         width=800)
        else:
            # Falls keine 'Score'-Spalte vorhanden ist, nur 'Ranking' und 'Gruppe' anzeigen
            st.dataframe(table_right_df[['Ranking', 'Gruppe']],
                         hide_index=True,
                         width=800)
    else:
        # Nachricht anzeigen, wenn noch keine Stakeholder zur Bewertung hinzugefügt wurden
        st.info("Es sind noch keine Inhalte verfügbar. Bitte fügen Sie zuerst Inhalte hinzu.")

# Funktion zum Hinzufügen von Stakeholdern zu 'Einbezogene_Stakeholder'
def add_to_einbezogene_stakeholder(selected_items):
    for item in selected_items:
        # Entfernen des Stakeholders aus 'Ausgeschlossene_Stakeholder' und Hinzufügen zu 'Einbezogene_Stakeholder'
        if item in st.session_state.Ausgeschlossene_Stakeholder:
            st.session_state.Einbezogene_Stakeholder.append(item)
            st.session_state.Ausgeschlossene_Stakeholder.remove(item)

# Funktion zum Entfernen von Stakeholdern aus 'Einbezogene_Stakeholder'
def remove_from_einbezogene_stakeholder(selected_items):
    for item in selected_items:
        # Entfernen des Stakeholders aus 'Einbezogene_Stakeholder' und Hinzufügen zurück zu 'Ausgeschlossene_Stakeholder'
        if item in st.session_state.Einbezogene_Stakeholder:
            st.session_state.Einbezogene_Stakeholder.remove(item)
            st.session_state.Ausgeschlossene_Stakeholder.append(item)

# Funktion zur Auswahl von Stakeholdern und Verschiebung nach 'Einbezogene_Stakeholder'
def add_button_selection():
    # Multiselect-Widget für 'Ausgeschlossene_Stakeholder', um Stakeholder auszuwählen
    selected_table1 = st.multiselect(
        "Wählen Sie Stakeholder zum Hinzufügen aus:",
        st.session_state.Ausgeschlossene_Stakeholder,
        key="select_table1"
    )
    # Button zum Verschieben der ausgewählten Stakeholder nach 'Einbezogene_Stakeholder'
    if st.button("Hinzufügen >>>"):
        add_to_einbezogene_stakeholder(selected_table1)
        st.rerun()  # Neuladen der Seite, um die Änderungen anzuzeigen

# Funktion zur Auswahl von Stakeholdern und Verschiebung zurück zu 'Ausgeschlossene_Stakeholder'
def remove_button_selection():
    # Überprüfen, ob Inhalte in 'Einbezogene_Stakeholder' vorhanden sind
    if st.session_state.Einbezogene_Stakeholder:
        # Multiselect-Widget für 'Einbezogene_Stakeholder', um Stakeholder auszuwählen
        selected_table2 = st.multiselect(
            "Wählen Sie Stakeholder zum Entfernen aus:",
            st.session_state.Einbezogene_Stakeholder,
            key="select_table2"
        )
        # Button zum Verschieben der ausgewählten Stakeholder zurück zu 'Ausgeschlossene_Stakeholder'
        if st.button("<<< Entfernen"):
            remove_from_einbezogene_stakeholder(selected_table2)
            st.rerun()  # Neuladen der Seite, um die Änderungen anzuzeigen

# Funktion zur Überprüfung und Anzeige der Checkbox für "Abgeschlossen"
def check_abgeschlossen_stakeholder_auswahl():
    # Initialisierung des Checkbox-Zustands, falls noch nicht vorhanden
    if 'checkbox_state_2' not in st.session_state:
        st.session_state['checkbox_state_2'] = False
    
    # Anzeige der Checkbox und Speichern des Zustands
    st.session_state['checkbox_state_2'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_2'])

# Funktion, um Platzhalter für das Layout hinzuzufügen
def placeholder():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

# Hauptfunktion zur Anzeige der Seite
def display_page():
    
    # Erstellung von zwei Spalten für das Layout der Seite
    col1, col2 = st.columns([7, 1])
    
    # Linke Spalte: Header der Seite
    with col1:
        st.header("Stakeholder Auswahl")
    
    # Rechte Spalte: Checkbox zur Auswahl "Abgeschlossen"
    with col2:
        container = st.container(border=False)
        with container:
            check_abgeschlossen_stakeholder_auswahl()
    
    # Einleitender Text zur Erklärung der Funktionalität der Seite
    st.write("Wählen Sie die Stakeholder aus, die Sie in die Bewertung aufnehmen möchten. In der linken Tabelle befinden sich Stakeholder, die nicht in die Bewertung aufgenommen sind. In der rechten Tabelle befinden sich Stakeholder, die in die Bewertung aufgenommen sind. Verschieben Sie die Stakeholder über die Multiselect-Elemente und die Schaltflächen zwischen den Tabellen, um Stakeholder einzubeziehen oder auszuschließen.")
    
    # Platzhalter für Layout-Abstand
    placeholder()

    # Initialisierung des Session-States und Überprüfung, ob Stakeholder vorhanden sind
    if not initialize_session_state():
        return

    # Erstellung von zwei Spalten für die Tabellenanzeige
    col1, col2 = st.columns([1, 1], gap='medium')

    # Linke Spalte: Anzeige der Stakeholder, die nicht in die Bewertung aufgenommen sind
    with col1:
        container_left = st.container(border=True)
        with container_left:
            st.write(" ")
            st.write(" ")
            # Anzeige der nicht bewerteten Stakeholder und Auswahl zum Hinzufügen
            display_not_in_evaluation()
            placeholder()
            add_button_selection()

    # Rechte Spalte: Anzeige der Stakeholder, die in die Bewertung aufgenommen sind
    with col2:
        container_right = st.container(border=True)
        with container_right:
            st.write(" ")
            st.write(" ")
            # Anzeige der bewerteten Stakeholder und Auswahl zum Entfernen
            display_in_evaluation()
            placeholder()
            # Die Schaltfläche zum Entfernen nur anzeigen, wenn Inhalte in der Liste vorhanden sind
            if st.session_state.Einbezogene_Stakeholder:
                remove_button_selection()

    # Bereinigung der Tabellen vor dem Speichern des Zustands
    clean_up_tables()
    save_state()
