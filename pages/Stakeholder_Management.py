import streamlit as st
import pandas as pd
import pickle
import os
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pyvis.network import Network

# Konstante für den Dateinamen des Sitzungszustands
STATE_FILE = 'session_states.pkl'

# Funktion zum Initialisieren des DataFrame mit leeren Spalten für die Stakeholder-Daten
def initialize_df():
    return pd.DataFrame(columns=[
        "Gruppe", "Bestehende Beziehung", "Auswirkung auf Interessen", "Level des Engagements",
        "Stakeholdergruppe", "Kommunikation", "Art der Betroffenheit", "Zeithorizont"
    ])

# Funktion zum Speichern des aktuellen Sitzungszustands in eine Datei
def save_state():
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(dict(st.session_state), f)

# Initialisierung des Sitzungszustands beim Laden der Seite, falls eine gespeicherte Datei existiert
if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
    with open(STATE_FILE, 'rb') as f:
        loaded_state = pickle.load(f)
        for key, value in loaded_state.items():
            if key not in st.session_state:
                st.session_state[key] = value

# Initialisiere DataFrame, falls es nicht existiert
if 'df' not in st.session_state:
    st.session_state.df = initialize_df()

# Initialisiere Ranking-Tabelle, falls sie nicht existiert
if 'ranking_table' not in st.session_state:
    st.session_state.ranking_table = pd.DataFrame(columns=["Gruppe", "Score", "Ranking"])

# Berechnung des Scores für einen Stakeholder basierend auf verschiedenen Kriterien
def calculate_score(row):
    # Mapping der Kategorien auf numerische Werte für die Berechnung
    engagement_mapping = {'Hoch': 3, 'Mittel': 1.5, 'Niedrig': 0}
    kommunikation_mapping = {'Regelmäßig': 3, 'Gelegentlich': 1.5, 'Nie': 0}
    zeithorizont_mapping = {'Langfristig': 3, 'Mittelfristig': 1.5, 'Kurzfristig': 0}
    auswirkung_mapping = {'Hoch': 3, 'Mittel': 1.5, 'Niedrig': 0}

    # Berechnung des Scores als gewichteter Durchschnitt
    score = (engagement_mapping.get(row['Level des Engagements'], 0) +
             kommunikation_mapping.get(row['Kommunikation'], 0) +
             zeithorizont_mapping.get(row['Zeithorizont'], 0) +
             auswirkung_mapping.get(row['Auswirkung auf Interessen'], 0)) / 12 * 100
    return round(score)

# Funktion zur Festlegung der Knotenfarbe basierend auf dem Score
def get_node_color(score):
    if score <= 33:
        return "red"
    elif score <= 66:
        return "orange"
    return "green"

# Funktion zur Erstellung der Seitenleiste für die Stakeholder-Eingabe
def sidebar():
    # Standardwerte für Formularfelder initialisieren
    keys = [
        ('gruppe', ''), ('bestehende_beziehung', ''), ('auswirkung', ''), ('level_des_engagements', ''), 
        ('stakeholdergruppe', ''), ('kommunikation', ''), ('art_der_betroffenheit', ''), ('zeithorizont', '')
    ]

    # Prüfen, ob die Schlüssel in der Session existieren, andernfalls Standardwerte setzen
    for key, default in keys:
        if key not in st.session_state:
            st.session_state[key] = default

    # Formular für die Eingabe neuer Stakeholder-Daten
    with st.form(key='stakeholder_form', clear_on_submit=True):
        gruppe = st.text_input("Gruppe", value=st.session_state.gruppe)
        bestehende_beziehung = st.selectbox("Bestehende Beziehung", ['', 'Ja', 'Nein'], 
                                            index=['', 'Ja', 'Nein'].index(st.session_state.bestehende_beziehung))
        auswirkung = st.selectbox("Auswirkung auf Interessen", ['', 'Hoch', 'Mittel', 'Niedrig'], 
                                  index=['', 'Hoch', 'Mittel', 'Niedrig'].index(st.session_state.auswirkung))
        level_des_engagements = st.selectbox("Level des Engagements", ['', 'Hoch', 'Mittel', 'Niedrig'], 
                                             index=['', 'Hoch', 'Mittel', 'Niedrig'].index(st.session_state.level_des_engagements))
        stakeholdergruppe = st.selectbox("Stakeholdergruppe", ['', 'Intern', 'Extern'], 
                                         index=['', 'Intern', 'Extern'].index(st.session_state.stakeholdergruppe))
        kommunikation = st.selectbox("Kommunikation", ['', 'Regelmäßig', 'Gelegentlich', 'Nie'], 
                                     index=['', 'Regelmäßig', 'Gelegentlich', 'Nie'].index(st.session_state.kommunikation))
        art_der_betroffenheit = st.selectbox("Art der Betroffenheit", ['', 'Direkt', 'Indirekt', 'Keine'], 
                                             index=['', 'Direkt', 'Indirekt', 'Keine'].index(st.session_state.art_der_betroffenheit))
        zeithorizont = st.selectbox("Zeithorizont", ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'], 
                                    index=['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'].index(st.session_state.zeithorizont))

        # Hinzufügen der Stakeholder-Daten nach dem Klicken auf den Button
        add_row = st.form_submit_button('Hinzufügen')

        # Beim Klicken wird die Funktion zum Hinzufügen eines neuen Stakeholders aufgerufen
        if add_row:
            add_new_row(gruppe, bestehende_beziehung, auswirkung, level_des_engagements, stakeholdergruppe, kommunikation, art_der_betroffenheit, zeithorizont)

    # Rückgabe der Benutzereingaben und des "Hinzufügen"-Buttons
    return gruppe, bestehende_beziehung, auswirkung, level_des_engagements, stakeholdergruppe, kommunikation, art_der_betroffenheit, zeithorizont, add_row

