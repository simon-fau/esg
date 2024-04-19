import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
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

def display_page():
    st.title("Stakeholder-Analysetool")
    with st.expander("Anleitung"):
        st.markdown("""
        ## Stakeholder-Analysetool
        Dieses Tool hilft Ihnen, Ihre Stakeholder effektiv zu verwalten und zu analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.
        
        ### Anleitung:
        - **Gruppe hinzufügen**: Fügen Sie über die Seitenleiste neue Stakeholder-Gruppen hinzu.
        - **Daten bearbeiten**: Direkt in der Tabelle können Sie vorhandene Informationen ändern.
        - **Zeilen löschen**: Wählen Sie eine oder mehrere Zeilen aus und verwenden Sie den 'Ausgewählte Zeilen löschen' Button, um diese zu entfernen.
        - **Navigieren**: Die Tabelle unterstützt das Sortieren und Filtern, um die Ansicht Ihrer Daten zu optimieren.
        """)

    # Initialize the session state for the DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "Gruppe": [""] * 5,
            "Bestehende Beziehung": [""] * 5,
            "Auswirkung auf Interessen": [""] * 5,
            "Level des Engagements": [""] * 5,
            "Stakeholdergruppe": [""] * 5,
            "Kommunikation": [""] * 5,
            "Art der Betroffenheit": [""] * 5,
            "Zeithorizont": [""] * 5
        })  

    with st.sidebar:
        st.markdown("---")
        gruppe = st.text_input("Gruppe", '', key='gruppe1')
        bestehende_beziehung = st.selectbox("Bestehende Beziehung", ['', 'Ja', 'Nein'], key='bestehende_beziehung')
        auswirkung = st.selectbox("Auswirkung auf Interessen", ['', 'Hoch', 'Mittel', 'Niedrig'], key='auswirkung')
        level_des_engagements = st.selectbox("Level des Engagements", ['', 'Hoch', 'Mittel', 'Niedrig'], key='level_des_engagements')
        stakeholdergruppe = st.selectbox("Stakeholdergruppe", ['', 'Intern', 'Extern'], key='stakeholdergruppe')
        kommunikation = st.selectbox("Kommunikation", ['', 'Regelmäßig', 'Gelegentlich', 'Nie'], key='kommunikation')
        art_der_betroffenheit = st.selectbox("Art der Betroffenheit", ['', 'Direkt', 'Indirekt', 'Keine'], key='art_der_betroffenheit')
        zeithorizont = st.selectbox("Zeithorizont", ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'], key='zeithorizont')
        add_row = st.button('Hinzufügen', key='add_row')

    if add_row:
        if add_row:
            empty_row_index = st.session_state.df[
                (st.session_state.df["Gruppe"] == "") &
                (st.session_state.df["Bestehende Beziehung"] == "") &
                (st.session_state.df["Auswirkung auf Interessen"] == "") &
                (st.session_state.df["Level des Engagements"] == "") &
                (st.session_state.df["Stakeholdergruppe"] == "") &
                (st.session_state.df["Kommunikation"] == "") &
                (st.session_state.df["Art der Betroffenheit"] == "") &
                (st.session_state.df["Zeithorizont"] == "")
            ].first_valid_index()
        if empty_row_index is not None:
            st.session_state.df.at[empty_row_index, "Gruppe"] = gruppe
            st.session_state.df.at[empty_row_index, "Bestehende Beziehung"] = bestehende_beziehung
            st.session_state.df.at[empty_row_index, "Auswirkung auf Interessen"] = auswirkung
            st.session_state.df.at[empty_row_index, "Level des Engagements"] = level_des_engagements
            st.session_state.df.at[empty_row_index, "Stakeholdergruppe"] = stakeholdergruppe
            st.session_state.df.at[empty_row_index, "Kommunikation"] = kommunikation
            st.session_state.df.at[empty_row_index, "Art der Betroffenheit"] = art_der_betroffenheit
            st.session_state.df.at[empty_row_index, "Zeithorizont"] = zeithorizont
        else:
            new_row = {
                "Gruppe": gruppe,
                "Bestehende Beziehung": bestehende_beziehung,
                "Auswirkung auf Interessen": auswirkung,
                "Level des Engagements": level_des_engagements,
                "Stakeholdergruppe": stakeholdergruppe,
                "Kommunikation": kommunikation,
                "Art der Betroffenheit": art_der_betroffenheit,
                "Zeithorizont": zeithorizont
            }
            st.session_state.df = st.session_state.df._append(new_row, ignore_index=True)

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']

    grid_response = AgGrid(
        st.session_state.df.reset_index(),
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=300,
        width='100%',
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        return_mode=DataReturnMode.__members__['AS_INPUT'],  # Adjust the DataReturnMode as per available options
        selection_mode='multiple'
    )

    add_empty_row = st.button('Leere Zeile hinzufügen', key='add_empty_row')
    if add_empty_row:
        empty_row = {

            "Gruppe": "",
            "Bestehende Beziehung": "",
            "Auswirkung auf Interessen": "",
            "Level des Engagements": "",
            "Stakeholdergruppe": "",
            "Kommunikation": "",
            "Art der Betroffenheit": "",
            "Zeithorizont": ""
        }
        st.session_state.df = st.session_state.df._append(empty_row, ignore_index=True)
        st.experimental_rerun()

    delete_rows = st.button('Ausgewählte Zeilen löschen', key='delete_rows')
    if delete_rows:
        selected_rows = grid_response['selected_rows']
        selected_indices = [row['index'] for row in selected_rows]
        st.session_state.df = st.session_state.df.drop(selected_indices)
        st.experimental_rerun()

    save_changes = st.button('Änderungen speichern', key='save_changes')
    if save_changes:
        st.session_state.df = grid_response['data'].set_index('index')
    

    # Berechne den Score für jede Zeile nach der Änderung
    df_temp = pd.DataFrame(grid_response['data'])
    df_temp['Score'] = df_temp.apply(calculate_score, axis=1)

    # Validiere die Änderungen
    st.session_state['namen_tabelle'] = df_temp.sort_values(by='Score', ascending=False).reset_index(drop=True)
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
    
    display_page()
