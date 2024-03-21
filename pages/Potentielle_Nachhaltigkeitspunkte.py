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
                ["E1", "Klimawandel", "Anpassung an den Klimawandel", ""],
                ["E1", "Klimawandel", "Eindämmung des Klimawandels", ""],
                ["E1", "Klimawandel", "Energie", ""],
                ["E2", "Verschmutzung", "Luftverschmutzung", ""],
                ["E2", "Verschmutzung", "Wasserverschmutzung", ""],
                ["E2", "Verschmutzung", "Bodenverschmutzung", ""],
                ["E2", "Verschmutzung", "Verschmutzung lebender Organismen und Nahrungsressourcen", ""],
                ["E2", "Verschmutzung", "Verschmutzung: Bedenkliche Stoffe", ""],
                ["E2", "Verschmutzung", "Verschmutzung: Sehr bedenkliche Stoffe", ""],
                ["E3", "Wasser- und Meeresressourcen", "Wasserentnahmen", ""],
                ["E3", "Wasser- und Meeresressourcen", "Wasserverbrauch", ""],
                ["E3", "Wasser- und Meeresressourcen", "Wassernutzung", ""],
                ["E3", "Wasser- und Meeresressourcen", "Wassereinleitungen in Gewässer und in die Ozeane", ""],
                ["E3", "Wasser- und Meeresressourcen", "Verschlechterung der Wasser-/Meereshabitate und Intensität des Einflusses auf die Meeresressourcen", ""],
                ["E4", "Biodiversität und Ökosysteme", "Verlust der biologischen Vielfalt", ""],
                ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf den Zustand der Arten", ""],
                ["E4", "Biodiversität und Ökosysteme", "Auswirkungen auf und Abhängigkeiten von Ökosystemleistungen", ""],
                ["E5", "Kreislaufwirtschaft", "Ressourcenzuflüsse, einschließlich Ressourcennutzung", ""],
                ["E5", "Kreislaufwirtschaft", "Ressourcenabflüsse in Bezug auf Produkte und Dienstleistungen", ""],
                ["E5", "Kreislaufwirtschaft", "Abfall", ""],

            ],
            columns=["ESRS", "Nachhaltigkeitsaspekt", "Themen", "Unterthemen"]
        )

    col1, col2 = st.columns([2, 1])  # Ändern der Spaltenverhältnisse für eine breitere Darstellung des DataFrames
    with col1:
        if 'dataf' not in st.session_state:
            st.session_state['dataf'] = pd.DataFrame()  # Initialisiere das DataFrame mit leeren Daten
        st.session_state['dataf'] = st.data_editor(st.session_state['dataf'], num_rows="dynamic", height=700)
    
    with col2:
        uploaded_files = st.file_uploader("Wählen Sie ein Dokument aus", accept_multiple_files=True, key="file_uploader")
        if st.button("Analysieren", key="analyze_button"):
            st.session_state['uploaded_files'] = uploaded_files

        # Verwende die hochgeladenen Dateien aus dem Session State, wenn vorhanden
        if st.session_state['uploaded_files'] is not None:
            for uploaded_file in st.session_state['uploaded_files']:
                bytes_data = uploaded_file.read()
                st.write("Dateiname:", uploaded_file.name)
                st.write(bytes_data)

        # Trennlinie zwischen Datei-Uploader und Selectboxen
        st.markdown("---")  # Markdown für eine horizontale Linie

        #Erstelle Selectboxen für die Eingabe neuer Daten
        esrs = st.selectbox("ESRS", ["E1", "E2", "E3", "E4", "E5"], key="esrs_select")
        nachhaltigkeitsaspekt = st.selectbox("Nachhaltigkeitsaspekt", ["Klimawandel", "Verschmutzung", "Wasser- und Meeresressourcen",  "Biodiversität und Ökosysteme", "Kreislaufwirtschaft"], key="nachhaltigkeitsaspekt_select")
        themen = st.text_input("Thema", key="themen_input")
        unterpunkte = st.text_input("Unterthema", key="unterthemen_input")  

        # Button, um die Auswahl aus den Selectboxen zum DataFrame hinzuzufügen
        if st.button("Hinzufügen"):
            #Füge eine neue Zeile zum DataFrame hinzu
            neue_zeile = {
                "ESRS": esrs,
                "Nachhaltigkeitsaspekt": nachhaltigkeitsaspekt,
                "Themen": themen,
                "Unterthemen": unterpunkte
            }
            neue_zeile = pd.DataFrame([[esrs, nachhaltigkeitsaspekt, themen, unterpunkte]], columns=st.session_state['dataf'].columns)
            st.session_state['dataf'] = pd.concat([st.session_state['dataf'], neue_zeile], ignore_index=True)

        # Trennlinie zwischen Datei-Uploader und Selectboxen
        st.markdown("---")  # Markdown für eine horizontale Linie
        
        # Download-Button
        csv = convert_df_to_csv(st.session_state['dataf'])
        st.download_button(
            label="Tabelle herunterladen",
            data=csv,
            file_name='dataframe.csv',
            mime='text/csv',
        )