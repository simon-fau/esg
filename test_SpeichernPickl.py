import pytest
import pickle
from unittest import mock
import streamlit as st
from pages.Longlist import save_state

# Test für die save_state-Funktion
def test_save_state():
    # Definiere eine Mock-Datei
    mock_file = mock.mock_open()

    # Definiere den Zustand, der in st.session_state gespeichert werden soll
    session_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": 123
    }

    # Simuliere das Vorhandensein von st.session_state
    with mock.patch('streamlit.session_state', session_data):
        # Mock für die 'open'-Funktion, um zu vermeiden, dass tatsächlich eine Datei erstellt wird
        with mock.patch('builtins.open', mock_file):
            # Mock für 'pickle.dump' um zu überprüfen, ob die Daten korrekt gespeichert werden
            with mock.patch('pickle.dump') as mock_pickle_dump:
                # Rufe die save_state-Funktion auf
                save_state()

                # Überprüfe, ob die Datei korrekt geöffnet wurde
                mock_file.assert_called_once_with('SessionStates.pkl', 'wb')  # Passe hier den Dateinamen an

                # Überprüfe, ob pickle.dump mit den korrekten Daten aufgerufen wurde
                mock_pickle_dump.assert_called_once_with(session_data, mock.ANY)
