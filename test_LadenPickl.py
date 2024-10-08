import os
import pickle
import pytest
import tempfile
from unittest import mock
from Main import load_pickle  # Angenommen, deine Funktion ist in Main.py

# Test für nicht existierende Datei
def test_load_pickle_file_not_exist():
    result = load_pickle('non_existent_file.pkl')
    assert result is None

# Test für leere Datei
def test_load_pickle_empty_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        pass  # Erstelle eine leere Datei
    try:
        result = load_pickle(file_path)
        assert result is None
    finally:
        os.remove(file_path)  # Leere Datei löschen

# Test für korrektes Laden einer Pickle-Datei
def test_load_pickle_valid_file():
    data = {"key": "value"}
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    try:
        result = load_pickle(file_path)
        assert result == data  # Die geladenen Daten sollten den gespeicherten entsprechen
    finally:
        os.remove(file_path)  # Temporäre Datei löschen

# Test für eine fehlerhafte Pickle-Datei
def test_load_pickle_corrupted_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        with open(file_path, 'wb') as f:
            f.write(b'not a pickle')  # Schreibe ungültige Daten
    try:
        with mock.patch('streamlit.error') as mock_error:  # Mock für st.error
            result = load_pickle(file_path)
            assert result is None
            mock_error.assert_called_once_with("UnpicklingError: Die Pickle-Datei ist nicht korrekt formatiert.")
    finally:
        os.remove(file_path)  # Temporäre Datei löschen
