import streamlit as st
import pickle
import os
import time

def initialize_state():
    if 'yes_no_selection' not in st.session_state:
        st.session_state['yes_no_selection'] 

def save_session_state():
    with open('session_states_top_down.pkl', 'wb') as f:
        pickle.dump(st.session_state['yes_no_selection'], f)

def load_session_state():
    if os.path.exists('session_states_top_down.pkl'):
        with open('session_states_top_down.pkl', 'rb') as f:
            st.session_state['yes_no_selection'] = pickle.load(f)
    else:
        initialize_state()

def Text():
    st.markdown("""
        Bitte bewerten Sie die Themengebiete anhand ihrer Relevanz für Ihr Unternehmen. Dabei gilt folgende Definition für die verschiedenen Auswahlmöglichkeiten:
        - **Relevant für Bewertung**: Ein Aspekt ist relevant für die Bewertung, wenn er signifikante tatsächliche oder potenzielle Auswirkungen auf Menschen oder die Umwelt hat oder wesentliche finanzielle Auswirkungen auf das Unternehmen nach sich zieht bzw. zu erwarten sind.
        - **Unrelevant für Bewertung**: Ein Aspekt ist unrelevant für die Bewertung, wenn die Auswirkungen auf Menschen oder die Umwelt begrenzt sind oder die finanziellen Auswirkungen gering oder unwahrscheinlich sind.
    """)

def display_section(topics, section_key):
    current_selection = {}

    # CSS to increase the horizontal spacing between radio buttons
    st.markdown(
        """
        <style>
        .stRadio > div {
            display: flex;
            gap: 155px; /* Adjust the value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for topic, key in topics:
        cols = st.columns([3.35, 1])
        cols[0].write(f"{topic}:")
        radio_key = f"Relevance_{key}_{section_key}"
        selected_option = st.session_state['yes_no_selection'].get(radio_key, None)
        option = cols[1].radio("", options=[" ", " "],index=0 if selected_option == "Relevant für Bewertung" else 1 if selected_option == "Unrelevant für Bewertung" else None, key=radio_key, label_visibility='collapsed', horizontal=True)
        current_selection[radio_key] = option

    st.session_state['yes_no_selection'] = {**st.session_state['yes_no_selection'], **current_selection}
    return True

def display_complex_section(sections, section_key):

    def create_section(title, topics):
        st.markdown(f"**{title}**")
        current_selection = {}
        for topic, key in topics:
            cols = st.columns([3.35, 1])
            cols[0].write(f"{topic}:")
            radio_key = f"Relevance_{key}_{section_key}"
            selected_option = st.session_state['yes_no_selection'].get(radio_key, None)
            option = cols[1].radio("", options=[" ", " "], index=0 if selected_option == "Relevant für Bewertung" else 1 if selected_option == "Unrelevant für Bewertung" else None, key=radio_key, label_visibility='collapsed', horizontal=True)
            current_selection[radio_key] = option
        return current_selection

    for section_title, topics in sections:
        current_selection = create_section(section_title, topics)
        st.session_state['yes_no_selection'] = {
            **st.session_state['yes_no_selection'],
            **current_selection
        }

    return True

def display_save_button(section_name):
    Placeholder()
    col1, col2 = st.columns([5, 1.5])
    with col2:
        Placeholder()
        # CSS für rechtsbündige Anzeige des Buttons
        st.markdown(
            """
            <style>
            .stButton button {
                float: right;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        if st.button(f"💾 Auswahl speichern", key=f'Button_{section_name}'):
            success_placeholder = st.empty()
            success_placeholder.success(f"Auswahl erfolgreich gespeichert!")
            save_session_state()
            time.sleep(3)
            success_placeholder.empty()
                
def display_E1_Klimawandel():
    topics = [("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"), ("Klimaschutz", "Klimaschutz"), ("Energie", "Energie")]
    display_section(topics, "E1")
    display_save_button("Klimawandel")

def display_E2_Umweltverschmutzung():
    topics = [
        ("Luftverschmutzung", "Luftverschmutzung"), ("Wasserverschmutzung", "Wasserverschmutzung"), ("Bodenverschmutzung", "Bodenverschmutzung"),
        ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Verschmutzung_von_lebenden_Organismen_und_Nahrungsressourcen"),
        ("Besorgniserregende Stoffe", "Besorgniserregende_Stoffe"), ("Besonders besorgniserregende Stoffe", "Besonders_besorgniserregende_Stoffe"), ("Mikroplastik", "Mikroplastik")
    ]
    display_section(topics, "E2")
    display_save_button("Umweltverschmutzung")

def display_E3_Wasser_und_Meeresressourcen():
    topics = [
        ("Wasserverbrauch", "Wasserverbrauch"), ("Wasserentnahme", "Wasserentnahme"), ("Ableitung von Wasser", "Ableitung_von_Wasser"),
        ("Ableitung von Wasser in die Ozeane", "Ableitung_von_Wasser_in_die_Ozeane"), ("Gewinnung und Nutzung von Meeresressourcen", "Gewinnung_und_Nutzung_von_Meeresressourcen")
    ]
    display_section(topics, "E3")
    display_save_button("WasserundMeeresressourcen")

def display_E4_Biodiversität():
    sections = [
        ("Direkte Ursachen des Biodiversitätsverlusts", [
            ("Klimawandel", "Klimawandel"),
            ("Land-, Süßwasser- und Meeresnutzungsänderungen", "Land-_Süßwasser-_und_Meeresnutzungsänderungen"),
            ("Direkte Ausbeutung", "Direkte_Ausbeutung"),
            ("Invasive gebietsfremde Arten", "Invasive_gebietsfremde_Arten"),
            ("Umweltverschmutzung", "Umweltverschmutzung"),
            ("Sonstige", "Sonstige")
        ]),
        ("Auswirkungen auf den Zustand der Arten", [
            ("Populationsgröße von Arten", "Populationsgröße_von_Arten"),
            ("Globales Ausrottungsrisiko von Arten", "Globales_Ausrottungsrisiko_von_Arten")
        ]),
        ("Auswirkungen auf den Umfang und den Zustand von Ökosystemen", [
            ("Landdegradation", "Landdegradation"),
            ("Wüstenbildung", "Wüstenbildung"),
            ("Bodenversiegelung", "Bodenversiegelung")
        ]),
        ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", [
            ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", "Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistungen")
        ])
    ]
    display_complex_section(sections, "E4")
    display_save_button("Biodiversität")

