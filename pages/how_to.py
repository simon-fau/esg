import streamlit as st
import os

def Platzhalter():
    """Creates empty lines for spacing in the Streamlit app."""
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

def allgemeine_informationen():
    """Displays general information about ESRS with sections and placeholders for spacing."""
    st.header("Allgemeine Informationen zu den ESRS")
    st.write("Hier finden Sie allgemeine Informationen zu den European Sustainability Reporting Standards (ESRS), darunter den Zweck, die Struktur und die Inhalte der ESRS. "
         "Zusätzlich finden Sie eine detaillierte Anleitung zum Ablauf der Wesentlichkeitsanalyse im Tab 'Anleitung zur Nutzung des ESG-Tools'.")
    Platzhalter()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, '..', 'Pictures', 'ESRS_Übersicht.png')

        # Bild anzeigen, wenn es vorhanden ist
        if os.path.exists(image_path):
            st.image(image_path, caption='Übersicht der ESRS Standards')
        else:
            st.error(f"Bilddatei {image_path} nicht gefunden.")
        Platzhalter()

    with st.expander("Ziel und Zweck der ESRS", expanded=False):
        st.write("""
        - **Standardisierung**: Die ESRS streben an, die Nachhaltigkeitsberichterstattung zu vereinheitlichen, 
          indem sie Unternehmen klare Richtlinien und Standards vorgeben. Dies soll die Vergleichbarkeit und 
          Konsistenz von Nachhaltigkeitsinformationen über verschiedene Unternehmen und Branchen hinweg erhöhen.
        - **Transparenz**: Die ESRS zielen darauf ab, die Transparenz zu steigern, indem sie Unternehmen verpflichten, 
          relevante und verlässliche datenbasierte Nachhaltigkeitsinformationen zu veröffentlichen. Diese Informationen 
          sollen Stakeholdern wie Investoren, Kunden und Mitarbeitern helfen, fundierte Entscheidungen über die 
          Nachhaltigkeitsleistung eines Unternehmens zu treffen.
        - **Relevanz**: Die ESRS verlangen von Unternehmen, dass sie über Nachhaltigkeitsthemen berichten, die für ihr 
          Geschäft und ihre Stakeholder von Bedeutung sind (sogenannte „doppelte Materialität“). Dies soll sicherstellen, 
          dass Unternehmen die Nachhaltigkeitsthemen mit dem größten Einfluss auf Umwelt und Gesellschaft priorisieren.
        - **Verbesserung**: Die ESRS sollen Unternehmen unterstützen, ihre Nachhaltigkeitsleistung zu steigern, indem sie 
          Anleitungen zu Best Practices und Anforderungen an die Berichterstattung bieten. Durch die Einhaltung der 
          ESRS-Richtlinien sollen Unternehmen Bereiche mit Verbesserungspotenzial identifizieren und Maßnahmen ergreifen, 
          um die ESG-Themen mit den größten Auswirkungen anzugehen.
        """)

    with st.expander("Struktur und Inhalte der ESRS", expanded=False):
        st.markdown("""
        Die European Sustainability Reporting Standards (ESRS) sind eine Reihe von Standards und Leitlinien, die entwickelt wurden, um die 
        Nachhaltigkeitsberichterstattung von Unternehmen in Europa zu harmonisieren und zu verbessern. 
        Diese Standards bieten einen Rahmen für die systematische Erfassung, Messung und Offenlegung von 
        Informationen zu Umwelt-, Sozial- und Governance-Aspekten (ESG) in Unternehmensberichten.
        """)

        st.markdown("""
        Die ESRS wurden entwickelt, um den gestiegenen Anforderungen an die Transparenz und Nachvollziehbarkeit von Nachhaltigkeitsberichten in der Europäischen Union gerecht zu werden. 
        Angesichts der globalen Herausforderungen des Klimawandels, der Ressourcenknappheit und sozialer Ungleichheiten war es notwendig, klare Richtlinien zu schaffen, die Unternehmen dazu verpflichten, ihre Auswirkungen auf Umwelt, Gesellschaft und Wirtschaft transparent darzulegen.
        Die ESRS wurden im Rahmen der Corporate Sustainability Reporting Directive (CSRD) ins Leben gerufen, um sicherzustellen, dass Nachhaltigkeitsinformationen vergleichbar, umfassend und verlässlich sind, und gleichzeitig die Erreichung der Klimaziele der EU zu unterstützen.
        Der Aufbau der ESRS besteht aus insgesamt 14 Standards, die in zwei Kategorien unterteilt sind: 12 themenspezifische Standards und 2 übergreifende Standards. Die themenspezifischen Standards decken Bereiche wie Umwelt, soziale Verantwortung und Governance ab. Dazu gehören Themen wie Klimawandel, Biodiversität oder auch die Lieferkette. 
        Die übergreifenden Standards legen allgemeine Anforderungen an den Berichterstattungsprozess fest, darunter die Struktur und Form der Berichte sowie Vorgaben zur Wesentlichkeitsanalyse, die Unternehmen dabei unterstützt, die für sie relevanten Nachhaltigkeitsthemen zu identifizieren.
        """)
        

