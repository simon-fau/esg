import os
import streamlit as st
import hydralit_components as hc
import pickle
import pandas as pd

# Funktion zum Laden einer Pickle-Datei mit Fehlerbehandlung
def load_pickle(file_path):
    # Überprüfen, ob die Datei existiert
    if not os.path.exists(file_path):
        return None  # Wenn die Datei nicht existiert, None zurückgeben

    # Überprüfen, ob die Datei leer ist
    if os.path.getsize(file_path) == 0:
        return None  

    # Versuchen, die Pickle-Datei zu laden, mit Fehlerbehandlung
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)  # Pickle-Datei laden und den Inhalt zurückgeben
    except EOFError:
        # Streamlit-Fehlermeldung anzeigen, wenn die Datei leer oder beschädigt ist
        st.error("EOFError: Die Pickle-Datei ist leer oder beschädigt.")
        return None  
    except pickle.UnpicklingError:
        # Streamlit-Fehlermeldung anzeigen, wenn die Pickle-Datei nicht korrekt formatiert ist
        st.error("UnpicklingError: Die Pickle-Datei ist nicht korrekt formatiert.")
        return None  

# Pfad zur Pickle-Datei setzen
pickle_file_path = os.path.join(os.path.dirname(__file__), 'session_states.pkl')

# Daten aus der Pickle-Datei laden
loaded_data = load_pickle(pickle_file_path)

# Initialisieren von Session States, falls Daten geladen wurden
if loaded_data is not None:
    for key, value in loaded_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Seitenkonfiguration festlegen
st.set_page_config(
    page_title="ESG-Tool",  # Titel der Seite
    page_icon=os.path.join(os.path.dirname(__file__), 'Pflanze.jpg'),  # Icon der Seite
    layout="wide",  # Breites Layout
    initial_sidebar_state="expanded"  # Die Seitenleiste ist standardmäßig erweitert
)

#  Festlegung von Hintergrundfarbe, Textfarbe und Schriftgröße des Titels
st.markdown("<h1 style='text-align: center; width: 100%; margin-left: -100; background-color: #08298A; color: #ece5f6'>ESG-Tool</h1>", unsafe_allow_html=True)

# Entfernen von Abständen in Titeln und Navigationsleisten
st.markdown("""<style>.element-container { margin: -6px !important; padding: 0px !important;}</style>""", unsafe_allow_html=True)

# Definition der Navigationsleiste
menu_data = [
    {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
    {'id': 'Wesentlichkeitsanalyse', 'label': "Wesentlichkeitsanalyse", 'icon': "fas fa-file-alt"},
    {'id': 'Allgemeine_Angaben', 'label': "Allgemeine Angaben", 'icon': "fas fa-file-alt"},
    {'id': 'Mindestangabepflicht', 'label': "Mindestangabepflicht", 'icon': "fas fa-file-alt"},
    {'id': 'Übersicht', 'label': "Übersicht", 'icon': "fas fa-info-circle"},
    {'id': 'Einstellungen', 'label': "Einstellungen & Ausleitung", 'icon': "fas fa-cog"}  
]

# Erstellen der Navigationsleiste
selected_menu = hc.nav_bar(
    menu_definition=menu_data, # Menüdefinition von oben
    hide_streamlit_markers=False,  # Streamlit-Markierungen nicht verstecken
    sticky_nav=True,  # Navigation bleibt am Bildschirm haften
    sticky_mode='pinned',  # "Gepinnt"-Modus für die Navigation
    override_theme={'menu_background': '#0431B4'}  # Hintergrundfarbe der Navigationsleiste anpassen
)

# Funktion zum Laden der ausgewählten Seite
def load_page(page_module):
    # Überprüfen, ob die Seite eine Funktion 'display_page' hat
    page_function = getattr(page_module, 'display_page', None)
    if callable(page_function):
        page_function()  # Die Funktion 'display_page' ausführen
    else:
        st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")

# Wenn der Nutzer 'Wesentlichkeitsanalyse' aus dem Menü auswählt
if selected_menu == 'Wesentlichkeitsanalyse':

    # Öffnen der Sidebar, wenn 'Wesentlichkeitsanalyse' ausgewählt ist
    st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: block;}</style>""", unsafe_allow_html=True)
    
    # Titel der Sidebar setzen
    st.sidebar.title("Wesentlichkeitsanalyse")
    
    # Ausblenden der Subpages in der Sidebar, indem ganze Klasse ausgeblendet wird. Ersichtlich in der app durch Rechtklick auf Sidebar dann "Untersuchen"
    hide_specific_class = """
        <style>
            .st-emotion-cache-79elbk {
            display: none;
            }
        </style>
    """
    st.markdown(hide_specific_class, unsafe_allow_html=True)

    # Auswahlbox in der Sidebar anzeigen
    page_option = st.sidebar.selectbox(
        "Wählen Sie eine Option:",
        ['1. Stakeholder Management', '2. Stakeholder Auswahl', '3. Themenspezifische ESRS', '4. Interne Nachhaltigkeitspunkte', '5. Externe Nachhaltigkeitspunkte', '6. Bewertung der Longlist', '7. Erstellung der Shortlist']
    )

    # Laden der Subpages, die in die Sidebar der Wesntlichkeitsanalyse eingebunden sind
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

# Verstecken der Sidebar, wenn andere Hauptnavigationspunkt als die WA ausgewählt werden
else:
    st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: none;}</style>""", unsafe_allow_html=True)

# Laden der Subpages als Navigationspunkte
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
elif selected_menu == 'Einstellungen':
    import pages.Einstellungen as Einstellungen_page
    Einstellungen_page.display_page()
