import streamlit as st
import pandas as pd

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







