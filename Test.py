import streamlit as st
import pickle
import os

class YesNoSelection:
    def __init__(self):
        self.load_session_state()
        self.initialize_state()

    def initialize_state(self):
        options = {'Ja': False, 'Nein': False, 'Durst_Ja': False, 'Durst_Nein': False}
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
        hunger_row = st.columns([1, 0.5, 0.5])
        hunger_row[0].write("Hunger:")
        ja_checked = hunger_row[1].checkbox("Ja", value=st.session_state['yes_no_selection'].get('Hunger_Ja', False), key="hunger_ja")
        nein_checked = hunger_row[2].checkbox("Nein", value=st.session_state['yes_no_selection'].get('Hunger_Nein', False), key="hunger_nein")
        
        durst_row = st.columns([1, 0.5, 0.5])
        durst_row[0].write("Durst:")
        durst_ja_checked = durst_row[1].checkbox("Ja", value=st.session_state['yes_no_selection'].get('Durst_Ja', False), key="durst_ja")
        durst_nein_checked = durst_row[2].checkbox("Nein", value=st.session_state['yes_no_selection'].get('Durst_Nein', False), key="durst_nein")
        
        # Aktualisieren Sie die Zustände im st.session_state korrekt, ohne Schlüssel zu überschreiben
        st.session_state['yes_no_selection']['Hunger_Ja'] = ja_checked
        st.session_state['yes_no_selection']['Hunger_Nein'] = nein_checked
        st.session_state['yes_no_selection']['Durst_Ja'] = durst_ja_checked
        st.session_state['yes_no_selection']['Durst_Nein'] = durst_nein_checked

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