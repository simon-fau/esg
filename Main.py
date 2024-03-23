import os
import streamlit as st
import hydralit_components as hc

# Setzen der Seitenkonfiguration
st.set_page_config(
    page_title="ESG-Tool",
    page_icon=os.path.join(os.path.dirname(__file__)),
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hauptüberschrift und Untertitel
st.markdown("<h1 style='text-align: center; width: 100%; margin-left: -100; background-color: #08298A; color: #ece5f6'>ESG-Tool</h1>", unsafe_allow_html=True)

# Entfernt den Abstand von Überschrift und Navbar
st.markdown("""<style>.element-container { margin: -6px !important; padding: 0px !important;}</style>""", unsafe_allow_html=True)

# Sidebar ausblenden
#st.markdown("""<style>section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}</style>""", unsafe_allow_html=True)

# Definition der Navigationsleiste
menu_data = [
    {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
    {'id': 'Wesentlichkeitsanalyse', 'label': "Wesentlichkeitsanalyse", 'icon': "fas fa-file-alt"},
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

#Importieren und Ausführen der entsprechenden Funktion aus der Subpage
def load_page(page_module):
    page_function = getattr(page_module, 'display_page', None)
    if callable(page_function):
        page_function()
    else:
        # Fehlermeldung, wenn die Seite keine Funktion namens 'display_page' hat
        st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.") 

# Verwenden der Auswahl, um die Inhalte der Seite zu ändern
if selected_menu == 'Wesentlichkeitsanalyse':
    st.markdown("""<style>section[data-testid="stSidebar"][aria-expanded="true"]{display: block;}</style>""", unsafe_allow_html=True)
    st.sidebar.title("Ablauf Wesentlichkeitsanalyse")
    
    # CSS, um die spezifische Klasse auszublenden
    hide_specific_class = """
        <style>
            .st-emotion-cache-79elbk {
            display: none;
            }
        </style>
    """

    # Fügen Sie die CSS-Regel in das Streamlit Dokument ein
    st.markdown(hide_specific_class, unsafe_allow_html=True)
    wesentlichkeitsanalyse_options = st.sidebar.radio(
        "Wählen Sie eine Option:",
        ('1.Stakeholder', '2.Potentielle Nachhaltigkeitspunkte', '3.Bewertung Nachhaltigkeitspunkte')
    )

    # Die Optionen werden entsprechend der nummerierten Auswahl angepasst
    if wesentlichkeitsanalyse_options == '1.Stakeholder':
        import pages.Stakeholder as Stakeholder_page
        load_page(Stakeholder_page)
    elif wesentlichkeitsanalyse_options == '2.Potentielle Nachhaltigkeitspunkte':
        import pages.Potentielle_Nachhaltigkeitspunkte as Potentielle_Nachhaltigkeitspunkte_page
        load_page(Potentielle_Nachhaltigkeitspunkte_page)
    elif wesentlichkeitsanalyse_options == '3.Bewertung Nachhaltigkeitspunkte':
        import pages.Bewertung_Nachhaltigkeitspunkte as Bewertung_Nachhaltigkeitspunkte_page
        load_page(Bewertung_Nachhaltigkeitspunkte_page)
else:
    # Verstecke die Sidebar für alle anderen Seiten
    st.markdown("""<style>section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}</style>""", unsafe_allow_html=True)