# Funktion zur Anzeige der AgGrid-Tabelle mit Stakeholder-Daten
def display_grid():
    # Erstellen des GridOptionsBuilder-Objekts basierend auf den Daten im DataFrame aus dem Sitzungszustand (st.session_state.df)
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    
    # Konfigurieren der Standardspalten-Eigenschaften:
    # - editable: Spalten können bearbeitet werden
    # - resizable: Spalten sind in der Größe veränderbar
    # - sortable: Spalten können sortiert werden
    # - filterable: Spalten können gefiltert werden
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)

    # Konfigurieren der Grid-Optionen:
    # - domLayout: Automatische Höhenanpassung der Tabelle
    # - enableRowId: Aktiviert die Row-ID, die zur Identifizierung von Zeilen verwendet wird
    # - rowId: Definiert die Zeilen-ID auf Basis des DataFrame-Index
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')

    # Erstellen der Grid-Optionen und zusätzliche Konfiguration der Spalten
    # Die "Score"-Spalte wird aus der Anzeige entfernt
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + [
        col for col in grid_options['columnDefs'] if col['field'] != 'Score'  # "Score"-Spalte ausblenden
    ]

    # Rückgabe der AgGrid-Tabelle mit den konfigurierten Grid-Optionen
    return AgGrid(
        st.session_state.df.reset_index(),  # DataFrame mit zurückgesetztem Index wird angezeigt
        gridOptions=grid_options,
        fit_columns_on_grid_load=True, #  Die Spalten werden bei der Initialisierung automatisch angepasst
        height=300,  # Höhe der Tabelle wird auf 300 Pixel gesetzt
        width='100%', # Breite der Tabelle auf 100% des Container-Bereichs
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Die Tabelle wird aktualisiert, wenn sich das Modell ändert (MODEL_CHANGED)
        allow_unsafe_jscode=True, # Erlaubt die Verwendung von unsicherem JavaScript-Code (erforderlich für einige Konfigurationsoptionen)
        return_mode=DataReturnMode.FILTERED_AND_SORTED,   # Gibt die sortierten und gefilterten Daten zurück
        selection_mode='multiple', # Mehrfachauswahl wird aktiviert, um mehrere Zeilen gleichzeitig auswählen zu können
    )

