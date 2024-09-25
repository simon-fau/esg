import streamlit as st
import pandas as pd
import pickle
import os

# Datei zum Speichern des Sitzungszustands
state_file = 'SessionStates.pkl'

# Funktion zum Speichern des Zustands
def save_state():
    with open('SessionStates.pkl', 'wb') as f:
        pickle.dump(dict(st.session_state), f)

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
    if "Antworten_MDR" not in st.session_state:
        st.session_state["Antworten_MDR"] = [""] * len(df_mdr)
    df_mdr["Antworten_MDR"] = st.session_state["Antworten_MDR"]  # Spalte für Antworten_MDR hinzufügen
    return df_mdr

# Funktion zur Aktualisierung der Antworten_MDR
def update_answers(i):
    st.session_state["Antworten_MDR"][i] = st.session_state[f"answer_mdr_{i}"]
    save_state()  # Speichern des Zustands nach jeder Änderung

def add_entries(df_mdr):
    # Tabelle anzeigen
    for i in range(len(df_mdr)):
        st.text_area(
            f"{df_mdr['Referenz'][i]} - {df_mdr['Beschreibung'][i]}",
            key=f"answer_mdr_{i}",
            value=st.session_state["Antworten_MDR"][i],
            on_change=update_answers,
            args=(i,)
        )

def display_page():
    df_mdr = create_mdr_table()
    st.title("Mindestangaben- Raus rahmen?")

    tab1, tab2 = st.tabs(["Inhalte hinzufügen", "Übersicht"])

    with tab1:
        add_entries(df_mdr)

    with tab2:
        if not any(st.session_state["Antworten_MDR"]):
            st.info("Noch keine Einträge vorhanden.")
        else:
            df_mdr["Antworten_MDR"] = st.session_state["Antworten_MDR"]
            st.table(df_mdr)


    save_state()  # Sicherstellen, dass der Zustand am Ende gespeichert wird