def Placeholder():
    st.write("")
    st.write("")
    st.write("")
    st.write("")

def display_page():

    load_session_state()
    initialize_state()
    col1, col2 = st.columns([4, 1])
    with col1:
        st.header("Themenspezifische ESRS") 
    with col2:
        pass
                     
    Text()

    tabs = st.tabs(["Klimawandel", "Umweltverschmutzung", "Wasser- und Meeressourcen", "Biodiversität"])
    
    with tabs[0]:
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            st.subheader("Klimawandel")
        with col2:
            pass
        with col3:
            st.write("**Relevant für Bewertung**")
        with col4:
            st.write("**Unrelevant für Bewertung**")
            
        Placeholder()
        display_E1_Klimawandel()
    
    with tabs[1]:
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            st.subheader("Umweltverschmutzung")
        with col2:
            pass
        with col3:
            st.write("**Relevant für Bewertung**")
        with col4:
            st.write("**Unrelevant für Bewertung**")

        Placeholder()
        display_E2_Umweltverschmutzung()
    
    with tabs[2]:
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            st.subheader("Meeres- und Wasserressourcen")
        with col2:
            pass
        with col3:
            st.write("**Relevant für Bewertung**")
        with col4:
            st.write("**Unrelevant für Bewertung**")

        Placeholder()
        display_E3_Wasser_und_Meeresressourcen()
    
    with tabs[3]:
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            st.subheader("Biodiversität")
        with col2:
            pass
        with col3:
            st.write("**Relevant für Bewertung**")
        with col4:
            st.write("**Unrelevant für Bewertung**")
            
        Placeholder()
        display_E4_Biodiversität()

