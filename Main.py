import os
import streamlit as st
import hydralit_components as hc
import pickle
import pandas as pd

# Funktion zum Laden der Pickle-Datei mit Fehlerbehandlung
def load_pickle(file_path):
    if not os.path.exists(file_path):
        return None

    if os.path.getsize(file_path) == 0:
        return None

    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except EOFError:
        st.error("EOFError: Die Pickle-Datei ist leer oder beschädigt.")
        return None
    except pickle.UnpicklingError:
        st.error("UnpicklingError: Die Pickle-Datei ist nicht korrekt formatiert.")
        return None

# Laden der Pickle-Datei der Longlist.py
pickle_file_path = os.path.join(os.path.dirname(__file__), 'a.pkl')
loaded_data = load_pickle(pickle_file_path)

# Initialisierung der Session States
if loaded_data is not None:
    for key, value in loaded_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Setzen der Seitenkonfiguration
st.set_page_config(
    page_title="ESG-Tool",
    page_icon=os.path.join(os.path.dirname(__file__)),
    layout="wide",
    initial_sidebar_state="expanded"  
)

# Hauptüberschrift und Untertitel
st.markdown("<h1 style='text-align: center; width: 100%; margin-left: -100; background-color: #08298A; color: #ece5f6'>ESG-Tool</h1>", unsafe_allow_html=True)

# Entfernt den Abstand von Überschrift und Navbar
st.markdown("""<style>.element-container { margin: -6px !important; padding: 0px !important;}</style>""", unsafe_allow_html=True)

# Definition der Navigationsleiste
menu_data = [
    {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
    {'id': 'Wesentlichkeitsanalyse', 'label': "Wesentlichkeitsanalyse", 'icon': "fas fa-file-alt"},
    {'id': 'Allgemeine_Angaben', 'label': "Allgemeine Angaben", 'icon': "fas fa-file-alt"},
    {'id': 'Mindestangabepflicht', 'label': "Mindestangabepflicht", 'icon': "fas fa-file-alt"},
    {'id': 'Übersicht', 'label': "Übersicht", 'icon': "fas fa-info-circle"}
]

# Erstellen der Navigationsleiste
selected_menu = hc.nav_bar(
    menu_definition=menu_data,
    hide_streamlit_markers=False, 
    sticky_nav=True,
    sticky_mode='pinned',
    override_theme={'menu_background': '#0431B4'}
)

def load_page(page_module):
    page_function = getattr(page_module, 'display_page', None)
    if callable(page_function):
        page_function()
    else:
        st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")

if selected_menu == 'Wesentlichkeitsanalyse':
    st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: block;}</style>""", unsafe_allow_html=True)
    st.sidebar.title("Wesentlichkeitsanalyse")
    hide_specific_class = """
        <style>
            .st-emotion-cache-79elbk {
            display: none;
            }
        </style>
    """
    st.markdown(hide_specific_class, unsafe_allow_html=True)

    page_option = st.sidebar.selectbox(
        "Wählen Sie eine Option:",
        ['1. Stakeholder Management', '2. Stakeholder Auswahl', '3. Themenspezifische ESRS', '4. Interne Nachhaltigkeitspunkte', '5. Externe Nachhaltigkeitspunkte', '6. Bewertung der Longlist', '7. Erstellung der Shortlist']
    )

    if page_option == '1. Stakeholder Management':
        import pages.Stakeholder_Management as Stakeholder_page
        load_page(Stakeholder_page)
    elif page_option == '2. Stakeholder Auswahl':
        import pages.Stakeholder_Auswahl as Stakeholder_Auswahl_page
        load_page(Stakeholder_Auswahl_page)
    elif page_option == '3. Themenspezifische ESRS':
        import pages.Themenspezifische_ESRS as Top_down_page
        load_page(Top_down_page)
    elif page_option == '4. Interne Nachhaltigkeitspunkte':
        import pages.Interne_Nachhaltigkeitspunkte as Bottom_up_eigene_page
        load_page(Bottom_up_eigene_page)
    elif page_option == '5. Externe Nachhaltigkeitspunkte':
        import pages.Externe_Nachhaltigkeitspunkte as Bottom_up_stakeholder_page
        load_page(Bottom_up_stakeholder_page)
    elif page_option == '6. Bewertung der Longlist':
        import pages.Longlist as Bewertung_Nachhaltigkeitspunkte_page
        load_page(Bewertung_Nachhaltigkeitspunkte_page)
    elif page_option == '7. Erstellung der Shortlist':
        import pages.Shortlist as Shortlist_page
        load_page(Shortlist_page)
else:
    st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: none;}</style>""", unsafe_allow_html=True)

if selected_menu == 'Übersicht':
    import pages.Übersicht as Übersicht_page
    Übersicht_page.display_page()
elif selected_menu == 'how_to':
    import pages.how_to as How_to_page
    How_to_page.display_page()
elif selected_menu == 'Allgemeine_Angaben': 
    import pages.Allgemeine_Angaben as Allgemeine_Angaben_page
    Allgemeine_Angaben_page.display_page()
elif selected_menu == 'Mindestangabepflicht':
    import pages.Mindestangabepflicht as Mindestangabepflicht_page
    Mindestangabepflicht_page.display_page()