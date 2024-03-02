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
st.markdown("""<style>section[data-testid="stSidebar"][aria-expanded="true"]{display: none;}</style>""", unsafe_allow_html=True)

# Definition der Navigationsleiste
menu_data = [
    {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
    {'id': 'individual_document', 'label': "Individual Document", 'icon': "fas fa-file-alt"},
    {'id': 'document_collection', 'label': "Document Collection", 'icon': "fas fa-file-archive"},
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
if selected_menu == 'how_to':
    import pages.how_to as how_to_page
    load_page(how_to_page)
elif selected_menu == 'individual_document':
    import pages.individual_document as individual_document_page
    load_page(individual_document_page)
elif selected_menu == 'document_collection':
    import pages.document_collection as document_collection_page
    load_page(document_collection_page)