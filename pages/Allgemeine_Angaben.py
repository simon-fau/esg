import streamlit as st
import pandas as pd

def Tabelle():
    # Daten für die Tabelle erstellen
    data = {
        "Referenz": [
            "ESRS 2 BP-1 §5a", "ESRS 2 BP-1 §5b i", "ESRS 2 BP-1 §5b ii", "ESRS 2 BP-1 §5c",
            "ESRS 2 GOV-4 §30; §32", "ESRS 2 GOV-5 §36a", "ESRS 2 GOV-5 §36b", "ESRS 2 GOV-5 §36c",
            "ESRS 2 GOV-5 §36d", "ESRS 2 SBM-1 §40a i", "ESRS 2 SBM-1 §40a iii", "ESRS 2 SBM-1 §40b",
            "ESRS 2 SBM-1 §40d i", "ESRS 2 SBM-1 §40e", "ESRS 2 SBM-1 §42", "ESRS 2 SBM-1 §42a",
            "ESRS 2 SBM-1 §42b", "ESRS 2 SBM-1 §42c", "ESRS 2 SBM-3 §48a", "ESRS 2 SBM-3 §48b",
            "ESRS 2 SBM-3 §48c i", "ESRS 2 SBM-3 §48c ii", "ESRS 2 SBM-3 §48c iii", "ESRS 2 SBM-3 §48c iv",
            "ESRS 2 SBM-3 §48d", "ESRS 2 SBM-3 §48e", "ESRS 2 SBM-3 §48f", "ESRS 2 SBM-3 §48g", "ESRS 2 SBM-3 §48h"
        ],
        "Beschreibung": [
            "Das Unternehmen gibt an, ob die Nachhaltigkeitserklärung auf konsolidierter oder auf individueller Basis erstellt wurde",
            "Das Unternehmen gibt für die konsolidierte Nachhaltigkeitsberichterstattung an, ob eine Bestätigung, dass der Konsolidierungskreis der gleiche wie für die Jahresabschlüsse ist, oder gegebenenfalls eine Erklärung, dass das Bericht erstattende Unternehmen keinen Jahresabschluss erstellen muss oder dass das Bericht erstattende Unternehmen eine konsolidierte Nachhaltigkeitsberichterstattung gemäß Artikel 48i der Richtlinie 2013/34/EU erstellt",
            "Das Unternehmen gibt für die konsolidierte Nachhaltigkeitsberichterstattung an, ob gegebenenfalls, welche in die Konsolidierung einbezogenen Tochterunternehmen gemäß Artikel 19a Absatz 9 oder Artikel 29a Absatz 8 der Richtlinie 2013/34/EU von der jährlichen oder konsolidierten Nachhaltigkeitsberichterstattung ausgenommen sind",
            "Das Unternehmen gibt an inwieweit die Nachhaltigkeitserklärung die vor- und nachgelagerte Wertschöpfungskette des Unternehmens abdeckt (siehe ESRS 1 Abschnitt 5.1 Bericht erstattendes Unternehmen und Wertschöpfungskette)",
            "Das Unternehmen hat eine Übersicht über die in seiner Nachhaltigkeitserklärung bereitgestellten Informationen über das Verfahren zur Erfüllung der Sorgfaltspflicht anzugeben.",
            "Beschreibung des Umfangs, der Hauptmerkmale und Komponenten der Risikomanagement- und internen Kontrollprozesse und -systeme in Bezug auf die Nachhaltigkeitsberichterstattung",
            "Beschreibung verwendeten Ansatz zur Risikobewertung, einschließlich der Methode zur Priorisierung von Risiken",
            "Angabe der wichtigsten ermittelten Risiken und die Minderungsstrategien, einschließlich damit verbundener Kontrollen",
            "Beschreibung, wie das Unternehmen die Ergebnisse seiner Risikobewertung und seiner internen Kontrollen in Bezug auf das Verfahren der Nachhaltigkeitsberichterstattung in die einschlägigen internen Funktionen und Prozesse einbindet",
            "Beschreibung wesentlicher Gruppen von angebotenen Produkten und (oder) Dienstleistungen",
            "Angabe der Zahl der Beschäftigten nach geografischen Gebieten",
            "Aufschlüsselung der Gesamteinnahmen, wie sie im Jahresabschluss angegeben wurden, nach den maßgeblichen ESRS-Sektoren. Enthält der Jahresabschluss des Unternehmens Segmentberichterstattung nach dem IFRS 8 Geschäftssegmente, werden diese Informationen über die Umsatzerlöse des Sektors so weit wie möglich mit den Angaben gemäß IFRS 8 abgeglichen",
            "Einnahmen aus Taxonomie-konformen Wirtschaftsaktivitäten im Zusammenhang mit fossilem Gas",
            "Beschreibung nachhaltigkeitsbezogener Ziele im Hinblick auf wesentliche Produkt- und Dienstleistungsgruppen, Kundenkategorien, geografische Gebiete und Beziehungen zu Stakeholdern",
            "Beschreibung des Geschäftsmodells und der Wertschöpfungskette",
            "Beschreibung der Inputs und Vorgehensweise beim Sammeln, Erarbeiten und Sichern von Inputs",
            "Beschreibung der Leistungen und Ergebnisse im Hinblick auf aktuelle und erwartete Vorteile für Kunden, Investoren und andere Stakeholder",
            "Beschreibung der wichtigsten Merkmale seiner vor- und nachgelagerten Wertschöpfungskette und der Position des Unternehmens in seiner Wertschöpfungskette, einschließlich einer Beschreibung der wichtigsten Wirtschaftsakteure (wie wichtige Lieferanten, Vertriebskanäle und Endnutzer) und ihrer Beziehung zum Unternehmen. Verfügt das Unternehmen über mehrere Wertschöpfungsketten, erstreckt sich die Angabepflicht auf die wichtigsten Wertschöpfungsketten.",
            "Angabe einer kurzen Erläuterung seiner wesentlichen Auswirkungen, Risiken und Chancen, die sich aus seiner Bewertung der Wesentlichkeit ergeben (siehe Angabepflicht IRO-1 dieses Standards), einschließlich einer Beschreibung, wo in seinem Geschäftsmodell, seinen eigenen Tätigkeiten und seiner vor- und nachgelagerten Wertschöpfungskette diese wesentlichen Auswirkungen, Risiken und Chancen konzentriert sind",
            "Angabe über den derzeitigen und erwarteten Einfluss seiner wesentlichen Auswirkungen, Risiken und Chancen auf sein Geschäftsmodell, seine Wertschöpfungskette, seine Strategie und seine Entscheidungsfindung sowie die Art und Weise, wie es auf diesen Einfluss reagiert hat oder zu reagieren beabsichtigt, einschließlich aller Änderungen, die es im Rahmen seiner Maßnahmen zum Umgang mit bestimmten wesentlichen Auswirkungen oder Risiken oder zur Nutzung bestimmter wesentlicher Chancen an seiner Strategie oder seinem Geschäftsmodell vorgenommen hat oder vorzunehmen beabsichtigt",
            "Angabe wie die wesentlichen negativen und positiven Auswirkungen des Unternehmens sich auf Menschen oder die Umwelt auswirken (oder im Falle potenzieller Auswirkungen, wie sie sich wahrscheinlich auswirken)",
            "Angabe ob und wie die Auswirkungen von der Strategie und dem Geschäftsmodell des Unternehmens ausgehen oder damit in Verbindung stehen",
            "Angabe welche Zeithorizonte für die Auswirkungen vernünftigerweise zu erwarten sind",
            "Angabe ob das Unternehmen durch seine Tätigkeiten oder aufgrund seiner Geschäftsbeziehungen einen Anteil an den wesentlichen Auswirkungen hat, mit einer Beschreibung der Art der betreffenden Tätigkeiten oder Geschäftsbeziehungen",
            "Offenlegung der aktuellen finanziellen Auswirkungen wesentlicher Risiken und Chancen auf die Finanzlage, die Finanzleistung und die Cashflows sowie wesentliche Risiken und Chancen, bei denen ein erhebliches Risiko einer wesentlichen Anpassung der Buchwerte der in den entsprechenden Abschlüssen ausgewiesenen Vermögenswerte und Verbindlichkeiten innerhalb der nächsten jährlichen Berichtsperiode besteht",
            "Offenlegung der erwarteten finanziellen Auswirkungen wesentlicher Risiken und Chancen auf die Finanzlage, die Finanzleistung und die Cashflows kurz-, mittel- und langfristig",
            "Informationen zur Widerstandsfähigkeit der Strategie und des Geschäftsmodells hinsichtlich der Fähigkeit, wesentliche Auswirkungen und Risiken zu bewältigen und wesentliche Chancen zu nutzen",
            "Angabe der Änderungen der wesentlichen Auswirkungen, Risiken und Chancen im Vergleich zum vorangegangenen Berichtszeitraum",
            "eine genaue Beschreibung der Auswirkungen, Risiken und Chancen, die unter die Angabepflichten des ESRS fallen, im Gegensatz zu den Auswirkungen, die von dem Unternehmen durch zusätzliche unternehmensspezifische Angaben abgedeckt werden"
        ]
    }

# DataFrame erstellen
    df = pd.DataFrame(data)
    if "Antworten" not in st.session_state:
        st.session_state["Antworten"] = [""] * len(df)
    df["Antworten"] = st.session_state["Antworten"]  # Spalte für Antworten hinzufügen
    return df

def add_entries(df):
    # Tabelle anzeigen
    for i in range(len(df)):
        antwort = st.text_area(f"{df['Referenz'][i]} - {df['Beschreibung'][i]}", 
                               key=f"answer_mdr_{i}", value=st.session_state["Antworten"][i])
        st.session_state["Antworten"][i] = antwort

def display_page():
    df = Tabelle()
    st.title("Mindestangaben ESRS MDR")
    
    tab1, tab2 = st.tabs(["Inhalte hinzufügen", "Übersicht"])
    
    with tab1:
        add_entries(df)
    
    with tab2:
        st.title("Übersicht")
        df["Antworten"] = st.session_state["Antworten"]
        st.table(df)