def anleitung_zur_nutzung():
    st.header("Durchführung der Wesentlichkeitsanalyse")
    
    with st.expander("1. Stakeholder Management", expanded=False):
        st.write("""
            Fügen Sie hier all Ihre Stakeholder hinzu und verwalten diese. Hierfür können Sie die Stakeholder über die Sidebar hinzufügen und diesen Eigenschaften zuweisen. 
            Auf Basis der Eigenschaften wird ein Stakeholder-Rating erstellt, welches Ihnen bei der Auswahl der Stakeholder für die Wesentlichkeitsanalyse hilft.
        """)

    with st.expander("2. Stakeholder Auswahl", expanded=False):
        st.write("""
            In diesem Schritt werden die Stakeholder ausgewählt, die im Rahmen der Wesentlichkeitsanalyse berücksichtigt werden sollen.
        """)

    with st.expander("3. Themenspezifische ESRS", expanded=False):
        st.write("""
            Dieser Schritt ist nicht offiziell in den ESRS vorgeschrieben. Er dient der Vorauswahl potenziell wesentlicher IROs basierend auf den Themenbereichen der themenspezifischen ESRS. Punkte, die hier als relevant gekennzeichnet werden, werden in einem späteren Schritt bewertet.
        """)

    with st.expander("4. Interne Nachhaltigkeitspunkte", expanded=False):
        st.write("""
            Hier können Sie Ihre eigenen internen Nachhaltigkeitspunkte hinzufügen, die nicht in den themenspezifischen ESRS enthalten sind. Aktualisieren Sie anschließend die Excel-Datei und laden Sie diese herunter. Diese Datei soll dann an die Stakeholder versendet werden, die Sie in Schritt 2 ausgewählt haben.
            Die Excel-Datei wird automatisch generiert und enthält sowohl die IROs aus Schritt 4 der internen Untersuchung als auch die Punkte der themenspezifischen ESRS. 
            Zudem haben die Stakeholder die Möglichkeit, eigene IROs, die noch nicht abgedeckt sind, hinzuzufügen. 
            Wichtig ist, dass die Stakeholder die vollständige Liste der themenspezifischen ESRS erhalten, nicht die vorsortierte aus Schritt 1. 
            Alle diese Punkte werden anschließend von den Stakeholdern auf einer Skala von 4 Stufen bewertet.
        """)

    with st.expander("5. Externe Nachhaltigkeitspunkte", expanded=False):
        st.write("""
            Diese Seite ist dafür da, die bewerteten Excel-Dateien der Stakeholer hochzuladen. Dabei werden die Ergebnisse aller Stakeholder in einer Tabelle kumuliert daregstellt. Dabei können Sie hier auch Stakeholder und deren Bewertungen wieder entfernen.
        """)

    with st.expander("6. Bewertung der Longlist", expanded=False):
        st.write("""
            Hier befinden sich alle potenziellen IROs aus Schritt 3, 4 und 5. Die Bewertung erfolgt anhand der auswirkungsbezogenen und der finanziellen Wesentlichkeit,
            wobei das Minimum für jede Wesentlichkeitsdimension der Wert 0 ist und das Maximum 1000.
        """)

    with st.expander("7. Erstellung der Shortlist", expanded=False):
        st.write("""
            Hier werden alle bewerteten IROs in einer Wesentlichkeitsmatrix angezeigt. Das Unternehmen legt sowohl einen Schwellenwert für die Wesentlichkeit fest,
            als auch für die Stakeholder-Wichtigkeit. Punkte, die eine der beiden Grenzen überschreiten, gelten als wesentlich und werden in die Shortlist übernommen.
            Die Shortlist enthält alle wesentlichen IROs, die das Unternehmen im Rahmen der Wesentlichkeitsanalyse identifiziert hat.
        """)

def display_page():
    
    tab1, tab2 = st.tabs(["Allgemeine Informationen", "Anleitung zur Nutzung des ESG-Tools"])
    with tab1:
        allgemeine_informationen()
    with tab2:
        anleitung_zur_nutzung()


