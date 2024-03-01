import streamlit as st
import pandas as pd


def display_page():

    # Initialisiere den Session State als leeren DataFrame, wenn er noch nicht gesetzt wurde
    if 'namen_tabelle' not in st.session_state:
        st.session_state['namen_tabelle'] = pd.DataFrame(columns=['Gruppe'])
    
    st.title("Wesentlichkeitsanalyse")
    
   
    

  

    with st.expander("**1.** Steakholdergruppen hinzufügen"):
    
        # Erstelle Spalten für das Layout
        col1, col2 = st.columns([1, 1])

        # Selectbox in der ersten Spalte
        with col1:
            auswahl = st.selectbox('', ['Mitarbeiter', 'Kunden', 'Investoren'], key='unique_selectbox_key', label_visibility="collapsed")

        # Button in der zweiten Spalte
        with col2:
            add_button = st.button('Hinzufügen')

        # Prüfe, ob der Button gedrückt wurde
        if add_button:
            new_row = pd.DataFrame([auswahl], columns=['Gruppe'])


            st.session_state['namen_tabelle'] = pd.concat([st.session_state['namen_tabelle'], new_row], ignore_index=True)
    
    with st.expander("**2.** Stakeholder Beziehungen", expanded=len(st.session_state['namen_tabelle']) > 0):

        # Zeige die Tabelle mit den hinzugefügten Namen an, wenn sie nicht leer ist
        if len(st.session_state['namen_tabelle']) > 0:
            # Anzeigen der Tabelle mit der Möglichkeit zum dynamischen Bearbeiten
            edited_df = st.data_editor(st.session_state['namen_tabelle'], num_rows="dynamic")
            # Aktualisiere den Session State nach der Bearbeitung
            st.session_state['namen_tabelle'] = edited_df
        else:
            # Wenn die Tabelle leer ist, leere den entsprechenden Session State
            st.session_state['namen_tabelle'] = pd.DataFrame(columns=['Gruppe'])
            # Anzeigen der leeren Tabelle
            st.data_editor(st.session_state['namen_tabelle'], num_rows="dynamic")


