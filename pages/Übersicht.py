import streamlit as st
import altair as alt
import pandas as pd
from pages.Stakeholder_Management import stakeholder_ranking
from pages.Longlist import  bewertung_Uebersicht_Nein,  bewertung_Uebersicht, anzahl_punkte_Longlist, count_top_down_points, count_internal_points, count_stakeholder_points
from pages.Shortlist import Balken_Finanzbezogen_Stakeholder,Balken_Auswirkungsbezogen_Stakeholder, chart_übersicht_allgemein_test_2, Balken_Finanzbezogen, chart_auswirkungsbezogen, chart_finanzbezogen, Balken_Auswirkungsbezogen
from pages.Themenspezifische_ESRS import calculate_percentages, checkboxes_count


# Stellt sicher, dass der 'checkbox_count' in der Session initialisiert ist
if 'checkbox_count' not in st.session_state:
    st.session_state['checkbox_count'] = 0

# Funktion zur Anzeige der Anzahl der Punkte in der Shortlist
def count_shortlist_points():
    if 'filtered_df' in st.session_state:
        count = len(st.session_state.filtered_df)
        st.metric("Anzahl der Punkte in der Shortlist:", count)

# Funktion zur Anzeige der Unternehmen in der Stakeholder-Tabelle
def companies_in_stakeholder_table():
    if 'sidebar_companies' in st.session_state:
        st.write("Folgende Stakeholder wurden in Bewertung miteinbezogen:")
        for item in st.session_state.sidebar_companies:
            st.write(f"- {item}")
    else:
        st.write("Keine Stakeholder in Bewertung aufgenommen")

# Funktion zum Laden einer Seite und Aufruf der 'display_page'-Funktion des Moduls
def load_page(page_module):
    page_function = getattr(page_module, 'display_page', None)
    if callable(page_function):
        page_function()
    else:
        st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")

#------------------- Wesentlichkeitsanalyse --------------------#

# Funktion zur Überprüfung des aktuellen Fortschritts der Wesentlichkeitsanalyse
def aktueller_stand_wesentlichkeitsanalyse():
    completed_count = 0

    # Liste der zu überprüfenden Session-States und ihrer Namen
    session_states_to_check = [
        ('checkbox_state_1', '1. Stakeholder Management'),
        ('checkbox_state_2', '2. Stakeholder Auswahl'),
        ('checkbox_state_3', '3. Themenspezifische ESRS'),
        ('checkbox_state_4', '4. Interne Nachhaltigkeitspunkte'),
        ('checkbox_state_5', '5. Externe Nachhaltigkeitspunkte'),
        ('checkbox_state_6', '6. Bewertung der Longlist'),
        ('checkbox_state_7', '7. Shortlist')
    ]

    # Überprüfung jedes Schrittes der Analyse
    for key, name in session_states_to_check:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(name)  # Zeigt den Namen des Schrittes an
        with col2:
            # Spezielle Logik für Schritt 5 (externe Nachhaltigkeitspunkte)
            if key == 'checkbox_state_5':
                if 'Einbezogene_Stakeholder' in st.session_state and 'sidebar_companies' in st.session_state:
                    if not st.session_state['Einbezogene_Stakeholder'] and not st.session_state['sidebar_companies']:
                        st.write("✘")  # Kein Stakeholder einbezogen
                    elif not st.session_state['Einbezogene_Stakeholder']:
                        st.write("✔")  # Nur externe Stakeholder ausgewählt
                    else:
                        # Anzahl fehlender Stakeholder anzeigen
                        count = len([opt for opt in st.session_state['Einbezogene_Stakeholder'] if opt not in st.session_state['sidebar_companies']])
                        if st.session_state.get(key) == True:
                            completed_count += 1
                            st.write("✔")  # Schritt abgeschlossen
                        else:
                            st.write(f"Es fehlt noch {count} Stakeholder.")  # Fehlende Stakeholder anzeigen
                else:
                    st.write("✘")  # Kein Stakeholder vorhanden

            # Logik für Schritt 3 (themenspezifische ESRS)
            elif key == 'checkbox_state_3':
                if st.session_state.get(key) == True:
                    completed_count += 1
                    st.write("✔")  # Schritt abgeschlossen
                else:
                    if 'checkbox_count' in st.session_state and st.session_state['checkbox_count'] > 0:
                        percentage_missing = calculate_percentages()
                        st.write(f"Es fehlen noch {percentage_missing}%.")  # Prozentsatz der fehlenden Themen anzeigen
                    else:
                        st.write("✘")  # Kein Fortschritt bei den Themen

            # Logik für Schritt 6 (Bewertung der Longlist)
            elif key == 'checkbox_state_6':
                if 'longlist' in st.session_state and not st.session_state['longlist'].empty:
                    if st.session_state.get(key) == True:
                        completed_count += 1
                        st.write("✔")  # Schritt abgeschlossen
                    else:
                        nein_prozent = bewertung_Uebersicht_Nein()
                        st.write(f"Es fehlen noch {nein_prozent}%.")  # Fehlende Prozentanzeige
                else:
                    st.write("✘")  # Longlist ist leer

            # Standardlogik für alle anderen Schritte
            else:
                if st.session_state.get(key) == True:
                    completed_count += 1
                    st.write("✔")  # Schritt abgeschlossen
                else:
                    st.write("✘")  # Schritt nicht abgeschlossen

