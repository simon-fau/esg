import streamlit as st
# Erstellen der Navigationsleiste
selected_menu = st.sidebar.radio()

#Importieren und Ausführen der entsprechenden Funktion aus der Subpage
def load_page(page_module):
    page_function = getattr(page_module, 'display_page', None)
    if callable(page_function):
        page_function()
    else:
        # Fehlermeldung, wenn die Seite keine Funktion namens 'display_page' hat
        st.error(f"Fehler: Die Seite {page_module.__name__} hat keine Funktion namens 'display_page'.")

if  selected_menu == 'Wesentlichkeitsanalyse':
    import pages.Wesentlichkeitsanalyse as Wesentlichkeitsanalyse_page
    load_page(Wesentlichkeitsanalyse_page)
elif selected_menu == 'Bewertung_Nachhaltigkeitspunkte':
    import Subpages.Bewertung_Nachhaltigkeitspunkte as Bewertung_Nachhaltigkeitspunkte_page
    load_page(Bewertung_Nachhaltigkeitspunkte_page)
elif selected_menu == 'Potentielle_Nachhaltigkeitspunkte':
    import Subpages.Potentielle_Nachhaltigkeitspunkte as Potentielle_Nachhaltigkeitspunkte_page
    load_page(Potentielle_Nachhaltigkeitspunkte_page)