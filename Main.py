import os
import streamlit as st
import hydralit_components as hc
import pickle

# Setzen der Seitenkonfiguration
st.set_page_config(
    page_title="ESG-Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Datei zum Speichern des Sitzungszustands
state_file = 'session_states.pkl'

# Funktion zum Laden des Sitzungszustands
def load_session_state(file):
    if file is not None:
        st.session_state['uploaded'] = True
        st.session_state['file'] = file
        return pickle.load(file)
    else:
        return {}

# Funktion zum Speichern des Sitzungszustands
def save_session_state():
    with open(state_file, 'wb') as f:
        pickle.dump(st.session_state.to_dict(), f)
    st.success("Session state saved!")

# Hauptteil der Anwendung
def main():
    menu_data = [
        {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
        {'id': 'Wesentlichkeitsanalyse', 'label': "Wesentlichkeitsanalyse", 'icon': "fas fa-file-alt"},
        {'id': 'Übersicht', 'label': "Übersicht", 'icon': "fas fa-info-circle"},
    ]

    # Erstellen der Navigationsleiste
    selected_menu = hc.nav_bar(
        menu_definition=menu_data,
        hide_streamlit_markers=False, 
        sticky_nav=True,
        sticky_mode='pinned',
        override_theme={'menu_background': '#0431B4'}
    )

    if selected_menu == 'Wesentlichkeitsanalyse':
        st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: block;}</style>""", unsafe_allow_html=True)
        st.sidebar.title("Wesentlichkeitsanalyse")
        # CSS, um die spezifische Klasse auszublenden
        hide_specific_class = """
            <style>
                .st-emotion-cache-79elbk {
                display: none;
                }
            </style>
        """
        st.markdown(hide_specific_class, unsafe_allow_html=True)

        # Auswahl der Seite über eine SelectBox
        page_option = st.sidebar.selectbox(
            "Wählen Sie eine Option:",
            ['1. Stakeholder Management', '2. Themenspezifische ESRS','3. Eigene Nachhaltigkeitspunkte', '4. Stakeholder Nachhaltigkeitspunkte', '5. Bewertung']
        )

        # Importieren und Ausführen der entsprechenden Funktion aus der Subpage
        def load_page(page_module):
            page_function = getattr(page_module, 'display_page', None)
            if callable(page_function):
                page_function()
            else:
                st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.") 

        if page_option == '1. Stakeholder Management':
            import pages.Stakeholder as Stakeholder_page
            load_page(Stakeholder_page)
        elif page_option == '2. Themenspezifische ESRS':
            import pages.Top_down as Top_down_page
            load_page(Top_down_page)
        elif page_option == '3. Eigene Nachhaltigkeitspunkte':
            import pages.Bottom_up_eigene as Bottom_up_eigene_page
            load_page(Bottom_up_eigene_page)
        elif page_option == '4. Stakeholder Nachhaltigkeitspunkte':
            import pages.Bottom_up_stakeholder as Bottom_up_stakeholder_page
            load_page(Bottom_up_stakeholder_page)
        elif page_option == '5. Bewertung':
            import pages.Bewertung_Nachhaltigkeitspunkte as Bewertung_Nachhaltigkeitspunkte_page
            load_page(Bewertung_Nachhaltigkeitspunkte_page)
    else:
        st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: none;}</style>""", unsafe_allow_html=True)

    if selected_menu == 'Übersicht':
        import pages.Übersicht as Übersicht_page
        Übersicht_page.display_page()
    elif selected_menu == 'How To':
        import pages.how_to as How_to_page
        How_to_page.display_page()

# Display choice for uploading pickle or starting new session
if 'uploaded' not in st.session_state:
    st.write("")  
    # Gewichte für die Spaltenbreiten: Die mittlere Spalte wird schmaler gemacht
    cols = st.columns([3, 1, 3])  # Ändert die Breitenverhältnisse der Spalten
    
    with cols[0]:
        st.markdown("""
            <style>
            .subheader-center {
                text-align: center;
            }
            </style>
            <h2 class="subheader-center">Pickle-Datei hochladen</h2>
            """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type="pkl", key="file_upload")
    
    with cols[1]:
        st.markdown("""
            <style>
            .vertical-line-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 400px;
            }
            .vertical-line {
                border-left: 2px solid gray;
                height: 100%;
            }
            </style>
            <div class="vertical-line-container">
                <div class="vertical-line"></div>
            </div>
            """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
            <style>
            .subheader-center {
                text-align: center;
            }
            .centered-button {
                display: flex;
                justify-content: center;
            }
            </style>
            <h2 class="subheader-center">Neue Sitzung starten</h2>
            """, unsafe_allow_html=True)
        
        # Fügt einen Zeilenumbruch hinzu, um den Button tiefer zu positionieren
        st.write("")
        st.write("")
        st.write("")  
    
        # Zentriert den Button innerhalb der Spalte
        with st.container():
            col1, col2, col3 = st.columns([1,0.4,1])
            with col2:
                if st.button("Neustart", key="restart"):
                    st.session_state['uploaded'] = True
                    st.experimental_rerun()

    if uploaded_file is not None:
        loaded_state = load_session_state(uploaded_file)
        st.session_state.update(loaded_state)
        st.experimental_rerun()
else:
    st.markdown("<h1 style='text-align: center; width: 100%; margin-left: -100; background-color: #08298A; color: #ece5f6'>ESG-Tool</h1>", unsafe_allow_html=True)
    st.markdown("""<style>.element-container { margin: -6px !important; padding: 0px !important;}</style>""", unsafe_allow_html=True)
    main()