# Funktion für leere Platzhalter zur Strukturierung des Layouts
def placeholder():
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

#------------------- Seitenanzeige und Tabs --------------------#

# Hauptfunktion zur Anzeige der Seite und der Tabs
def display_page():
    
    # Liste der Session-States, die überprüft werden müssen
    session_states_to_check = [
        'stakeholder_punkte_df', 'filtered_df', 'sidebar_companies', 
        'namen_tabelle', 'ranking_table', 'stakeholder_punkte_filtered',
    ]

    # Überprüfen, ob alle relevanten Session-States leer oder nicht vorhanden sind
    if all(
        key not in st.session_state or 
        (isinstance(st.session_state[key], pd.DataFrame) and st.session_state[key].empty) 
        for key in session_states_to_check
    ):
        st.info("Es wurden noch keine Inhalte hinzugefügt. Starten Sie mit der Wesentlichkeitsanalyse")
        return
    
    # Tabs für die verschiedenen Ansichten
    tab1, tab2, tab3 = st.tabs(["Übersicht", "Allgemeine Graphik", "Spezifische Graphiken"])
    
    #------------------- Tab 1: Übersicht --------------------#
    with tab1:
        col = st.columns((1.6, 2.5, 1), gap='small')
        
        # Linke Spalte: Fortschritt der Wesentlichkeitsanalyse und Punkte anzeigen
        with col[0]:
            container = st.container(border=True)
            with container:
                st.markdown('#### Fortschritt Wesentlichkeitsanalyse')
                aktueller_stand_wesentlichkeitsanalyse()  # Zeigt den Fortschritt der Analyse an
            container_4 = st.container(border=True)
            with container_4:
                checkboxes_count()  # Zählt die ausgewählten Checkboxen
                
            container_5 = st.container(border=True)
            with container_5:
                anzahl_punkte_Longlist()  # Zeigt die Anzahl der Punkte in der Longlist
                bewertung_Uebersicht()  # Übersicht der Bewertung    
            container_3 = st.container(border=True)
            with container_3:
                count_shortlist_points()  # Zeigt die Anzahl der Shortlist-Punkte an

        # Mittlere Spalte: Eigene Bewertung und Darstellung der Top 30 Punkte
        with col[1]:        
            container_1 = st.container(border=True)
            with container_1:
                st.header("Eigene Bewertung")
                
                on = st.toggle ("Änderung der Darstellung", True)
                if on:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Top 30 der auswirkungsbezogenen Punkte**")
                    Balken_Auswirkungsbezogen()  # Balkendiagramm für auswirkungsbezogene Punkte
                else:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Top 30 der finanzbezogenen Punkte**")
                    Balken_Finanzbezogen()  # Balkendiagramm für finanzbezogene Punkte

            # Stakeholder Bewertung
            container_2 = st.container(border=True)
            with container_2:
                st.header("Stakeholder Bewertung")
                
                on = st.toggle("Änderung der Darstellung.", True)
                if on:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Top 30 der auswirkungsbezogenen Punkte nach Stakeholder**")
                    Balken_Auswirkungsbezogen_Stakeholder()  # Balkendiagramm für Stakeholder-Auswirkungen
                else:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Top 30 finanzbezogenen Punkte nach Stakeholder**")
                    Balken_Finanzbezogen_Stakeholder()  # Balkendiagramm für Stakeholder-Finanzen
                
        # Rechte Spalte: Anzeige der Stakeholder und ihres Rankings
        with col[2]:      
            container_6 = st.container(border=True)
            with container_6:
                st.markdown('#### Stakeholder')
                companies_in_stakeholder_table()  # Zeigt die Stakeholder in der Tabelle

            container_7 = st.container(border=True)
            with container_7:
                st.markdown('#### Stakeholder Ranking')
                stakeholder_ranking()  # Zeigt das Stakeholder-Ranking

    #------------------- Tab 2: Allgemeine Graphik --------------------#
    with tab2:
        st.title("Allgemeine Graphik") 
        st.write("Hier finden Sie eine Graphik, welche alle Informationen zu den bewerteten IROs zusammenfasst")
        st.markdown("---")
        placeholder()  # Platzhalter für das Layout
        chart_übersicht_allgemein_test_2(width=900, height=800)  # Anzeige der allgemeinen Graphik

    #------------------- Tab 3: Spezifische Graphiken --------------------#
    with tab3:
        st.title("Zusätzliche Graphiken")
        st.write("Hier finden Sie zusätzliche Darstellungen der Wesentlichkeitsmatrix")
        chart_auswirkungsbezogen(width=900, height=800)  # Anzeige der auswirkungsbezogenen Graphik
        chart_finanzbezogen(width=900, height=800)  # Anzeige der finanzbezogenen Graphik
