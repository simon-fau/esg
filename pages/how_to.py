import streamlit as st

def Einführung():
    st.title("How to use the ESRS-Tool")
    st.write("Die Software wurde entwickelt, um die Erstellung eines ESRS-Berichts zu erleichtern.")

def allgemeine_informationen():
    with st.expander("Allgemeine Informationen zur ESRS", expanded=False):
        st.header("Was sind ESRS?")
        st.write("ESRS sind eine Reihe von Standards und Leitlinien, die entwickelt wurden, um die Nachhaltigkeitsberichterstattung von Unternehmen in Europa zu harmonisieren und zu verbessern. Diese Standards bieten einen Rahmen für die systematische Erfassung, Messung und Offenlegung von Informationen zu Umwelt-, Sozial- und Governance-Aspekten (ESG) in Unternehmensberichten.")
        st.write("Die Entstehung der ESRS ist auf die wachsende Bedeutung der Nachhaltigkeitsberichterstattung für Unternehmen und deren Stakeholder zurückzuführen. Investoren, Kunden und die Gesellschaft erwarten zunehmend, dass Unternehmen nicht nur finanzielle Kennzahlen, sondern auch ihre Auswirkungen auf Umwelt und Gesellschaft offenlegen. Zur Förderung einer einheitlichen und vergleichbaren Nachhaltigkeitsberichterstattung in Europa wurde die ESRS-Initiative ins Leben gerufen. Diese Initiative umfasst eine breite Palette von Interessengruppen, darunter Unternehmen, Investoren, Regulierungsbehörden und NGOs, die gemeinsam daran arbeiten, transparente und verlässliche Standards für die Berichterstattung zu entwickeln.")
        st.header("Ziel und Zweck")
        st.write("""
        - **Standardisierung**: Die ESRS streben an, die Nachhaltigkeitsberichterstattung zu vereinheitlichen, indem sie Unternehmen klare Richtlinien und Standards vorgeben. Dies soll die Vergleichbarkeit und Konsistenz von Nachhaltigkeitsinformationen über verschiedene Unternehmen und Branchen hinweg erhöhen.
        - **Transparenz**: Die ESRS zielen darauf ab, die Transparenz zu steigern, indem sie Unternehmen verpflichten, relevante und verlässliche datenbasierte Nachhaltigkeitsinformationen zu veröffentlichen. Diese Informationen sollen Stakeholdern wie Investoren, Kunden und Mitarbeitern helfen, fundierte Entscheidungen über die Nachhaltigkeitsleistung eines Unternehmens zu treffen.
        - **Relevanz**: Die ESRS verlangen von Unternehmen, dass sie über Nachhaltigkeitsthemen berichten, die für ihr Geschäft und ihre Stakeholder von Bedeutung sind (sogenannte „doppelte Materialität“). Dies soll sicherstellen, dass Unternehmen die Nachhaltigkeitsthemen mit dem größten Einfluss auf Umwelt und Gesellschaft priorisieren.
        - **Verbesserung**: Die ESRS sollen Unternehmen unterstützen, ihre Nachhaltigkeitsleistung zu steigern, indem sie Anleitungen zu Best Practices und Anforderungen an die Berichterstattung bieten. Durch die Einhaltung der ESRS-Richtlinien sollen Unternehmen Bereiche mit Verbesserungspotenzial identifizieren und Maßnahmen ergreifen, um die ESG-Themen mit den größten Auswirkungen anzugehen.
        """)
        st.header("Struktur und Inhalte")
        st.write("Der aktuelle Entwurf der ESRS besteht aus allgemeinen Standards und themenspezifischen Standards, die für alle Industrien relevant sind. Die allgemeinen Standards definieren die grundlegenden Anforderungen für die Nachhaltigkeitsberichterstattung, während die themenspezifischen Standards spezifische Nachhaltigkeitsthemen wie Klima, Biodiversität und Arbeitsbedingungen entlang der Wertschöpfungskette abdecken. Es gibt zwei zentrale Standards innerhalb der ESRS, die Unternehmen bei ihrer Nachhaltigkeitsberichterstattung leiten. Der ESRS 1 Standard Set 1 umfasst allgemeine Prinzipien und Richtlinien. Der ESRS 2 Standard, der sich mit Allgemeinen Offenlegungspflichten zu Strategie, Unternehmensführung und Materialitätsbewertung befasst, ist speziell für Unternehmen mit mehr als 250 Mitarbeitern verpflichtend.")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")  # Fügt eine leere Zeile für zusätzlichen Abstand ein
        st.image('ESRS_Übersicht.png', caption='Übersicht der ESRS Standards',)
        st.write("\n")  # Fügt eine leere Zeile für zusätzlichen Abstand ein
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("Die zehn thematischen ESRS-Standards, die von E1 bis G1 reichen, sind grundsätzlich optional. Unternehmen müssen jedoch im Rahmen einer verpflichtenden Wesentlichkeitsanalyse prüfen, ob die Inhalte relevant sind. Wenn ein Thema wie der Klimawandel als „nicht wesentlich“ betrachtet wird, muss dies ausführlich begründet werden. Andere Themen, die als „nicht wesentlich“ eingestuft werden, dürfen nicht einfach ignoriert werden, sondern müssen ausdrücklich als solche gekennzeichnet werden.")

def display_page():
    Einführung()
    allgemeine_informationen()
    
    
    