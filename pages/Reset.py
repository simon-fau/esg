import streamlit as st
import os
import shutil
import zipfile
from io import BytesIO

import streamlit as st
import os
import shutil
import zipfile
from io import BytesIO

# Definiere die Dateipfade für die Pickle-Dateien
STATE_FILE = 'SessionStates.pkl'
BACKUP_STATE_FILE = 'SessionStatesThemenESRS.pkl'
DEFAULT_STATE_FILE = 'Grundlagen.pkl'
DEFAULT_BACKUP_FILE = 'Grundlagen_Themen_ESRS.pkl'

# Funktion zum Zurücksetzen des Session-Status
def reset_session_state():
    st.session_state.clear()  # Löscht alle Werte aus dem aktuellen Session-Status

    # Überprüfen, ob die Pickle-Dateien 'SessionStates.pkl' und 'SessionStatesThemenESRS.pkl' existieren,
    # und überschreibt sie mit den Standarddateien
    if os.path.exists(STATE_FILE) and os.path.exists(BACKUP_STATE_FILE):
        shutil.copy(DEFAULT_STATE_FILE, STATE_FILE)  # Überschreibt 'SessionStates.pkl' mit 'Grundlagen.pkl'
        shutil.copy(DEFAULT_BACKUP_FILE, BACKUP_STATE_FILE)  # Überschreibt 'SessionStatesThemenESRS.pkl' mit 'Grundlagen_Themen_ESRS.pkl'
        st.success("App wurde erfolgreich zurückgesetzt. Alle gespeicherten Inhalte wurden entfernt. Aktualisieren Sie die Seite im Browser oder starten Sie die App neu.")  # Erfolgsmeldung
    else:
        st.error("Die erforderlichen Pickle-Dateien 'SessionStates.pkl' und 'SessionStatesThemenESRS.pkl' fehlen. Bitte überprüfen Sie, ob die Dateien im Verzeichnis vorliegen.")  # Fehlermeldung, wenn Dateien fehlen

# Funktion zum Simulieren eines modalen Dialogs für die Rücksetzbestätigung
def show_modal_dialog():
    with st.expander("⚠️ Bestätigen Sie Ihre Aktion", expanded=True):  # Ein Klappbereich für die Bestätigung des Resets
        st.write("Sind Sie sicher, dass Sie alle gespeicherten Inhalte aus der App entfernen möchten?")  # Sicherheitsabfrage

        col1, col2, col3 = st.columns([1, 1, 4])  # Drei Spalten für die Buttons
        with col1:
            if st.button("Ja"):  # Wenn der Benutzer auf "Ja" klickt
                reset_session_state()  # Führt die Funktion zum Zurücksetzen der App aus
                st.session_state.modal_open = False  # Schließt das Modal-Fenster
        with col2:
            if st.button("Nein"):  # Wenn der Benutzer auf "Nein" klickt
                st.session_state.modal_open = False  # Schließt das Modal-Fenster
                st.warning("Zurücksetzung abgebrochen.")  # Zeigt eine Warnung an, dass der Prozess abgebrochen wurde

# Funktion zum Erstellen einer ZIP-Datei der beiden Pickle-Dateien und eines Download-Buttons
def download_pickle_files_as_zip():
    # Überprüfen, ob beide Dateien existieren, bevor fortgefahren wird
    if os.path.exists(STATE_FILE) and os.path.exists(BACKUP_STATE_FILE):
        # Erstelle eine ZIP-Datei im Speicher
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            zf.write(STATE_FILE)  # Füge 'SessionStates.pkl' zur ZIP-Datei hinzu
            zf.write(BACKUP_STATE_FILE)  # Füge 'SessionStatesThemenESRS.pkl' zur ZIP-Datei hinzu
        
        # Stelle sicher, dass der Puffer am Anfang ist, bevor er gelesen wird
        zip_buffer.seek(0)

        # Download-Button für die ZIP-Datei
        st.download_button(
            label="Download Pickle Files (ZIP)",  # Beschriftung des Download-Buttons
            data=zip_buffer,  # Daten, die heruntergeladen werden sollen (die ZIP-Datei)
            file_name="Speicherstände.zip",  # Dateiname für den Download
            mime="application/zip"  # MIME-Typ der Datei
        )
    else:
        st.warning("Eine oder beide der erforderlichen Pickle-Dateien fehlen. Bitte überprüfen Sie, ob 'SessionStates.pkl' und 'SessionStatesThemenESRS.pkl' existieren.")  # Warnung, wenn die Dateien fehlen

# Funktion zur Anzeige der Einstellungsseite
def display_settings_page():
    if 'modal_open' not in st.session_state:
        st.session_state.modal_open = False  # Initialisierung des Modal-Status, falls noch nicht vorhanden

    if st.button('🔄 App neu starten'):  # Button zum Triggern des Resets
        st.session_state.modal_open = True  # Öffnet das Modal, wenn der Button geklickt wird
    
    if st.session_state.modal_open:
        show_modal_dialog()  # Zeigt das modale Dialogfenster an, wenn es geöffnet ist
    
    # Bereich für den Download der Pickle-Dateien
    st.subheader("Speicherstände herunterladen")
    download_pickle_files_as_zip()  # Bietet den Download der ZIP-Datei mit den Pickle-Dateien an

# Hauptfunktion zur Anzeige der Seite
def display_page():
    st.subheader("Reset")  # Unterüberschrift der Seite
    st.write("Auf dieser Seite können Sie die App zurücksetzen und die Standardeinstellungen wiederherstellen.")  # Beschreibung der Seite
    display_settings_page()  # Ruft die Funktion auf, die die Einstellungsseite anzeigt

