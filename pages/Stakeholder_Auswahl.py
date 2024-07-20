import streamlit as st
import pandas as pd

def update_session_state():
    if 'ranking_table' in st.session_state:
        current_ranking = st.session_state['ranking_table']['Gruppe'].tolist()
        if 'table2' not in st.session_state:
            st.session_state.table2 = []
        if 'table1' not in st.session_state:
            st.session_state.table1 = current_ranking
        else:
            new_items = [item for item in current_ranking if item not in st.session_state.table1 and item not in st.session_state.table2]
            st.session_state.table1.extend(new_items)
    else:
        st.error("No ranking table found in session state")

def display_page():
    st.title("Stakeholder Auswahl")
    st.write("Wählen Sie die Stakeholder aus, die Sie in die Bewertung aufnehmen möchten.")
    
    update_session_state()

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Nicht in Bewertung aufgenommene Stakeholder:**")
        if 'ranking_table' in st.session_state:
            ranking_table = st.session_state['ranking_table'].copy()
            
            if 'Score' in ranking_table.columns:
                ranking_table['Score'] = ranking_table['Score'].apply(lambda x: x)  # Remove percentage formatting if any
                not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.table1)]
                st.dataframe(not_in_evaluation[['Ranking', 'Gruppe', 'Score']],
                             hide_index=True,
                             width=800)
            else:
                not_in_evaluation = ranking_table[ranking_table['Gruppe'].isin(st.session_state.table1)]
                st.dataframe(not_in_evaluation[['Ranking', 'Gruppe']],
                             hide_index=True,
                             width=800)

            selected_table1 = st.multiselect(
                "Wählen Sie Stakeholder zum Hinzufügen aus:",
                st.session_state.table1,
                key="select_table1"
            )
            if st.button("Hinzufügen >>>"):
                add_to_table2(selected_table1)
                st.experimental_rerun()
    
    with col2:
        st.write("**In Bewertung aufgenommene Stakeholder:**")
        if st.session_state.table2:
            table2_df = st.session_state['ranking_table'][st.session_state['ranking_table']['Gruppe'].isin(st.session_state.table2)]
            if 'Score' in table2_df.columns:
                table2_df['Score'] = table2_df['Score'].apply(lambda x: x)  # Remove percentage formatting if any
                st.dataframe(table2_df[['Ranking', 'Gruppe', 'Score']],
                             hide_index=True,
                             width=800)
            else:
                st.dataframe(table2_df[['Ranking', 'Gruppe']],
                             hide_index=True,
                             width=800)

            selected_table2 = st.multiselect(
                "Wählen Sie Stakeholder zum Entfernen aus:",
                table2_df['Gruppe'].tolist(),
                key="select_table2"
            )
            if st.button("<<< Entfernen"):
                remove_from_table2(selected_table2)
                st.experimental_rerun()

def add_to_table2(selected_items):
    for item in selected_items:
        if item in st.session_state.table1:
            st.session_state.table2.append(item)
            st.session_state.table1.remove(item)

def remove_from_table2(selected_items):
    for item in selected_items:
        if item in st.session_state.table2:
            st.session_state.table2.remove(item)
            st.session_state.table1.append(item)
