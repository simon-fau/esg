@echo off
cd /d "%~dp0"  # Wechselt in das Verzeichnis der Batch-Datei
streamlit run Main.py  # Startet die Streamlit-App "Main.py"
