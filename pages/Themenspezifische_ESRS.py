import streamlit as st
import pickle
import os

def Text():
    st.markdown("""
        Bitte bewerten Sie die Themengebiete anhand ihrer Relevanz für Ihr Unternehmen. Dabei gilt folgende Definition für die verschiedenen Auswahlmöglichkeiten:
        - **Wesentlich**:  Ein Aspekt ist wesentlich, wenn er signifikante tatsächliche oder potenzielle Auswirkungen auf Menschen oder die Umwelt hat oder wesentliche finanzielle Auswirkungen auf das Unternehmen nach sich zieht bzw. zu erwarten sind.
        - **Eher Wesentlich**: Ein Aspekt ist eher wesentlich, wenn er bedeutende, aber nicht unbedingt kritische Auswirkungen auf Menschen oder die Umwelt hat oder wenn finanzielle Auswirkungen wahrscheinlich, aber nicht zwingend erheblich sind.
        - **Eher nicht Wesentlich**: Ein Aspekt ist eher nicht wesentlich, wenn die Auswirkungen auf Menschen oder die Umwelt begrenzt sind oder die finanziellen Auswirkungen gering oder unwahrscheinlich sind.
        - **Nicht Wesentlich**: Ein Aspekt ist nicht wesentlich, wenn er keine oder nur vernachlässigbare Auswirkungen auf Menschen, die Umwelt oder die Finanzen des Unternehmens hat.
    """)

if 'relevance_selection' not in st.session_state:
    st.session_state['relevance_selection'] = {}

# Speichert den aktuellen Zustand der Auswahloptionen in eine Pickle-Datei
def save_session_state():
    with open('session_states_top_down.pkl', 'wb') as f:
        pickle.dump(st.session_state['relevance_selection'], f)

# Lädt den Zustand der Auswahloptionen aus einer Pickle-Datei
def load_session_state():
    if os.path.exists('session_states_top_down.pkl'):
        with open('session_states_top_down.pkl', 'rb') as f:
            st.session_state['relevance_selection'] = pickle.load(f)

# Definiert die Struktur für Auswahlsektionen ohne Untersektionen z.B für Klimawandel
def display_section(topics, section_key, section_title):
    form_key = f'form_{section_key}'
    with st.form(key=form_key, border=False):
        st.subheader(section_title)
        headers = ["Relevant", "Nicht Relevant"]
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)

        current_selection = {}
        validation_passed = True

        for topic, key in topics:
            cols = st.columns([4, 1, 1])
            cols[0].write(f"{topic}:")
            selected_count = 0
            for i, header in enumerate(headers):
                checkbox_key = f"{header}_{key}_{section_key}"
                checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                current_selection[checkbox_key] = checkbox_state
                if checkbox_state:
                    selected_count += 1
            if selected_count > 1:
                validation_passed = False

        submitted = st.form_submit_button("💾 Auswahl speichern")
        if submitted:
            st.session_state['relevance_selection'] = {**st.session_state['relevance_selection'], **current_selection}
            if validation_passed:
                st.success("Auswahl erfolgreich gespeichert!")
                save_session_state()
            else:
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")

    return validation_passed

# Definiert die Struktur für komplexe Auswahlsektionen mit mehreren Untersektionen z.B für Biodiversität
def display_complex_section(sections, section_key, section_title):
    form_key = f'form_{section_key}'
    with st.form(key=form_key):
        st.subheader(section_title)
        headers = ["Relevant", "Nicht Relevant"]
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            header_row[i + 1].write(header)

        def create_section(title, topics):
            st.markdown(f"**{title}**")
            current_selection = {}
            validation_passed = True
            for topic, key in topics:
                cols = st.columns([4, 1, 1])
                cols[0].write(f"{topic}:")
                selected_count = 0
                for i, header in enumerate(headers):
                    checkbox_key = f"{header}_{key}_{section_key}"
                    checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                    checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                    current_selection[checkbox_key] = checkbox_state
                    if checkbox_state:
                        selected_count += 1
                if selected_count > 1:
                    validation_passed = False
            return current_selection, validation_passed

        all_validation_passed = True
        for section_title, topics in sections:
            current_selection, validation_passed = create_section(section_title, topics)
            st.session_state['relevance_selection'] = {
                **st.session_state['relevance_selection'],
                **current_selection
            }
            if not validation_passed:
                all_validation_passed = False

        submitted = st.form_submit_button("💾 Auswahl speichern")
        if submitted:
            if all_validation_passed:
                st.success("Auswahl erfolgreich gespeichert!")
                save_session_state()
            else:
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")

    return all_validation_passed

# Zeigt die Auswahloptionen für Klimawandel an
def display_E1_Klimawandel():
    topics = [("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"), ("Klimaschutz", "Klimaschutz"), ("Energie", "Energie")]
    validation_passed = display_section(topics, "E1", "Klimawandel")


# Hauptfunktion zum Anzeigen der Seite mit den verschiedenen Auswahloptionen
def display_page():
    
    load_session_state()
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("Themenspezifische ESRS") 
    with col2:
        container = st.container(border=True)
        with container:
            pass
            
    Text()

    tabs = st.tabs(["Klimawandel"])
    with tabs[0]:
        display_E1_Klimawandel()
    