import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd
from pyvis.network import Network

def generate_stakeholder_ranking():
    # Überprüfe, ob 'namen_tabelle' initialisiert und nicht leer ist
    if 'namen_tabelle' not in st.session_state or st.session_state['namen_tabelle'].empty:
        st.write("Keine Daten vorhanden für das Stakeholder-Ranking.")
        return pd.DataFrame()  # Frühes Beenden mit leerer DataFrame

    score_table = st.session_state['namen_tabelle'][['Gruppe', 'Score']].copy()
    if not score_table.empty:
        score_table['Ranking'] = range(1, len(score_table) + 1)
        score_table = score_table.sort_values(by='Score', ascending=False).reset_index(drop=True)
        st.dataframe(score_table[['Ranking', 'Gruppe', 'Score']], column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, hide_index=True)
    else:
        st.write("Keine Stakeholder-Daten vorhanden.")

def get_node_color(score):
    if score <= 33:
        return "red"
    elif score <= 66:
        return "orange"
    else:
        return "green"

def calculate_score(row):
    engagement_mapping = {'Hoch': 3, 'Mittel': 1.5, 'Niedrig': 0}
    kommunikation_mapping = {'Regelmäßig': 3, 'Gelegentlich': 1.5, 'Nie': 0}
    zeithorizont_mapping = {'Langfristig': 3, 'Mittelfristig': 1.5, 'Kurzfristig': 0}
    
    score = (engagement_mapping.get(row['Level des Engagements'], 0) +
             kommunikation_mapping.get(row['Kommunikation'], 0) +
             zeithorizont_mapping.get(row['Zeithorizont'], 0)) / 9 * 100
    
    return round(score)

def validate_data(df):
    erlaubte_werte = {
        'Bestehende Beziehung': ['', 'Ja', 'Nein'],
        'Auswirkung auf Interessen': ['', 'Hoch', 'Mittel', 'Niedrig'],
        'Level des Engagements': ['', 'Hoch', 'Mittel', 'Niedrig'],
        'Stakeholdergruppe': ['', 'Intern', 'Extern'],
        'Kommunikation': ['', 'Regelmäßig', 'Gelegentlich', 'Nie'],
        'Art der Betroffenheit': ['', 'Direkt', 'Indirekt', 'Keine'],
        'Zeithorizont': ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig']
    }

    for spalte, erlaubte in erlaubte_werte.items():
        if not set(df[spalte].dropna()).issubset(set(erlaubte)):
            return False, f"Fehler: Ungültige Werte in Spalte '{spalte}'. Eintrag wurde nicht übernommen. Erlaubte Werte sind: {', '.join(erlaubte)}"
    
    return True, "Daten sind gültig."

def add_entry_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.header("Neuen Eintrag hinzufügen")
        gruppe = st.text_input("Gruppe", '')
        bestehende_beziehung = st.selectbox("Bestehende Beziehung", ['', 'Ja', 'Nein'])
        auswirkung = st.selectbox("Auswirkung auf Interessen", ['', 'Hoch', 'Mittel', 'Niedrig'])
        level_des_engagements = st.selectbox("Level des Engagements", ['', 'Hoch', 'Mittel', 'Niedrig'])
        stakeholdergruppe = st.selectbox("Stakeholdergruppe", ['', 'Intern', 'Extern'])
        kommunikation = st.selectbox("Kommunikation", ['', 'Regelmäßig', 'Gelegentlich', 'Nie'])
        art_der_betroffenheit = st.selectbox("Art der Betroffenheit", ['', 'Direkt', 'Indirekt', 'Keine'])
        zeithorizont = st.selectbox("Zeithorizont", ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'])

        if st.button("Eintrag hinzufügen"):
            new_entry = {
                'Gruppe': gruppe,
                'Bestehende Beziehung': bestehende_beziehung,
                'Auswirkung auf Interessen': auswirkung,
                'Level des Engagements': level_des_engagements,
                'Stakeholdergruppe': stakeholdergruppe,
                'Kommunikation': kommunikation,
                'Art der Betroffenheit': art_der_betroffenheit,
                'Zeithorizont': zeithorizont,
                'Score': 0  # Initialscore, wird später aktualisiert
            }

            new_entry_df = pd.DataFrame([new_entry])
            st.session_state['namen_tabelle'] = pd.concat([st.session_state['namen_tabelle'], new_entry_df], ignore_index=True)
            # Aktualisiere den Key für AgGrid, um eine Neurenderung zu erzwingen
            st.session_state['grid_update_key'] = st.session_state.get('grid_update_key', 0) + 1

def display_page():

    if 'namen_tabelle' not in st.session_state:
        st.session_state['namen_tabelle'] = pd.DataFrame({
            'Gruppe': ['Beispielgruppe'],
            'Bestehende Beziehung': ['Ja'],
            'Auswirkung auf Interessen': ['Hoch'],
            'Level des Engagements': ['Mittel'],
            'Stakeholdergruppe': ['Intern'],
            'Kommunikation': ['Regelmäßig'],
            'Art der Betroffenheit': ['Direkt'],
            'Zeithorizont': ['Langfristig'],
            'Score': [0]  # Initialscore für bestehende Einträge
        })

    add_entry_sidebar()
    
    # Erstelle eine Kopie des DataFrames ohne die 'Score'-Spalte für das AgGrid
    df_for_aggrid = st.session_state['namen_tabelle'].drop(columns=['Score'])

    gb = GridOptionsBuilder.from_dataframe(df_for_aggrid)
    gb.configure_default_column(editable=True, resizable=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True, rowMultiSelectWithClick=True, suppressRowDeselection=False)
    gb.configure_grid_options(enableRangeSelection=True, domLayout='normal')
    gridOptions = gb.build()

    # Anzeige der Tabelle mit AgGrid
    grid_key = f"grid_{st.session_state.get('grid_update_key', 0)}"
    grid_response = AgGrid(
        df_for_aggrid,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme='streamlit',
        enable_enterprise_modules=True,
        key=grid_key 
    )


    # Berechne den Score für jede Zeile nach der Änderung
    df_temp = pd.DataFrame(grid_response['data'])
    df_temp['Score'] = df_temp.apply(calculate_score, axis=1)

    # Validiere die Änderungen
    valid, message = validate_data(df_temp)
    if not valid:
        st.error(message)
    else:
        st.session_state['namen_tabelle'] = df_temp.sort_values(by='Score', ascending=False).reset_index(drop=True)
        st.markdown("---")
        col_score, col_network, col_empty = st.columns([1, 1, 1], gap="small")
        with col_score:
            # Erstelle eine neue DataFrame für die Score-Tabelle und füge die Ranking-Spalte hinzu
            st.session_state['namen_tabelle'] = df_temp.sort_values(by='Score', ascending=False).reset_index(drop=True)
            generate_stakeholder_ranking()
        
        with col_network:
            # Netzwerkdiagramm
            net = Network(height="300px", width="100%", bgcolor="white", font_color="black")
            net.add_node("Mein Unternehmen", color="black", label="", title="")  # Leeres Label und Titel

            for _, row in st.session_state['namen_tabelle'].iterrows():
                size = row['Score'] / 100 * 10 + 15
                color = get_node_color(row['Score'])
                net.add_node(row['Gruppe'], color=color, label=row['Gruppe'], title=row['Gruppe'], size=size)
                net.add_edge("Mein Unternehmen", row['Gruppe'])

            net.save_graph("network.html")
            st.components.v1.html(open("network.html", "r").read(), height=600)    