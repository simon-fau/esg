import pytest
import pandas as pd
import numpy as np
import streamlit as st
from unittest import mock
from Main import merge_dataframes, submit_bewertung

# Test for merge_dataframes function
def test_merge_dataframes():
    # Mock session_state with sample data for Themenspezifische_ESRS, Stakeholder, and Eigene
    with mock.patch.dict(st.session_state, {
        'relevance_selection': {'Relevant_E1': True},
        'df2': pd.DataFrame({'Thema': ['Thema1'], 'Unterthema': ['Unterthema1'], 'Unter-Unterthema': ['Unter-Unterthema1']}),
        'stakeholder_punkte_filtered': pd.DataFrame({'Thema': ['Thema2'], 'Unterthema': ['Unterthema2'], 'Unter-Unterthema': ['Unter-Unterthema2'], 'Stakeholder Gesamtbew': [5], 'Stakeholder Bew Finanzen': [3], 'Stakeholder Bew Auswirkung': [4]})
    }):
        # Call the merge_dataframes function
        merge_dataframes()

        # Check if the combined DataFrame is in session_state and not empty
        assert 'combined_df' in st.session_state
        combined_df = st.session_state['combined_df']
        assert not combined_df.empty
        
        # Check if IDs are assigned correctly
        assert 'ID' in combined_df.columns
        assert combined_df['ID'].is_unique  # Ensure IDs are unique

        # Ensure the data from different sources are merged correctly
        assert len(combined_df) == 2  # Two sources of data merged

        # Verify data in the merged DataFrame
        assert 'Stakeholder Gesamtbew' in combined_df.columns
        assert combined_df.loc[combined_df['Thema'] == 'Thema2', 'Stakeholder Gesamtbew'].values[0] == 5

# Test for submit_bewertung function
def test_submit_bewertung():
    # Mock session_state with sample longlist and selected rows
    longlist = pd.DataFrame({'ID': [1, 2], 'Bewertet': ['Nein', 'Nein']})
    selected_rows = [{'ID': 1, 'Thema': 'Thema1', 'Unterthema': 'Unterthema1', 'Unter-Unterthema': 'Unter-Unterthema1'}]
    
    with mock.patch.dict(st.session_state, {'selected_rows': selected_rows}):
        # Define the ausgewaehlte_werte dictionary simulating user inputs for the Bewertung
        ausgewaehlte_werte = {
            "auswirkung_option": "Negative Auswirkung",
            "auswirkung_art_option": "Tatsächliche Auswirkung",
            "ausmass_neg_tat": "Erhöht",
            "umfang_neg_tat": "Regional",
            "behebbarkeit_neg_tat": "Mit hohem Aufwand",
            "ausmass_neg_pot": "Durchschnittlich",
            "umfang_neg_pot": "Lokal",
            "behebbarkeit_neg_pot": "Mäßiger Aufwand",
            "wahrscheinlichkeit_neg_pot": "Möglich",
            "ausmass_pos_tat": None,
            "umfang_pos_tat": None,
            "art_finanziell": "Risiko",
            "wahrscheinlichkeit_finanziell": "Wahrscheinlich",
            "ausmass_finanziell": "Stark"
        }

        # Call submit_bewertung function
        updated_longlist = submit_bewertung(longlist, ausgewaehlte_werte)
        
        # Check if the selected_data DataFrame is created in session_state
        assert 'selected_data' in st.session_state
        selected_data = st.session_state['selected_data']
        
        # Ensure that the selected row has been added to selected_data
        assert len(selected_data) == 1
        assert selected_data.loc[0, 'ID'] == 1
        
        # Check if the correct financial score is calculated
        assert selected_data.loc[0, 'Score Finanzen'] == pytest.approx(750, 0.1)  # Check financial score calculation
        
        # Check if the correct impact score is calculated
        assert selected_data.loc[0, 'Score Auswirkung'] == pytest.approx(1000, 0.1)  # Example score calculation

        # Ensure the longlist is updated correctly
        assert updated_longlist.loc[updated_longlist['ID'] == 1, 'Bewertet'].values[0] == 'Ja'
