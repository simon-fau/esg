import streamlit as st
from pages.Stakeholder_Management import display_stakeholder_ranking_and_network
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import merge_dataframes, bewertung_Uebersicht
import plotly.express as px
import plotly.graph_objects as go

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

def auswirkungsbezogene_graphik():
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        df = st.session_state.selected_columns

        # Farbcodierung basierend auf der Untersuchung der Zeichenkette in "Score Auswirkung"
        def determine_color(impact):
            if 'Positive Auswirkung' in impact:
                return 'Positive Auswirkung'
            elif 'Negative Auswirkung' in impact:
                return 'Negative Auswirkung'
            else:
                return 'Neutral'

        df['color'] = df['Auswirkung'].apply(determine_color)

        # Berechnung der Stakeholder Wichtigkeit
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew.'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew.'].max()
        df['Stakeholder Wichtigkeit'] = ((df['Stakeholder Gesamtbew.'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        df['Stakeholder Wichtigkeit'] = df['Stakeholder Wichtigkeit'].fillna(100)

        # Erstellen der Scatter-Graphik
        fig = px.scatter(df, x='Score Finanzen', y='Score Auswirkung', color='color',
                         size='Stakeholder Wichtigkeit',  # Größe der Punkte basierend auf Stakeholder Wichtigkeit
                         color_discrete_map={'Positive Auswirkung': 'green', 'Negative Auswirkung': 'red', 'Neutral': 'grey'},
                         labels={'Score Finanzen': 'Score Finanzen', 'Score Auswirkung': 'Score Auswirkung'},
                         title='Auswirkungsbezogene Grafik',
                         range_x=[0, 1000],  # X-Achsenbereich von 0 bis 1000
                         range_y=[0, 1000],  # Y-Achsenbereich von 0 bis 1000
                         width=1000,  # Breite des Charts
                         height=800,  # Höhe des Charts
                         hover_data={
                             'Thema': True,
                             'Unterthema': True,
                             'Unter-Unterthema': True,
                             'Score Auswirkung': True,
                             'Score Finanzen': True,
                             'Stakeholder Wichtigkeit': True,
                             'color': False  # Verhindert das Anzeigen der Farbe im Tooltip
                         })

        # Hinzufügen des Rasters und Festlegen der Achsenintervalle
        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=100,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=1,
                griddash='dash',
                zeroline=True,
                layer='above traces',
                side='bottom'
            ),
            xaxis2=dict(
                tickmode='linear',
                tick0=0,
                dtick=100,
                showgrid=False,
                zeroline=True,
                overlaying='x',
                side='top'
            ),
            yaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=100,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=1,
                griddash='dash',
                zeroline=True,
                layer='above traces'
            ),
            legend_title_text='Auswirkungen',
            staticPlot=True  # Disable interactivity
        )

        # Hinzufügen zusätzlicher Rasterlinien alle 50 Einheiten
        fig.update_xaxes(showline=True, gridwidth=1, gridcolor='lightgrey', tick0=0, dtick=100)
        fig.update_yaxes(showline=True, gridwidth=1, gridcolor='lightgrey', tick0=0, dtick=100)

        # Regler zum Bewegen der Linie hinzufügen
        line_position = st.slider('Linienposition', min_value=0, max_value=1000, value=400, step=10)
        
        fig.add_trace(go.Scatter(x=[0, line_position], y=[line_position, 0], mode='lines', name='Grenzlinie Stakeholder Wichtigkeit', line=dict(color='red')))

        st.plotly_chart(fig, use_container_width=True)

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
        st.write("Selected Columns:", st.session_state.get('selected_columns', 'Keine Spalten ausgewählt'))
        auswirkungsbezogene_graphik()
        