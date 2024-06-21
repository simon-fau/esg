import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pyvis.network import Network

# Datei zum Speichern des Sitzungszustands
state_file = 'session_state_stakeholder.pkl'

# Funktion zum Laden des Sitzungszustands
def load_session_state():
    if os.path.exists(state_file):
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

# Funktion zum Speichern des Sitzungszustands
def save_session_state(state):
    # Laden des aktuellen Zustands
    current_state = load_session_state()
    # Hinzufügen des neuen Zustands zum aktuellen Zustand
    combined_state = {**current_state, **state}
    # Speichern des kombinierten Zustands
    with open(state_file, 'wb') as f:
        pickle.dump(combined_state, f)
    
# Laden des Sitzungszustands aus der Datei
loaded_state = load_session_state()
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Gruppe",
        "Bestehende Beziehung",
        "Auswirkung auf Interessen",
        "Level des Engagements",
        "Stakeholdergruppe",
        "Kommunikation",
        "Art der Betroffenheit",
        "Zeithorizont"
    ])

if 'df' in loaded_state:
    st.session_state.df = loaded_state['df']

def generate_stakeholder_ranking():
    score_table = st.session_state['namen_tabelle'][['Gruppe', 'Score']].copy()
    if not score_table.empty:
        score_table['Ranking'] = range(1, len(score_table) + 1)
        score_table = score_table.sort_values(by='Score', ascending=False).reset_index(drop=True)
        st.dataframe(score_table[['Ranking', 'Gruppe', 'Score']], 
                     column_config={"Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%f")}, 
                     hide_index=True, 
                     width=800)
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
    st.header("Stakeholder-Management")
    st.markdown("""
        Hier können Sie ihre Stakeholder effektiv verwalten und analysieren. Sie können relevante Informationen über verschiedene Stakeholdergruppen hinzufügen, bearbeiten und visualisieren. Die Daten helfen Ihnen, Strategien für den Umgang mit Ihren Stakeholdern zu entwickeln und zu priorisieren, basierend auf verschiedenen Kriterien wie Engagement-Level und Kommunikationshäufigkeit.          
    """)      
    tab1, tab2 = st.tabs(["Stakeholder Übersicht", "Stakeholder Ranking & Netzwerkdiagramm"])

    with tab1:
        # Initialize the session state for the DataFrame with an empty row if it does not exist
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame(columns=[
                "Gruppe",
                "Bestehende Beziehung",
                "Auswirkung auf Interessen",
                "Level des Engagements",
                "Stakeholdergruppe",
                "Kommunikation",
                "Art der Betroffenheit",
                "Zeithorizont"
            ])

        with st.sidebar:
            st.markdown("---")
            gruppe = st.text_input("Gruppe", '')
            bestehende_beziehung = st.selectbox("Bestehende Beziehung", ['', 'Ja', 'Nein'])
            auswirkung = st.selectbox("Auswirkung auf Interessen", ['', 'Hoch', 'Mittel', 'Niedrig'])
            level_des_engagements = st.selectbox("Level des Engagements", ['', 'Hoch', 'Mittel', 'Niedrig'])
            stakeholdergruppe = st.selectbox("Stakeholdergruppe", ['', 'Intern', 'Extern'])
            kommunikation = st.selectbox("Kommunikation", ['', 'Regelmäßig', 'Gelegentlich', 'Nie'])
            art_der_betroffenheit = st.selectbox("Art der Betroffenheit", ['', 'Direkt', 'Indirekt', 'Keine'])
            zeithorizont = st.selectbox("Zeithorizont", ['', 'Kurzfristig', 'Mittelfristig', 'Langfristig'])
            add_row = st.button('Hinzufügen')

        if st.session_state.df.empty:
            st.warning("Keine Daten vorhanden.")
            grid_response = None
        else:
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
                return_mode=DataReturnMode.FILTERED_AND_SORTED,
                selection_mode='multiple',
            )

        if grid_response:
            delete_rows = st.button('Zeile löschen')
            if delete_rows:
                selected_rows = grid_response['selected_rows']
                selected_indices = [row['index'] for row in selected_rows]
                st.session_state.df = st.session_state.df.drop(selected_indices)
                save_session_state({'df': st.session_state.df})
                st.experimental_rerun()

        new_row = {}
        if add_row:
            new_row = pd.DataFrame({
                "Gruppe": [gruppe],
                "Bestehende Beziehung": [bestehende_beziehung],
                "Auswirkung auf Interessen": [auswirkung],
                "Level des Engagements": [level_des_engagements],
                "Stakeholdergruppe": [stakeholdergruppe],
                "Kommunikation": [kommunikation],
                "Art der Betroffenheit": [art_der_betroffenheit],
                "Zeithorizont": [zeithorizont]
            })

        if add_row:
            # Prepend the new row to the DataFrame
            st.session_state.df = pd.concat([new_row, st.session_state.df]).reset_index(drop=True)
            save_session_state({'df': st.session_state.df})
            st.experimental_rerun()

    with tab2:
        col1, col2 = st.columns([1.5, 1.5])
        with col1:
            st.subheader("Ranking")
            if grid_response:
                df_temp = pd.DataFrame(grid_response['data'])
                df_temp['Score'] = df_temp.apply(calculate_score, axis=1)
                st.session_state['namen_tabelle'] = df_temp.sort_values(by='Score', ascending=False).reset_index(drop=True)
                generate_stakeholder_ranking()

        with col2:
            # CSS to increase space between columns
            spacing_css = """
            <style>
                .reportview-container .main .block-container {
                    margin: 10px;  # Adjust this value to increase/decrease space
                }
            </style>
            """
            
            # Apply the CSS
            st.markdown(spacing_css, unsafe_allow_html=True)
            st.subheader("Netzwerkdiagramm")
            net = Network(height="300px", width="100%", bgcolor="white", font_color="black")
            net.add_node("Mein Unternehmen", color="black", label="", title="")
            if 'namen_tabelle' in st.session_state:
                for _, row in st.session_state['namen_tabelle'].iterrows():
                    size = row['Score'] / 100 * 10 + 15
                    color = get_node_color(row['Score'])
                    net.add_node(row['Gruppe'], color=color, label=row['Gruppe'], title=row['Gruppe'], size=size)
                    net.add_edge("Mein Unternehmen", row['Gruppe'])
            net.save_graph("network.html")
            st.components.v1.html(open("network.html", "r").read(), height=600)

   


