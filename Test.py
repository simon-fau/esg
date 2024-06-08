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
        hunger_row = st.columns([1, 0.5, 0.5, 0.5, 0.5])
        hunger_row[0].write("Anapssung an Klimawandel:")
        wesentlich_Klimawandel = hunger_row[1].checkbox("Wesentlich", value=st.session_state['yes_no_selection'].get('Wesentlich_Klimawandel', False), key="Wesentlich_Klimawandel")
        eher_wesentlich_Klimawandel = hunger_row[2].checkbox("Eher Wesentlich", value=st.session_state['yes_no_selection'].get('Eher_Wesentlich_Klimawandel', False), key="Eher_Wesentlich_Klimawandel")
        eher_nicht_wesentlich_Klimawandel = hunger_row[3].checkbox("Eher nicht Wesentlich", value=st.session_state['yes_no_selection'].get('Eher_nicht_wesentlich', False), key="Eher_nicht_wesentlich")
        nicht_wesentlich_Klimawandel = hunger_row[4].checkbox("Nicht Wesentlich", value=st.session_state['yes_no_selection'].get('Nicht_Wesentlich_Klimawandel', False), key="Nicht_Wesentlich_Klimawandel")
        
        durst_row = st.columns([1, 0.5, 0.5, 0.5, 0.5])
        durst_row[0].write("Klimaschutz:")
        wesentlich_Klimawandel_2 = hunger_row[1].checkbox("Wesentlich", value=st.session_state['yes_no_selection'].get('Wesentlich_Klimawandel_2', False), key="Wesentlich_Klimawandel_2")
        eher_wesentlich_Klimawandel_2 = hunger_row[2].checkbox("Eher Wesentlich", value=st.session_state['yes_no_selection'].get('Eher_Wesentlich_Klimawandel_2', False), key="Eher_Wesentlich_Klimawandel_2")
        eher_nicht_wesentlich_Klimawandel_2 = hunger_row[3].checkbox("Eher nicht Wesentlich", value=st.session_state['yes_no_selection'].get('Eher_nicht_wesentlich_2', False), key="Eher_nicht_wesentlich_2")
        nicht_wesentlich_Klimawandel_2 = hunger_row[4].checkbox("Nicht Wesentlich", value=st.session_state['yes_no_selection'].get('Nicht_Wesentlich_Klimawandel_2', False), key="Nicht_Wesentlich_Klimawandel_2")
        
        # Aktualisieren Sie die Zustände im st.session_state korrekt, ohne Schlüssel zu überschreiben
        st.session_state['yes_no_selection']['Wesentlich_Klimawandel'] = wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Eher_Wesentlich_Klimawandel'] = eher_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Eher_nicht_wesentlich'] = eher_nicht_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Nicht_Wesentlich_Klimawandel'] = nicht_wesentlich_Klimawandel
        st.session_state['yes_no_selection']['Wesentlich_Klimawandel_2'] = wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Eher_Wesentlich_Klimawandel_2'] = eher_wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Eher_nicht_wesentlich_2'] = eher_nicht_wesentlich_Klimawandel_2
        st.session_state['yes_no_selection']['Nicht_Wesentlich_Klimawandel_2'] = nicht_wesentlich_Klimawandel_2

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