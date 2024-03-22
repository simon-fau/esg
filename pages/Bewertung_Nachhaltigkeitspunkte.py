import streamlit as st

def display_page():
    # Direktes Hinzufügen von Sidebar-Elementen
    st.sidebar.title("Sidebar für Bewertung")
    st.sidebar.write("Hier können Sie die Nachhaltigkeitspunkte bewerten.")
    # Beispiel: Ein Slider in der Sidebar
    bewertung = st.sidebar.slider("Bewertung", 0, 10, 5)
    
    # Hauptinhalt der Seite
    st.write("Bewertung Nachhaltigkeitspunkte")
    st.write(f"Ihre aktuelle Bewertung: {bewertung}")


