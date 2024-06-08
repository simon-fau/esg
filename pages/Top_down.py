import streamlit as st
import pickle
import os

class YesNoSelection:
    def __init__(self):
        self.load_session_state()
        self.initialize_state()

    def initialize_state(self):
        options = {
            'Wesentlich_Klimawandel': False,
            'Eher_Wesentlich_Klimawandel': False,
            'Eher_nicht_wesentlich': False,
            'Nicht_Wesentlich_Klimawandel': False,
            'Wesentlich_Klimawandel_2': False,
            'Eher_Wesentlich_Klimawandel_2': False,
            'Eher_nicht_wesentlich_2': False,
            'Nicht_Wesentlich_Klimawandel_2': False
        }
        if 'yes_no_selection' not in st.session_state:
            st.session_state['yes_no_selection'] = options

    def save_session_state(self):
        with open('a.pkl', 'wb') as f:
            pickle.dump(st.session_state['yes_no_selection'], f)

    def load_session_state(self):
        if os.path.exists('a.pkl'):
            with open('a.pkl', 'rb') as f:
                st.session_state['yes_no_selection'] = pickle.load(f)

    def E1_Klimawandel(self):
        topics = [
            ("Anpassung an Klimawandel", "Klimawandel"),
            ("Klimaschutz", "Klimaschutz"),
            ("Energie", "Energie")
        ]
        
        # Erstellen der Überschriftenzeile
        header_row = st.columns([2, 1, 1, 1, 1])
        headers = ["Wesentlich", "Eher Wesentlich", "Eher nicht Wesentlich", "Nicht Wesentlich"]
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)
        
        # Aktualisiere den session_state nur mit den aktuellen Werten der Checkboxen
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([2, 1, 1, 1, 1])
            cols[0].write(f"{topic}:")
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}"
                value = cols[i + 1].checkbox("", value=st.session_state['yes_no_selection'].get(checkbox_key, False), key=checkbox_key)
                current_selection[checkbox_key] = value
    
        # Aktualisiere den session_state mit den aktuellen Auswahlwerten
        st.session_state['yes_no_selection'] = current_selection
    
        st.write(st.session_state['yes_no_selection'])


    def display_selection(self):
        self.E1_Klimawandel()
        button = st.button("Auswahl speichern")
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

def display_session_state_contents():
    st.write("Aktueller Session State Inhalt:")
    st.json(st.session_state['yes_no_selection'])

def display_page():
    tabs = st.tabs(["Klimawandel", "Klimaschutz", "Energie", "Wasser", "Biodiversität"])
    with tabs[0]:
        st.title("Klimawandel")
        selection = YesNoSelection()
        selection.display_selection()
    with tabs[1]:
        st.title("Umweltverschmutzung")
    with tabs[2]:
        pass
    with tabs[3]:
        pass
    with tabs[4]:
        pass
    #display_session_state_contents()  # Zeigt den Inhalt des Session State an