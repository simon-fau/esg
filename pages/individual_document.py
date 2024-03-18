import streamlit as st
import pandas as pd
from pyvis.network import Network

def get_empfehlung(score):
    if score > 66:
        return "Einladung und Interview von Repräsentanten, Definition gemeinsamer Ziele und Projekte"
    elif 33 < score <= 66:
        return "Stakeholder-Dialog mittels Umfrage"
    else:
        return "offene Unternehmenkommunikation"

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

def get_node_color(score):
    if score <= 33:
        return "red"
    elif score <= 66:
        return "orange"
    else:
        return "green"

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
            kommunikation = st.selectbox('Kommunikation*:', ['', 'Regelmäßig', 'Gelegentlich', 'Nie'], key='kommunikation')
            zeithorizont = st.selectbox('Zeithorizont*:', ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'], key='zeithorizont')
        with col3:
            auswirkung = st.selectbox('Auswirkung auf Interessen:', ['', 'Hoch', 'Mittel', 'Niedrig'], key='auswirkung')
            stakeholdergruppe = st.selectbox('Stakeholdergruppe:', ['', 'Intern', 'Extern'], key='stakeholdergruppe')
            art_der_betroffenheit = st.selectbox('Art der Betroffenheit:', ['', 'Direkt', 'Indirekt', 'Keine'], key='art_der_betroffenheit')
            level_des_engagements = st.selectbox('Level des Engagements*:', ['', 'Hoch', 'Mittel', 'Niedrig'], key='level_des_engagements')

        add_button = st.button('Hinzufügen', key='add_button')

        if add_button and gruppe:
            # Überprüfe, ob verpflichtende Felder ausgefüllt sind
            if level_des_engagements == '' or kommunikation == '' or zeithorizont == '':
                st.warning("Bitte füllen Sie die verpflichtenden Felder aus: Level des Engagements, Kommunikation, und Zeithorizont.")
            elif gruppe in st.session_state['namen_tabelle']['Gruppe'].values:
                st.warning("Diese Gruppe existiert bereits.")
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

    with st.expander("**3.** Network Chart & Score-Tabelle", expanded=False):
        col_network, col_score = st.columns([1, 1], gap="small")

        with col_network:
            # Netzwerkdiagramm
            net = Network(height="500px", width="100%", bgcolor="white", font_color="black")
            net.add_node(".", color="black", label="", title="")  # Leeres Label und Titel

            for _, row in st.session_state['namen_tabelle'].iterrows():
                size = row['Score'] / 100 * 10 + 15
                color = get_node_color(row['Score'])
                net.add_node(row['Gruppe'], color=color, label=row['Gruppe'], title=row['Gruppe'], size=size)
                net.add_edge(".", row['Gruppe'])

            net.save_graph("network.html")
            st.components.v1.html(open("network.html", "r").read(), height=600)

        with col_score:
             # Platzierungstabelle
            score_df = st.session_state['namen_tabelle'].copy()
            score_df['Platzierung'] = score_df['Score'].rank(ascending=False).astype(int)
            score_df['Empfehlung'] = score_df['Score'].apply(get_empfehlung)
            score_table = score_df[['Platzierung', 'Gruppe', 'Empfehlung']].sort_values(by='Platzierung')
            st.write("**Stakeholder Score Platzierung:**")
            st.table(score_table[['Platzierung', 'Gruppe', 'Empfehlung']].set_index('Platzierung'))