# Funktion zum Löschen der ausgewählten Zeilen in der Stakeholder-Tabelle
def delete_selected_rows(grid_response):
    # Erhalten der ausgewählten Zeilen aus der AgGrid-Antwort
    selected_rows = grid_response['selected_rows']
    
    # Extrahieren der Index-Werte der ausgewählten Zeilen, um sie zu löschen
    selected_indices = [row['index'] for row in selected_rows]
    
    # Löschen der ausgewählten Zeilen aus dem DataFrame im Sitzungszustand (st.session_state.df)
    st.session_state.df = st.session_state.df.drop(selected_indices).reset_index(drop=True)  # Index wird nach dem Löschen zurückgesetzt

    # Falls die Ranking-Tabelle existiert und nicht leer ist, lösche auch die entsprechenden Zeilen dort
    if 'ranking_table' in st.session_state and not st.session_state.ranking_table.empty:
        # Löschen der gleichen Zeilen aus der Ranking-Tabelle und Index zurücksetzen
        st.session_state.ranking_table = st.session_state.ranking_table.drop(selected_indices).reset_index(drop=True)
    
    # Speichern des aktuellen Sitzungszustands (aktualisierte Daten) in der Datei
    save_state()

    # Streamlit neu laden, um die Änderungen in der Tabelle zu reflektieren
    st.rerun()


# Funktion zum Hinzufügen einer neuen Zeile (neuer Stakeholder)
def add_new_row(gruppe, bestehende_beziehung, auswirkung, level_des_engagements, stakeholdergruppe, kommunikation, art_der_betroffenheit, zeithorizont):
    # Überprüfen, ob die Gruppe bereits in der DataFrame existiert
    if gruppe in st.session_state.df['Gruppe'].values:
        return False  # Gebe False zurück, wenn die Gruppe bereits existiert, nichts wird hinzugefügt
    else:
        # Neue Zeile erstellen
        new_row = pd.DataFrame({
            "Gruppe": [gruppe],
            "Bestehende Beziehung": [bestehende_beziehung],
            "Auswirkung auf Interessen": [auswirkung],
            "Level des Engagements": [level_des_engagements],
            "Stakeholdergruppe": [stakeholdergruppe],
            "Kommunikation": [kommunikation],
            "Art der Betroffenheit": [art_der_betroffenheit],
            "Zeithorizont": [zeithorizont]
        })
        # Die neue Zeile zur DataFrame hinzufügen
        st.session_state.df = pd.concat([new_row, st.session_state.df]).reset_index(drop=True)
        save_state()
        st.rerun()
        return True  # Gebe True zurück, wenn die Gruppe erfolgreich hinzugefügt wurde

# Hauptfunktion zur Anzeige des Stakeholder-Managements
def display_stakeholder_management():
    # Initialisiere das DataFrame (Datenstruktur), wenn es noch nicht vorhanden ist
    if 'df' not in st.session_state:
        st.session_state.df = initialize_df()

    # Initialisiere die Ranking-Tabelle, wenn sie noch nicht vorhanden ist
    if 'ranking_table' not in st.session_state:
        st.session_state.ranking_table = pd.DataFrame(columns=["Gruppe", "Score", "Ranking"])

    # Zeige die Seitenleiste an und lasse den Benutzer Stakeholder-Daten über ein Formular eingeben
    with st.sidebar:
        st.markdown("---")
        # Speichere die Benutzereingaben aus der Seitenleiste in 'inputs'
        inputs = sidebar()

    # Wenn das DataFrame leer ist, zeige eine Info-Nachricht an
    if st.session_state.df.empty:
        st.info("Keine Daten vorhanden.")
    else:
        # Zeige die Tabelle (DataFrame) mit den eingegebenen Stakeholder-Daten an
        grid_response = display_grid()

        # Überprüfe, ob der Benutzer auf den Lösch-Button klickt, und lösche die ausgewählten Zeilen
        if st.button('🗑️ Zeile löschen') and grid_response:
            delete_selected_rows(grid_response)

    # Überprüfe, ob der Benutzer neue Stakeholder-Daten hinzufügt (letztes Element in 'inputs' ist der "Hinzufügen"-Button)
    if inputs[-1]:  # 'add_row' ist das letzte Element im Rückgabewert von 'sidebar()'
        # Versuche, die neuen Daten als neue Zeile hinzuzufügen, und überprüfe, ob die Gruppe bereits existiert
        success = add_new_row(*inputs[:-1])
        
        # Wenn die Gruppe bereits existiert, zeige eine Warnung an, die nach 4 Sekunden verschwindet
        if success is False:
            warning_placeholder = st.empty()  # Platzhalter für die Warnung erstellen
            warning_placeholder.warning(f'Die Gruppe "{inputs[0]}" existiert bereits. Ein neuer Eintrag wurde nicht hinzugefügt.')
            time.sleep(4)  # 4 Sekunden warten
            warning_placeholder.empty()  # Die Warnung entfernen

