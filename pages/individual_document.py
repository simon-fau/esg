import streamlit as st
import pandas as pd

def calculate_score(row):
    # Mapping der Auswahlmöglichkeiten auf numerische Werte
    engagement_mapping = {'Hoch': 3, 'Mittel': 1.5, 'Niedrig': 0}
    kommunikation_mapping = {'Regelmäßig': 3, 'Gelegentlich': 1.5, 'Nie': 0}
    zeithorizont_mapping = {'Langfristig': 3, 'Mittelfristig': 1.5, 'Kurzfristig': 0}
    
    # Berechnung des Scores basierend auf den Werten der Auswahlmöglichkeiten
    score = (engagement_mapping.get(row['Level des Engagements'], 0) +
             kommunikation_mapping.get(row['Kommunikation'], 0) +
             zeithorizont_mapping.get(row['Zeithorizont'], 0))/9 * 100
    
    return score

def display_page():
    
    if 'namen_tabelle' not in st.session_state:
        st.session_state['namen_tabelle'] = pd.DataFrame(columns=[
            'Gruppe', 'Bestehende Beziehung', 'Auswirkung auf Interessen', 
            'Level des Engagements', 'Stakeholdergruppe', 'Kommunikation', 
            'Art der Betroffenheit', 'Zeithorizont', 'Score'
        ])

    st.session_state.setdefault('expander_open', False)
    st.subheader("Wesentlichkeitsanalyse")

    with st.expander("**1.** Stakeholdergruppen hinzufügen", expanded=not st.session_state['expander_open']):
        col1, col2, col3 = st.columns([3, 2, 2], gap="small")
        with col1:
            gruppe = st.text_input('Gib eine Gruppe ein:', key='unique_text_key')

        # Sammle Auswahlen aus den Selectboxen
        with col2:
            bestehende_beziehung = st.selectbox('Bestehende Beziehung:', ['', 'Ja', 'Nein'], key='bestehende_beziehung')
            kommunikation = st.selectbox('Kommunikation:', ['', 'Regelmäßig', 'Gelegentlich', 'Nie'], key='kommunikation')
            zeithorizont = st.selectbox('Zeithorizont:', ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'], key='zeithorizont')
        with col3:
            auswirkung = st.selectbox('Auswirkung auf Interessen:', ['', 'Hoch', 'Mittel', 'Niedrig'], key='auswirkung')
            stakeholdergruppe = st.selectbox('Stakeholdergruppe:', ['', 'Intern', 'Extern'], key='stakeholdergruppe')
            art_der_betroffenheit = st.selectbox('Art der Betroffenheit:', ['', 'Direkt', 'Indirekt', 'Keine'], key='art_der_betroffenheit')
            level_des_engagements = st.selectbox('Level des Engagements:', ['', 'Hoch', 'Mittel', 'Niedrig'], key='level_des_engagements')

        add_button = st.button('Hinzufügen', key='add_button')

        if add_button and gruppe:
            # Überprüfe, ob verpflichtende Felder ausgefüllt sind
            if level_des_engagements == '' or kommunikation == '' or zeithorizont == '':
                st.warning("Bitte füllen Sie die verpflichtenden Felder aus: Level des Engagements, Kommunikation, und Zeithorizont.")
            else:
                # Erstelle eine neue Zeile mit allen ausgewählten Werten und berechne den Score
                new_row = pd.DataFrame([{
                    'Gruppe': gruppe, 
                    'Bestehende Beziehung': bestehende_beziehung, 
                    'Auswirkung auf Interessen': auswirkung,
                    'Kommunikation': kommunikation,
                    'Stakeholdergruppe': stakeholdergruppe,
                    'Zeithorizont': zeithorizont,
                    'Art der Betroffenheit': art_der_betroffenheit,
                    'Level des Engagements': level_des_engagements,
                    'Score': calculate_score({
                        'Level des Engagements': level_des_engagements,
                        'Kommunikation': kommunikation,
                        'Zeithorizont': zeithorizont
                    })
                }])
                st.session_state['namen_tabelle'] = pd.concat([st.session_state['namen_tabelle'], new_row], ignore_index=True)
                st.session_state['expander_open'] = True  # Expander soll geöffnet werden

    with st.expander("**2.** Stakeholder Beziehungen", expanded=st.session_state['expander_open']):
        if not st.session_state['namen_tabelle'].empty:
            edited_df = st.data_editor(st.session_state['namen_tabelle'], num_rows="dynamic")
            st.session_state['namen_tabelle'] = edited_df
        else:
            st.write("Noch keine Daten vorhanden.")

display_page()





