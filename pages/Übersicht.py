import streamlit as st
from pages.Stakeholder_Management import display_stakeholder_ranking_and_network
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import merge_dataframes, bewertung_Uebersicht


def display_stakeholder_table():
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered

    if not stakeholder_punkte_filtered.empty:
        stakeholder_punkte_filtered.reset_index(inplace=True)
        stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)
        grid_response = display_aggrid(stakeholder_punkte_filtered.drop(columns=['_index']), with_checkboxes=True)
    else:
        st.warning("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")

def companies_in_stakeholder_table():
    if 'company_names' in st.session_state: 
        st.markdown("**Nachhaltigkeitspunkte von folgenden Stakeholdern einbezogen:**")
        for index, row in st.session_state.company_names.iterrows():
            st.markdown(f"- {row['Company Name']}")

def display_page():
    tab1, tab2 = st.tabs(["Stakeholder", "Longlist"])

    with tab1:
        st.title("Bewertete Nachhaltigkeitspunkte der Stakeholder:")
        display_stakeholder_table()
        display_stakeholder_ranking_and_network()
        companies_in_stakeholder_table()

    with tab2:
        st.write("Longlist")
        merge_dataframes()
        bewertung_Uebersicht()

        
    