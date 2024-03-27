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


with st.expander("**3.** Network Chart & Score-Tabelle", expanded=False):
        col_network, col_score = st.columns([1, 1], gap="small")

        with col_network:
            # Netzwerkdiagramm
            net = Network(height="500px", width="100%", bgcolor="white", font_color="black")
            net.add_node("Mein Unternehmen", color="black", label="", title="")  # Leeres Label und Titel

            for _, row in st.session_state['namen_tabelle'].iterrows():
                size = row['Score'] / 100 * 10 + 15
                color = get_node_color(row['Score'])
                net.add_node(row['Gruppe'], color=color, label=row['Gruppe'], title=row['Gruppe'], size=size)
                net.add_edge("Mein Unternehmen", row['Gruppe'])

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
