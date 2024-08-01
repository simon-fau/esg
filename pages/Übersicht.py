import streamlit as st
import altair as alt
import pandas as pd
from pages.Stakeholder_Management import stakeholder_ranking
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import  count_bewertete_punkte_übersicht,  bewertung_Uebersicht, anzahl_punkte_Longlist, count_top_down_points, count_internal_points, count_stakeholder_points
from pages.Shortlist import Balken_Finanzbezogen, chart_übersicht_allgemein, chart_auswirkungsbezogen, chart_finanzbezogen, Balken_Auswirkungsbezogen
from pages.Themenspezifische_ESRS import YesNoSelection

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
    else:
        st.info("Es wurden noch keine Inhalte hinzugefügt.")

def count_shortlist_points():
    if 'filtered_df' in st.session_state:
        count = len(st.session_state.filtered_df)
        st.metric("Anzahl der Punkte in der Shortlist:", count)

def companies_in_stakeholder_table():
    if 'company_names' in st.session_state and not st.session_state.company_names.empty:
        st.markdown("Nachhaltigkeitspunkte von folgenden Stakeholdern einbezogen:")
        for index, row in st.session_state.company_names.iterrows():
            st.markdown(f"- {row['Company Name']}")
    else:
        st.info("Keine Stakeholder einbezogen.")

def load_page(page_module):
                page_function = getattr(page_module, 'display_page', None)
                if callable(page_function):
                    page_function()
                else:
                    st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")

# Umwandeln der Daten und erstellen eines session states auf den in def aktueller_stand_wesentlichkeitsanalyse() zugegriffen werden kann
def aktueller_stand_themenspezifische_esrs():
    selection = YesNoSelection()
    total_checkboxes, checked_count = selection.count_marked_rows()

    if checked_count == total_checkboxes:
        st.session_state['checkbox_state_3'] = "Ja"
        st.write("erfolgreich")
    else:
        st.session_state['checkbox__state_3'] = "Nein"
        st.write(f"Nicht erfolgreich: {checked_count} von {total_checkboxes} Checkboxen sind aktiviert.")

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
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(name)
        with col2:
            if key in st.session_state and st.session_state[key] == True:
                completed_count += 1
                st.write("✔")
            else:
                st.write("✘")

def display_page():
    # Check if all relevant session states are empty
    session_states_to_check = [
        'stakeholder_punkte_df', 'filtered_df', 'company_names', 
        'namen_tabelle', 'ranking_table', 'stakeholder_punkte_filtered'
    ]
    if all(key not in st.session_state or st.session_state[key].empty for key in session_states_to_check):
        st.info("Es wurden noch keine Inhalte hinzugefügt.")
        return
    
    tab1, tab2 = st.tabs(["Allgemeine Übersicht", "Graphiken"])
    with tab1:
       

        col = st.columns((1, 2.5, 1), gap='medium')
        
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
                st.markdown('#### Themenbezogene ESRS')
                yes_no_selection = YesNoSelection()
                yes_no_selection.count_marked_rows_übersicht()

            container_6 = st.container(border=True)
            with container_6:
                st.markdown('#### Stakeholder')
                companies_in_stakeholder_table()

            container_7 = st.container(border=True)
            with container_7:
                st.markdown('#### Stakeholder Ranking')
                stakeholder_ranking()

    with tab2:
       
        chart_options = ["Allgemeine Graphik", "Auswirkungsbezoge Graphik", "Finanzbezoge Graphik"]
        selected_chart = st.selectbox("Wähle eine Grafik aus:", chart_options)
                   
        # Anzeigen der ausgewählten Grafik
        if selected_chart == "Allgemeine Graphik":
            chart_übersicht_allgemein(width=900, height=800)
        elif selected_chart == "Auswirkungsbezoge Graphik":
            chart_auswirkungsbezogen(width=900, height=800)
        elif selected_chart == "Finanzbezoge Graphik":
            chart_finanzbezogen(width=900, height=800)
        