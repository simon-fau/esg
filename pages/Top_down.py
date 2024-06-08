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

    def create_options_row(self):
        # Erstellen der Überschriftenzeile
        header_row = st.columns([2, 1, 1, 1, 1])
        header_row[1].write("Wesentlich")
        header_row[2].write("Eher Wesentlich")
        header_row[3].write("Eher nicht Wesentlich")
        header_row[4].write("Nicht Wesentlich")

        # Erste Zeile für "Anpassung an Klimawandel"
        Klimawandel_row = st.columns([2, 1, 1, 1, 1])
        Klimawandel_row[0].write("Anpassung an Klimawandel:")
        wesentlich_Klimawandel = Klimawandel_row[1].checkbox("", value=st.session_state['yes_no_selection'].get('Wesentlich_Klimawandel', False), key="Wesentlich_Klimawandel")
        eher_wesentlich_Klimawandel = Klimawandel_row[2].checkbox("", value=st.session_state['yes_no_selection'].get('Eher_Wesentlich_Klimawandel', False), key="Eher_Wesentlich_Klimawandel")
        eher_nicht_wesentlich_Klimawandel = Klimawandel_row[3].checkbox("", value=st.session_state['yes_no_selection'].get('Eher_nicht_wesentlich', False), key="Eher_nicht_wesentlich")
        nicht_wesentlich_Klimawandel = Klimawandel_row[4].checkbox("", value=st.session_state['yes_no_selection'].get('Nicht_Wesentlich_Klimawandel', False), key="Nicht_Wesentlich_Klimawandel")
        
        # Zweite Zeile für "Klimaschutz"
        Klimawandel_2_row = st.columns([2, 1, 1, 1, 1])
        Klimawandel_2_row[0].write("Klimaschutz:")
        wesentlich_Klimawandel_2 = Klimawandel_2_row[1].checkbox("", value=st.session_state['yes_no_selection'].get('Wesentlich_Klimawandel_2', False), key="Wesentlich_Klimawandel_2")
        eher_wesentlich_Klimawandel_2 = Klimawandel_2_row[2].checkbox("", value=st.session_state['yes_no_selection'].get('Eher_Wesentlich_Klimawandel_2', False), key="Eher_Wesentlich_Klimawandel_2")
        eher_nicht_wesentlich_Klimawandel_2 = Klimawandel_2_row[3].checkbox("", value=st.session_state['yes_no_selection'].get('Eher_nicht_wesentlich_2', False), key="Eher_nicht_wesentlich_2")
        nicht_wesentlich_Klimawandel_2 = Klimawandel_2_row[4].checkbox("", value=st.session_state['yes_no_selection'].get('Nicht_Wesentlich_Klimawandel_2', False), key="Nicht_Wesentlich_Klimawandel_2")
        
        # Aktualisieren der Zustände im st.session_state
        st.session_state['yes_no_selection']['Wesentlich_Klimawandel'] = wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Eher_Wesentlich_Klimawandel'] = eher_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Eher_nicht_wesentlich'] = eher_nicht_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Nicht_Wesentlich_Klimawandel'] = nicht_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Wesentlich_Klimawandel_2'] = wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Eher_Wesentlich_Klimawandel_2'] = eher_wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Eher_nicht_wesentlich_2'] = eher_nicht_wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Nicht_Wesentlich_Klimawandel_2'] = nicht_wesentlich_Klimawandel_2

    def display_selection(self):
        self.create_options_row()
        button = st.button("Auswahl speichern")
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

def display_session_state_contents():
    st.write("Aktueller Session State Inhalt:")
    st.json(st.session_state['yes_no_selection'])

def display_page():
    st.title("Klimawandel")
    selection = YesNoSelection()
    selection.display_selection()
    display_session_state_contents()  # Zeigt den Inhalt des Session State an