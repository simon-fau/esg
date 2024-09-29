import streamlit as st

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
    Platzhalter() 
    st.markdown("""
        ESRS sind eine Reihe von Standards und Leitlinien, die entwickelt wurden, um die 
        Nachhaltigkeitsberichterstattung von Unternehmen in Europa zu harmonisieren und zu verbessern. 
        Diese Standards bieten einen Rahmen für die systematische Erfassung, Messung und Offenlegung von 
        Informationen zu Umwelt-, Sozial- und Governance-Aspekten (ESG) in Unternehmensberichten.
    """)
    st.markdown("""
        Die Entstehung der ESRS ist auf die wachsende Bedeutung der Nachhaltigkeitsberichterstattung für 
        Unternehmen und deren Stakeholder zurückzuführen. Investoren, Kunden und die Gesellschaft erwarten 
        zunehmend, dass Unternehmen nicht nur finanzielle Kennzahlen, sondern auch ihre Auswirkungen auf 
        Umwelt und Gesellschaft offenlegen. Zur Förderung einer einheitlichen und vergleichbaren 
        Nachhaltigkeitsberichterstattung in Europa wurde die ESRS-Initiative ins Leben gerufen. Diese 
        Initiative umfasst eine breite Palette von Interessengruppen, darunter Unternehmen, Investoren, 
        Regulierungsbehörden und NGOs, die gemeinsam daran arbeiten, transparente und verlässliche Standards 
        für die Berichterstattung zu entwickeln.
    """)
    Platzhalter()
    Platzhalter()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:  
        st.image('Pictures/ESRS_Übersicht.png', caption='Übersicht der ESRS Standards')
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
        st.write("""
            Der aktuelle Entwurf der ESRS besteht aus allgemeinen Standards und themenspezifischen Standards, 
            die für alle Industrien relevant sind. Die allgemeinen Standards definieren die grundlegenden 
            Anforderungen für die Nachhaltigkeitsberichterstattung, während die themenspezifischen Standards 
            spezifische Nachhaltigkeitsthemen wie Klima, Biodiversität und Arbeitsbedingungen entlang der 
            Wertschöpfungskette abdecken. Es gibt zwei zentrale Standards innerhalb der ESRS, die Unternehmen 
            bei ihrer Nachhaltigkeitsberichterstattung leiten. Der ESRS 1 Standard Set 1 umfasst allgemeine 
            Prinzipien und Richtlinien. Der ESRS 2 Standard, der sich mit Allgemeinen Offenlegungspflichten zu 
            Strategie, Unternehmensführung und Materialitätsbewertung befasst, ist speziell für Unternehmen mit 
            mehr als 250 Mitarbeitern verpflichtend.
        """)
        st.write("""
            Die zehn thematischen ESRS-Standards, die von E1 bis G1 reichen, sind grundsätzlich optional. Unternehmen 
            müssen jedoch im Rahmen einer verpflichtenden Wesentlichkeitsanalyse prüfen, ob die Inhalte relevant sind. 
            Wenn ein Thema wie der Klimawandel als „nicht wesentlich“ betrachtet wird, muss dies ausführlich begründet 
            werden. Andere Themen, die als „nicht wesentlich“ eingestuft werden, dürfen nicht einfach ignoriert werden, 
            sondern müssen ausdrücklich als solche gekennzeichnet werden.
        """)

def anleitung_zur_nutzung():
    
    st.header("1. Wesentlichkeitsanalyse durchführen")
    st.write("Der erste Schritt in der App ist die Durchführung der Wesentlichkeitsanalyse. Hierbei können Sie über die Sidebar auf die unterschiedlichen Prozessschritte zugreifen.")

    st.subheader("1. Stakeholdermanagement")
    st.write("""
    In diesem Schritt können Sie verschiedene interne und externe Stakeholder hinzufügen.
    Basierend auf Ihren Auswahlen wird ein Ranking erstellt, welches die Relevanz der Stakeholder darstellt.
    Gehen Sie dabei wie folgt vor:
    1. Öffnen Sie die Sidebar und wählen Sie den Prozessschritt 'Stakeholdermanagement' aus.
    2. Fügen Sie Stakeholder hinzu, indem Sie in der Sidebar einen Stakeholder eintragen und anschließend Eigenschaften über die Slectbox auswaählen.
    3. Basierend auf den hinzugefügten Stakeholdern wird automatisch ein Relevanz-Ranking erstellt.
    """)

    st.subheader("2. Themenspezifische ESRS")
    st.write("""
    Im nächsten Schritt gilt es, eine erste Auswahl relevanter Themen vorzunehmen. Die dargestellten Themen decken Inhalte der ESRS E1 bis G1 ab.
    Dabei müssen Entscheidungen hinsichtlich der Wesentlichkeit dieser Themen getroffen werden. Ein Nachhaltigkeitspunkt wird als wesentlich erachtet, wenn er eine positive oder negative Auswirkung hat oder finanzielle Auswirkungen zur Folge hat.
    Nachhaltigkeitspunkte, die als wesentlich oder eher wesentlich eingestuft werden, werden in die spätere Bewertung aufgenommen.
    """)

    st.subheader("3. Interne Nachhaltigkeitspunkte")
    st.write("""       
    In diesem Schritt können Sie eigene Nachhaltigkeitspunkte, sogenannte "interne Nachhaltigkeitspunkte", hinzufügen. Erstellen Sie dazu eine Liste potenziell wesentlicher Nachhaltigkeitsthemen, basierend auf den IROs. Diese Themen sollen auf einer detaillierten Ebene identifiziert und anschließend in übergeordnete Themen oder Unterthemen gruppiert werden.

    Gehen Sie dabei wie folgt vor:

    - Wenn Sie Inhalte hinzufügen möchten, die sich einem Thema oder Unterthema der themenspezifischen ESRS-Punkte unterordnen lassen, verwenden Sie die Sidebar.
    - Wenn Sie eigene Themen, Unterthemen und Unter-Unterthemen erstellen möchten, können Sie dies direkt in der Tabelle tun. Bei Änderungen innerhalb der Tabelle, klicken Sie auf den Button "Speichern", um die Änderungen zu übernehmen.

    Sobald Sie die Liste erstellt haben, drücken Sie auf den Button "Excel aktualisieren" und anschließend auf "Excel herunterladen".
        """)
        

def display_page():
    """Displays the main page with tabs for general information and usage instructions."""
    tab1, tab2 = st.tabs(["Allgemeine Informationen", "Anleitung zur Nutzung des ESRS-Tools"])
    with tab1:
        allgemeine_informationen()
    with tab2:
        anleitung_zur_nutzung()


