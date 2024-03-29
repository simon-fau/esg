import streamlit as st

def display_page():
    # Definieren Sie die Struktur Ihrer Daten
    themen = ["Klimawandel"] * 3
    unterthemen = ["Anpassung an den Klimawandel", "Klimaschutz", "Energie"]

    # Erstellen Sie einen Expander für das Thema "E1 Klimawandel"
    with st.expander("ESRS E1 Klimawandel"):
        for unterthema in unterthemen:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.text("• " + unterthema)
            with col2:
                st.checkbox("", key=unterthema)

display_page()
    



