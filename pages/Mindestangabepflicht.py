import streamlit as st
import pandas as pd
import pickle
import os

# Datei zum Speichern des Sitzungszustands
state_file = 'session_state_mdr.pkl'

# Funktion zum Laden des Sitzungszustands
def load_session_state():
    if os.path.exists(state_file):
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

# Laden des Sitzungszustands aus der Datei
loaded_state = load_session_state()
st.session_state.update(loaded_state)

def create_mdr_table():
    # Daten für die Tabelle erstellen
    data_mdr = {
        "Referenz": [
            "ESRS MDR-P §65a", "ESRS MDR-P §65b", "ESRS MDR-A §68b", "ESRS MDR-A §68d",
            "ESRS MDR-A §69b", "ESRS MDR-A §69b", "ESRS MDR-A §69c", "ESRS MDR-A §69c",
            "ESRS MDR-M §75", "ESRS MDR-T §80"
        ],
        "Beschreibung": [
            "Beschreibung der wichtigsten Inhalte der Strategie, einschließlich ihrer allgemeinen Ziele, und der wesentlichen Auswirkungen, Risiken oder Chancen, auf die sich die Strategie bezieht, sowie des Überwachungsprozesses",
            "eine Beschreibung des Anwendungsbereichs der Strategie (oder der Ausnahmen) in Bezug auf Aktivitäten, die vor- und/oder nachgelagerte Wertschöpfungskette, geografische Gebiete und gegebenenfalls betroffene Interessengruppen",
            "Beschreibung des Umfangs der wichtigsten Maßnahmen in Bezug auf Aktivitäten, die Geografie der vor- und/oder nachgelagerten Wertschöpfungskette und gegebenenfalls betroffene Interessengruppen",
            "die wichtigsten Maßnahmen (zusammen mit ihren Ergebnissen), die ergriffen wurden, um Abhilfe für diejenigen zu schaffen, die durch tatsächliche wesentliche Auswirkungen geschädigt wurden",
            "Aktuelle, dem Aktionsplan zugewiesene Finanzmittel (CapEx)",
            "Aktuelle, dem Aktionsplan zugewiesene Finanzmittel (OpEx)",
            "Betrag der künftig, dem Aktionsplan zugewiesenen finanziellen Mittel (CapEx)",
            "Betrag der künftig, dem Aktionsplan zugewiesenen finanziellen Mittel (OpEx)",
            "Das Unternehmen gibt alle Parameter an, die es verwendet, um die Leistung und Wirksamkeit in Bezug auf wesentliche Auswirkungen, Risiken oder Chancen zu beurteilen",
            "Das Unternehmen muss die messbaren, ergebnisorientierten und terminierten Ziele in Bezug auf wesentliche Nachhaltigkeitsaspekte angeben, die es zur Bewertung der Fortschritte festgelegt hat. Für jedes Ziel enthält die Angabe folgende Informationen:"
        ]
    }

    # DataFrame erstellen
    df_mdr = pd.DataFrame(data_mdr)
    if "Antworten" not in st.session_state:
        st.session_state["Antworten"] = [""] * len(df_mdr)
    df_mdr["Antworten"] = st.session_state["Antworten"]  # Spalte für Antworten hinzufügen
    return df_mdr

def add_entries(df_mdr):
    # Tabelle anzeigen
    for i in range(len(df_mdr)):
        antwort = st.text_area(f"{df_mdr['Referenz'][i]} - {df_mdr['Beschreibung'][i]}", 
                               key=f"answer_mdr_{i}", value=st.session_state["Antworten"][i])
        st.session_state["Antworten"][i] = antwort

def display_page():
    df_mdr = create_mdr_table()
    st.title("Mindestangaben ESRS MDR")
    
    tab1, tab2 = st.tabs(["Inhalte hinzufügen", "Übersicht"])
    
    with tab1:
        add_entries(df_mdr)
    
    with tab2:
        st.title("Übersicht")
        df_mdr["Antworten"] = st.session_state["Antworten"]
        st.table(df_mdr)










def chart_Übersicht():

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Prepare the data
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]
        required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']

        # Check if the DataFrame is empty after filtering
        if selected_columns_df.empty:
            st.warning("Keine Daten vorhanden, um den Chart anzuzeigen.")
            return  # Stop the function execution

        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'

        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew.'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew.'].max()
        selected_columns['Stakeholder Wichtigkeit'] = ((selected_columns['Stakeholder Gesamtbew.'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        selected_columns['Stakeholder Wichtigkeit'] = selected_columns['Stakeholder Wichtigkeit'].fillna(100)

        # Base scatter chart
        scatter = alt.Chart(selected_columns, width=1000, height=800).mark_circle().encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Environmental', 'Social', 'Governance', 'Sonstige'],
                range=['green', 'yellow', 'blue', 'gray']
            ), legend=alt.Legend(
                title="Thema",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Environmental', 'Social', 'Governance', 'Sonstige']
            )),
            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=required_columns
        )

        # Line
        intersection_value = st.session_state.get('intersection_value', 500)  # Default value if not set in session state
        line = alt.Chart(pd.DataFrame({
            'x': [0, intersection_value],
            'y': [intersection_value, 0]
        })).mark_line(color='red').encode(
            x='x:Q',
            y='y:Q'
        )

        # Area to the left of the line
        area = alt.Chart(pd.DataFrame({
            'x': [0, 0, intersection_value],
            'y': [0, intersection_value, 0]
        })).mark_area(opacity=0.3, color='lightcoral').encode(
            x='x:Q',
            y='y:Q'
        )

        chart = area + scatter + line

        st.altair_chart(chart)
    else:
        st.warning("Keine Daten ausgewählt.")