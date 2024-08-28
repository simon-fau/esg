import streamlit as st
import altair as alt
import pandas as pd
from pages.Stakeholder_Management import stakeholder_ranking
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import  bewertung_Uebersicht_Nein,  bewertung_Uebersicht, anzahl_punkte_Longlist, count_top_down_points, count_internal_points, count_stakeholder_points
from pages.Shortlist import chart_übersicht_allgemein_test_2, Balken_Finanzbezogen, chart_auswirkungsbezogen, chart_finanzbezogen, Balken_Auswirkungsbezogen
from pages.Themenspezifische_ESRS import calculate_percentages, count_checkboxes

# Ensure 'checkbox_count' is initialized
if 'checkbox_count' not in st.session_state:
    st.session_state['checkbox_count'] = 0

def display_stakeholder_table():
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered

    if not stakeholder_punkte_filtered.empty:
        stakeholder_punkte_filtered.reset_index(inplace=True)
        stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)

        # Ensure "Platzierung" is the first column
        columns = stakeholder_punkte_filtered.columns.tolist()
        if 'Platzierung' in columns:
            columns.insert(0, columns.pop(columns.index('Platzierung')))
        stakeholder_punkte_filtered = stakeholder_punkte_filtered[columns]

        # Remove the "Quelle" column if it exists
        if 'Quelle' in stakeholder_punkte_filtered.columns:
            stakeholder_punkte_filtered = stakeholder_punkte_filtered.drop(columns=['Quelle'])

        # Display the table without checkboxes
        grid_response = display_aggrid(stakeholder_punkte_filtered.drop(columns=['_index']), with_checkboxes=False)

def count_shortlist_points():
    if 'filtered_df' in st.session_state:
        count = len(st.session_state.filtered_df)
        st.metric("Anzahl der Punkte in der Shortlist:", count)

def companies_in_stakeholder_table():
    if 'sidebar_companies' in st.session_state:
        st.write("Folgende Stakeholder wurden in Bewertung miteinbezogen:")
        for item in st.session_state.sidebar_companies:
            st.write(f"- {item}")
    else:
        st.write("Keine Stakeholder in Bewertung aufgenommen")


def load_page(page_module):
                page_function = getattr(page_module, 'display_page', None)
                if callable(page_function):
                    page_function()
                else:
                    st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")


def aktueller_stand_wesentlichkeitsanalyse():
    completed_count = 0

    session_states_to_check = [
        ('checkbox_state_1', '1. Stakeholder Management'),
        ('checkbox_state_2', '2. Stakeholder Auswahl'),
        ('checkbox_state_3', '3. Themenspezifische ESRS'),
        ('checkbox_state_4', '4. Interne Nachhaltigkeitspunkte'),
        ('checkbox_state_5', '5. Externe Nachhaltigkeitspunkte'),
        ('checkbox_state_6', '6. Bewertung der Longlist'),
        ('checkbox_state_7', '7. Shortlist')
    ]

    for key, name in session_states_to_check:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(name)
        with col2:
            if key == 'checkbox_state_5':
                if 'table2' in st.session_state and 'sidebar_items' in st.session_state:
                    if not st.session_state['table2']:
                        st.write("✔")
                    else:
                        count = len([opt for opt in st.session_state['table2'] if opt not in st.session_state['sidebar_items']])
                        if st.session_state.get(key) == True:
                            completed_count += 1
                            st.write("✔")
                        else:
                            st.write(f"Es fehlt noch {count} Stakeholder.")
                else:
                    st.write("✘")
            elif key == 'checkbox_state_3':
                if st.session_state.get(key) == True:
                    completed_count += 1
                    st.write("✔")
                else:
                    if 'checkbox_count' in st.session_state and st.session_state['checkbox_count'] > 0:
                        percentage_missing = calculate_percentages()
                        st.write(f"Es fehlen noch {percentage_missing}%.")
                    else:
                        st.write("✘")  # Zeige ✘, wenn keine Checkbox ausgewählt wurde und checkbox_count leer ist

            elif key == 'checkbox_state_6':
                if 'longlist' in st.session_state and not st.session_state['longlist'].empty:
                    if st.session_state.get(key) == True:
                        completed_count += 1
                        st.write("✔")
                    else:
                        nein_prozent = bewertung_Uebersicht_Nein()
                        st.write(f"Es fehlen noch {nein_prozent}%.")
                else:
                    st.write("✘")  # Zeige ✘, wenn die Longlist leer ist
            else:
                if st.session_state.get(key) == True:
                    completed_count += 1
                    st.write("✔")
                else:
                    st.write("✘")

def display_page():
    
    # Check if all relevant session states are empty
    session_states_to_check = [
        'stakeholder_punkte_df', 'filtered_df', 'sidebar_companies', 
        'namen_tabelle', 'ranking_table', 'stakeholder_punkte_filtered'
    ]
    if all(key not in st.session_state or st.session_state[key].empty for key in session_states_to_check):
        st.info("Es wurden noch keine Inhalte hinzugefügt. Starten Sie mit der Wesentlichkeitsanalyse")
        return
    
    tab1, tab2, tab3 = st.tabs(["Übersicht", "Allgemeine Graphik", "Spezifische Graphiken"])
    with tab1:
       
        col = st.columns((1.6, 2.5, 1), gap='small')
        
        with col[0]:
            container = st.container(border=True)
            with container:
                st.markdown('#### Fortschritt Wesentlichkeitsanalyse')
                aktueller_stand_wesentlichkeitsanalyse()
            container_4 = st.container(border=True)
            with container_4:
                anzahl_punkte_Longlist()
                bewertung_Uebersicht()
            container_5 = st.container(border=True)
            with container_5:
                count_shortlist_points()
                calculate_percentages()
            
        with col[1]:        

            container_1 = st.container(border=True)
            with container_1:
                
                on = st.toggle ("Änderung der Darstellung", True)
                if on:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Auswirkungsbezogene Darstellung**")
                    st.write(" ")
                    st.write(" ")
                    Balken_Auswirkungsbezogen()
                    
                else:
                    st.write(" ")
                    st.write(" ")
                    st.write("**Finanzbezogene Darstellung**")
                    st.write(" ")
                    st.write(" ")
                    Balken_Finanzbezogen()
                       
        with col[2]:

            container_3 = st.container(border=True)
            with container_3:
                count_checkboxes()      

            container_6 = st.container(border=True)
            with container_6:
                st.markdown('#### Stakeholder')
                companies_in_stakeholder_table()

            container_7 = st.container(border=True)
            with container_7:
                st.markdown('#### Stakeholder Ranking')
                stakeholder_ranking()

    with tab2:
        
            chart_übersicht_allgemein_test_2(width=900, height=800)

    with tab3:
            
        
            chart_auswirkungsbezogen(width=900, height=800)
            chart_finanzbezogen(width=900, height=800)
        