import streamlit as st
import pandas as pd

def convert_df_to_csv(df):
    # Konvertiere ein DataFrame in ein CSV-Objekt, bereit zum Herunterladen
    return df.to_csv(index=False).encode('utf-8')

def display_page():

    # Initialisiere den Session State für die hochgeladenen Dateien, falls noch nicht geschehen
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files'] = None

    # Initialisiere den Session State für das DataFrame, falls noch nicht geschehen
    if 'dataf' not in st.session_state:
        # Initialisiere das DataFrame mit den gegebenen Inhalten
        st.session_state['dataf'] = pd.DataFrame(
            [
                ["E1", "Klimawandel", "Anpassung an den Klimawandel", "", "Standard"],
                ["E1", "Klimawandel", "Eindämmung des Klimawandels", "", "Standard"],
                ["E1", "Klimawandel", "Energie", "", "Standard"],
                ["E2", "Verschmutzung", "Luftverschmutzung", "", "Standard"],
                ["E2", "Verschmutzung", "Wasserverschmutzung", "", "Standard"],
                ["E2", "Verschmutzung", "Bodenverschmutzung", "", "Standard"],
                ["E2", "Verschmutzung", "Verschmutzung lebender Organismen und Nahrungsressourcen", "", "Standard"],
                ["E2", "Verschmutzung", "Verschmutzung: Bedenkliche Stoffe", "", "Standard"],
                ["E2", "Verschmutzung", "Verschmutzung: Sehr bedenkliche Stoffe", "", "Standard"],
                ["E3", "Wasser- und Meeresressourcen", "Wasserentnahmen", "", "Standard"],
                ["E3", "Wasser- und Meeresressourcen", "Wasserverbrauch", "", "Standard"],
                ["E3", "Wasser- und Meeresressourcen", "Wassernutzung", "", "Standard"],
                ["E3", "Wasser- und Meeresressourcen", "Wassereinleitungen in Gewässer und in die Ozeane", "", "Standard"],
                ["E3", "Wasser- und Meeresressourcen", "Verschlechterung der Wasser-/Meereshabitate und Intensität des Einflusses auf die Meeresressourcen", "", "Standard"],
                ["E4", "Biodiversität und Ökosysteme", "Verlust der biologischen Vielfalt", "", "Standard"],
                ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf den Zustand der Arten", "", "Standard"],
                ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf und Abhängigkeiten von Ökosystemleistungen", "", "Standard"],
                ["E5", "Kreislaufwirtschaft", "Ressourcenzuflüsse, einschließlich Ressourcennutzung", "", "Standard"],
                ["E5", "Kreislaufwirtschaft", "Ressourcenabflüsse in Bezug auf Produkte und Dienstleistungen", "", "Standard"],
                ["E5", "Kreislaufwirtschaft", "Abfall", "", "Standard"],

            ],
            columns=["ESRS", "Nachhaltigkeitsaspekt", "Themen", "Unterthemen", "Datenherkunft"]
        )

    

    # Sidebar für Datei-Upload und Eingaben
    with st.sidebar:

        st.markdown("---")

        uploaded_files = st.file_uploader("Wählen Sie ein Dokument aus", accept_multiple_files=True)
        if uploaded_files is not None and len(uploaded_files) > 0:
            st.session_state['uploaded_files'] = uploaded_files
        
        # Eingabefelder in der Sidebar
        st.markdown("---")  # Markdown für eine horizontale Linie
        esrs = st.selectbox("ESRS", ["E1", "E2", "E3", "E4", "E5"], key="esrs_select")
        nachhaltigkeitsaspekt = st.selectbox(
            "Nachhaltigkeitsaspekt",
            ["Klimawandel", "Verschmutzung", "Wasser- und Meeresressourcen", "Biodiversität und Ökosysteme", "Kreislaufwirtschaft"],
            key="nachhaltigkeitsaspekt_select"
        )
        themen = st.text_input("Thema", key="themen_input")
        unterthemen = st.text_input("Unterthema", key="unterthemen_input")
        
        if st.button("Hinzufügen", key="hinzufuegen_button"):
            # Füge den neuen Eintrag zum DataFrame hinzu
            neue_zeile = pd.DataFrame(
                [[esrs, nachhaltigkeitsaspekt, themen, unterthemen, "Hinzugefügt"]],
                columns=["ESRS", "Nachhaltigkeitsaspekt", "Themen", "Unterthemen", "Datenherkunft"]
            )
            st.session_state['dataf'] = pd.concat([st.session_state['dataf'], neue_zeile], ignore_index=True)

            # Hauptbereich für die Anzeige des DataFrames
    st.write("Übersicht der potentiellen Nachhaltigkeitspunkte")
    with st.expander("Tabelle anzeigen/ausblenden", expanded=False):
        st.dataframe(st.session_state['dataf'], height=750, width=1500)

        # Download-Button für das gesamte DataFrame als CSV
        csv = convert_df_to_csv(st.session_state['dataf'])
        st.download_button("Tabelle herunterladen", csv, "dataframe.csv", "text/csv")

    # Wenn Dateien hochgeladen wurden, zeige sie an und lies ihre Daten
    if st.session_state['uploaded_files']:
        for uploaded_file in st.session_state['uploaded_files']:
            bytes_data = uploaded_file.read()
            st.write("Dateiname:", uploaded_file.name)

    



