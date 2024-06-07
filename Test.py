import streamlit as st
import pickle
import os

class YesNoSelection:
    def __init__(self):
        self.load_session_state()
        self.initialize_state()

    def initialize_state(self):
        options = {'Ja': False, 'Nein': False}
        if 'yes_no_selection' not in st.session_state:
            st.session_state['yes_no_selection'] = options

    def save_session_state(self):
        with open('session_state.pkl', 'wb') as f:
            pickle.dump(st.session_state['yes_no_selection'], f)

    def load_session_state(self):
        if os.path.exists('session_state.pkl'):
            with open('session_state.pkl', 'rb') as f:
                st.session_state['yes_no_selection'] = pickle.load(f)

    def create_options_row(self):
        row = st.columns([1, 0.5, 0.5])
        row[0].write("Ihre Auswahl:")
        ja_checked = row[1].checkbox("Ja", value=st.session_state['yes_no_selection']['Ja'])
        nein_checked = row[2].checkbox("Nein", value=st.session_state['yes_no_selection']['Nein'])
        
        st.session_state['yes_no_selection'] = {'Ja': ja_checked, 'Nein': nein_checked}

    def display_selection(self):
        st.header('Ja oder Nein Auswahl')
        self.create_options_row()
        button = st.button("Auswahl speichern")
        if button:
            self.save_session_state()
            st.success("Auswahl erfolgreich gespeichert!")

def display_page():
    st.title("Ja oder Nein Auswahl")
    selection = YesNoSelection()
    selection.display_selection()

if __name__ == "__main__":
    display_page()