# Funktion zur Berechnung und Anzeige des Rankings basierend auf dem Score
def stakeholder_ranking():
    # Überprüfe, ob das DataFrame nicht leer ist (es müssen Daten vorhanden sein)
    if not st.session_state.df.empty:
        # Berechne den Score für jeden Stakeholder basierend auf den Eingabedaten
        st.session_state.df['Score'] = st.session_state.df.apply(calculate_score, axis=1)
        
        # Erstelle eine Kopie der Gruppen und ihrer Scores und berechne das Ranking
        score_table = st.session_state.df[['Gruppe', 'Score']].copy()
        score_table['Ranking'] = score_table['Score'].rank(ascending=False, method='min').astype(int)  # Ranking in absteigender Reihenfolge
        
        # Sortiere die Tabelle nach dem Ranking und setze die Indexwerte zurück
        score_table = score_table.sort_values(by='Ranking').reset_index(drop=True)
        
        # Speichere die Ranking-Tabelle im Sitzungszustand
        st.session_state['ranking_table'] = score_table
        
        # Speichere den aktuellen Sitzungszustand in einer Datei
        save_state()

        # Zeige die Ranking-Tabelle im Streamlit-Interface als DataFrame an
        st.dataframe(
            score_table[['Ranking', 'Gruppe', 'Score']],  # Zeige nur diese Spalten an
            column_config={
                "Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")  # Konfiguriere den Score als Fortschrittsbalken
            },
            hide_index=True,  # Verstecke den Index
            width=800  # Setze die Breite der Tabelle
        )
    else:
        # Wenn keine Daten vorhanden sind, zeige eine Info-Nachricht an
        st.write("Keine Stakeholder-Daten vorhanden.")


# Funktion zur Erstellung und Anzeige des Netzwerkdiagramms der Stakeholder
def stakeholder_network():
    # Initialisiere das Netzwerkdiagramm
    net = Network(height="500px", width="100%", bgcolor="white", font_color="black", notebook=True, directed=False)

    # Füge das zentrale Unternehmen als Knoten hinzu
    net.add_node("Mein Unternehmen", color="black", label="Mein Unternehmen", title="Mein Unternehmen", fixed=True, x=220, y=360)

    # Füge alle Stakeholder aus der Ranking-Tabelle zum Netzwerk hinzu
    if 'ranking_table' in st.session_state:
        for _, row in st.session_state['ranking_table'].iterrows():
            size = row['Score'] / 100 * 10 + 15
            color = get_node_color(row['Score'])

            # Füge die Knoten für die Stakeholder hinzu
            net.add_node(row['Gruppe'], color=color, label=row['Gruppe'], title=row['Gruppe'], size=size)

            # Verbinde das Unternehmen mit den Stakeholdern
            net.add_edge("Mein Unternehmen", row['Gruppe'])

    # Physikalische Einstellungen für das Netzwerk festlegen
    net.repulsion(node_distance=100, central_gravity=0.3, spring_length=200, spring_strength=0.05, damping=0.09)

    # Speichere und zeige das Netzwerkdiagramm in Streamlit an
    net.save_graph("network.html")
    st.components.v1.html(open("network.html", "r").read(), height=600)

# Funktion zur Überprüfung, ob das Stakeholder-Management abgeschlossen ist
def check_abgeschlossen_stakeholder_management():
    if 'checkbox_state_1' not in st.session_state:
        st.session_state['checkbox_state_1'] = False

    # Checkbox zum Markieren des abgeschlossenen Stakeholder-Managements
    st.session_state['checkbox_state_1'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_1'])
    save_state()

# Hauptfunktion zur Anzeige der Stakeholder-Management-Seite
def display_page():
    
    col1, col2 = st.columns([7, 1])
    with col1:
        st.header("Stakeholder-Management")
    with col2:
        container = st.container()
        with container:
            check_abgeschlossen_stakeholder_management()
    
    st.markdown("""
        Hier können Sie ihre Stakeholder effektiv verwalten und analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.          
    """)
    
    # Zwei Tabs für die Übersicht und das Ranking & Netzwerkdiagramm
    tab1, tab2 = st.tabs(["Stakeholder Übersicht", "Stakeholder Ranking & Netzwerkdiagramm"])

    with tab1:
        display_stakeholder_management()

    with tab2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Ranking")
            stakeholder_ranking()
        with col2:
            st.subheader("Netzwerkdiagramm")
            stakeholder_network()
