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

# Definition der Navigationsleiste
menu_data = [
    {'id': 'how_to', 'label': "How To", 'icon': "fa fa-home"},
    {'id': 'Wesentlichkeitsanalyse', 'label': "Wesentlichkeitsanalyse", 'icon': "fas fa-file-alt"},
    {'id': 'Übersicht', 'label': "Übersicht", 'icon': "fas fa-info-circle"},
    {'id': 'Dokumentenanalyse', 'label': "Dokumentenanalyse", 'icon': "fas fa-info-circle"},
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
        ['1. Stakeholder', '2. Top-Down','3. Eigene Nachhaltigkeitspunkte hinzufügen', '4. Stakeholder Nachhaltigkeitspunkte hinzufügen', '5. Bewertung Nachhaltigkeitspunkte']
    )

    # Importieren und Ausführen der entsprechenden Funktion aus der Subpage
    def load_page(page_module):
        page_function = getattr(page_module, 'display_page', None)
        if callable(page_function):
            page_function()
        else:
            st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.") 

    if page_option == '1. Stakeholder':
        import pages.Stakeholder as Stakeholder_page
        load_page(Stakeholder_page)
    elif page_option == '2. Top-Down':
        import pages.Top_down as Top_down_page
        load_page(Top_down_page)
    elif page_option == '3. Eigene Nachhaltigkeitspunkte hinzufügen':
        import pages.Bottom_up_eigene as Bottom_up_eigene_page
        load_page(Bottom_up_eigene_page)
    elif page_option == '4. Stakeholder Nachhaltigkeitspunkte hinzufügen':
        import pages.Bottom_up_stakeholder as Bottom_up_stakeholder_page
        load_page(Bottom_up_stakeholder_page)
    elif page_option == '5. Bewertung Nachhaltigkeitspunkte':
        import pages.Bewertung_Nachhaltigkeitspunkte as Bewertung_Nachhaltigkeitspunkte_page
        load_page(Bewertung_Nachhaltigkeitspunkte_page)
else:
    st.markdown("""<style>section[data-testid='stSidebar'][aria-expanded='true']{display: none;}</style>""", unsafe_allow_html=True)

if selected_menu == 'Übersicht':
    import pages.Übersicht as Übersicht_page
    Übersicht_page.display_page()
elif selected_menu == 'Dokumentenanalyse':
    import pages.Dokumentenanalyse as Dokumentenanalyse_page
    Dokumentenanalyse_page.display_page()

   