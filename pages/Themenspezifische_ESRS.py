import streamlit as st
import pickle
import pandas as pd
import os

# Diese Funktion zeigt eine Markdown-Anleitung zur Bewertung der Relevanz von Themen.
def Text():
    st.markdown("""
        Bitte bewerten Sie die Themengebiete anhand ihrer Relevanz für Ihr Unternehmen. Dabei gilt folgende Definition für die verschiedenen Auswahlmöglichkeiten:
        - **Relevant**:  Ein Merkmal ist relevant, wenn es im Rahmen der doppelten Wesentlichkeit eine bedeutende Rolle für die Entscheidungen der Nutzer spielen kann. Dies bedeutet, dass Informationen als relevant gelten, wenn sie wesentliche oder potenziell wesentliche Auswirkungen auf Menschen, die Umwelt oder finanzielle Aspekte des Unternehmens haben und somit die Entscheidungsfindung der Nutzer beeinflussen.
        - **Nicht Relevant**: Ein Merkmal ist nicht relevant, wenn es im Rahmen der doppelten Wesentlichkeit keine oder nur vernachlässigbare Auswirkungen auf die Entscheidungen der Nutzer hat.
        """)

# Diese Funktion lädt den aktuellen Session-State (den Zustand der Session), falls er bereits existiert.
def load_session_state():
    if 'relevance_selection' not in st.session_state:
        # Initialisierung des Session-States, falls nicht vorhanden
        st.session_state['relevance_selection'] = {}
    # Prüfen, ob eine gespeicherte Datei existiert, und diese laden
    if os.path.exists('SessionStatesThemenESRS.pkl'):
        with open('SessionStatesThemenESRS.pkl', 'rb') as f:
            st.session_state['relevance_selection'] = pickle.load(f)

# Diese Funktion speichert den aktuellen Session-State in eine Datei ab.
def save_session_state():
    with open('SessionStatesThemenESRS.pkl', 'wb') as f:
        pickle.dump(st.session_state['relevance_selection'], f)

# Diese Bedingung stellt sicher, dass der Session-State zu Beginn geladen wird, falls noch nicht vorhanden.
if 'relevance_selection' not in st.session_state:
    load_session_state()

# Diese Funktion zählt, wie viele Checkboxen in der aktuellen Session angekreuzt wurden.
def count_checkboxes():
    # Filtert nur die Checkboxen heraus, die tatsächlich angekreuzt sind (True).
    checkbox_count = sum(1 for value in st.session_state['relevance_selection'].values() if isinstance(value, bool) and value)
    
    # Speichert die Anzahl der aktiven Checkboxen in der Session
    st.session_state['checkbox_count'] = checkbox_count

    # Aktualisiert einen weiteren Zustand, um zu prüfen, ob alle 93 Checkboxen aktiviert wurden.
    st.session_state['checkbox_state_3'] = (checkbox_count == 93)
    
    return checkbox_count

# Diese Funktion berechnet den Prozentsatz der noch fehlenden Checkboxen.
def calculate_percentages():
    checkbox_count = st.session_state['checkbox_count']
    total_checkboxes = 93
    percentage_complete = round((checkbox_count / total_checkboxes) * 100, 1)
    percentage_missing = round(100 - percentage_complete, 1)
    
    return percentage_missing

# Diese Funktion zeigt den Fortschritt basierend auf der Anzahl der markierten Checkboxen an.
def checkboxes_count():
    checkbox_count = st.session_state['checkbox_count']
    total_checkboxes = 93
    number_of_missing_checkboxes = total_checkboxes - checkbox_count
    
    # Berechnung des prozentualen Fortschritts
    percentage_complete = round((checkbox_count / total_checkboxes) * 100, 0)
    
    # Berechnung des Fortschritts für die st.progress Anzeige
    percentage_complete_normalized = min(max(percentage_complete / 100.0, 0.0), 1.0)
    
    # Anzeige des Fortschritts und verbleibenden Checkboxen
    st.metric(label="**Themenspezifische ESRS**", value=checkbox_count)
    st.write("Checkboxen wurden bis jetzt ausgewählt.")
    st.write("Es fehlen noch: **" + str(number_of_missing_checkboxes) + "** Checkboxen.")
    st.progress(percentage_complete_normalized)


# Diese Funktion zeigt eine Themen-Sektion an, in der die Nutzer die Relevanz auswählen können.
# Die Parameter:
# - topics: Liste der Themen mit einem Schlüssel (key) für die Auswahl
# - section_key: Ein eindeutiger Schlüssel, um die Sektion im Session-State zu identifizieren
# - section_title: Der Titel der Sektion, die angezeigt wird
def display_section(topics, section_key, section_title):
    # Erstellen eines eindeutigen Schlüssels für das Formular
    form_key = f'form_{section_key}'
    
    # Start des Formulars zur Auswahl der Checkboxen
    with st.form(key=form_key, border=False):
        # Anzeige des Sektionstitels
        st.subheader(section_title)
        
        # Definition der Spaltenüberschriften "Relevant" und "Nicht Relevant"
        headers = ["Relevant", "Nicht Relevant"]
        
        # Erstellen einer Zeile für die Spaltenüberschriften
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            # Die Spaltenüberschrift wird in der jeweiligen Spalte angezeigt
            header_row[i + 1].write(header)

        # Dictionary, das die aktuelle Auswahl der Nutzer speichert
        current_selection = {}
        
        # Variable, die sicherstellt, dass nur eine Checkbox pro Thema ausgewählt wird
        validation_passed = True

        # Anzeige der Themen und Checkboxen für die Auswahl
        for topic, key in topics:
            # Erstellen von drei Spalten: Eine für das Thema, zwei für die Checkboxen
            cols = st.columns([4, 1, 1])
            
            # Das Thema wird in der ersten Spalte angezeigt
            cols[0].write(f"{topic}:")
            
            # Zähler zur Überprüfung, ob mehr als eine Checkbox pro Thema aktiviert wurde
            selected_count = 0
            for i, header in enumerate(headers):
                # Erstellen eines eindeutigen Schlüssels für jede Checkbox basierend auf Thema und Sektion
                checkbox_key = f"{header}_{key}_{section_key}"
                
                # Abrufen des aktuellen Zustands der Checkbox aus dem Session-State (True/False)
                checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                
                # Erstellen der Checkbox in der entsprechenden Spalte
                # label_visibility='collapsed' blendet die Beschriftung der Checkbox aus
                checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                
                # Speichern des aktuellen Zustands der Checkbox
                current_selection[checkbox_key] = checkbox_state
                
                # Zähler erhöht sich, wenn eine Checkbox aktiviert wurde
                if checkbox_state:
                    selected_count += 1
            
            # Validierung: Es darf nur eine Checkbox pro Thema ausgewählt werden (Relevant oder Nicht Relevant)
            if selected_count > 1:
                validation_passed = False

        # Speichern-Button wird am Ende des Formulars angezeigt
        submitted = st.form_submit_button("💾 Auswahl speichern")
        
        # Wenn der Speichern-Button gedrückt wurde
        if submitted:
            # Wenn die Validierung erfolgreich ist (nur eine Checkbox pro Thema)
            if validation_passed:
                # Aktualisierung des Session-State mit den neuen Werten
                st.session_state['relevance_selection'] = {**st.session_state['relevance_selection'], **current_selection}
                st.success("Auswahl erfolgreich gespeichert!")
                
                # Speichern des Session-States in einer Datei
                save_session_state()
                
                # Neuladen der Seite, um die neuen Werte anzuzeigen
                st.rerun()
            else:
                # Warnung, wenn mehr als eine Checkbox pro Thema ausgewählt wurde
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")

# Diese Funktion zeigt eine komplexere Sektion mit mehreren Untersektionen an.
# Die Parameter:
# - sections: Eine Liste von Abschnitten, die jeweils einen Titel und Themen enthalten
# - section_key: Ein eindeutiger Schlüssel, um die Sektion im Session-State zu identifizieren
# - section_title: Der Titel der Sektion, die angezeigt wird
def display_complex_section(sections, section_key, section_title):
    # Erstellen eines eindeutigen Schlüssels für das Formular
    form_key = f'form_{section_key}'
    
    # Start des Formulars zur Auswahl der Checkboxen
    with st.form(key=form_key, border=False):
        # Anzeige des Sektionstitels
        st.subheader(section_title)
        
        # Definition der Spaltenüberschriften "Relevant" und "Nicht Relevant"
        headers = ["Relevant", "Nicht Relevant"]

        # Erstellen einer Zeile für die Spaltenüberschriften
        header_row = st.columns([4, 1, 1])
        for i, header in enumerate(headers):
            # Die Spaltenüberschrift wird in der jeweiligen Spalte angezeigt
            header_row[i + 1].write(header)

        # Dictionary, das die Auswahl für alle Untersektionen speichert
        overall_selection = {}
        
        # Variable, die sicherstellt, dass nur eine Checkbox pro Thema ausgewählt wird
        all_validation_passed = True

        # Unterfunktion zur Erstellung von Themen innerhalb einer Sektion
        def create_section(title, topics):
            # Anzeige des Titels der Untersektion
            st.markdown(f"**{title}**")
            
            # Dictionary, das die Auswahl für die aktuelle Untersektion speichert
            current_selection = {}
            
            # Variable, die sicherstellt, dass nur eine Checkbox pro Thema ausgewählt wird
            validation_passed = True
            
            # Anzeige der Themen mit Checkboxen für die Auswahl
            for topic, key in topics:
                # Erstellen von drei Spalten: Eine für das Thema, zwei für die Checkboxen
                cols = st.columns([4, 1, 1])
                
                # Das Thema wird in der ersten Spalte angezeigt
                cols[0].write(f"{topic}:")
                
                # Zähler zur Überprüfung, ob mehr als eine Checkbox pro Thema aktiviert wurde
                selected_count = 0
                for i, header in enumerate(headers):
                    # Erstellen eines eindeutigen Schlüssels für jede Checkbox basierend auf Thema und Sektion
                    checkbox_key = f"{header}_{key}_{section_key}"
                    
                    # Abrufen des aktuellen Zustands der Checkbox aus dem Session-State (True/False)
                    checked = st.session_state['relevance_selection'].get(checkbox_key, False)
                    
                    # Erstellen der Checkbox in der entsprechenden Spalte
                    checkbox_state = cols[i + 1].checkbox("Select", key=checkbox_key, value=checked, label_visibility='collapsed')
                    
                    # Speichern des aktuellen Zustands der Checkbox
                    current_selection[checkbox_key] = checkbox_state
                    
                    # Zähler erhöht sich, wenn eine Checkbox aktiviert wurde
                    if checkbox_state:
                        selected_count += 1
                
                # Validierung: Es darf nur eine Checkbox pro Thema ausgewählt werden (Relevant oder Nicht Relevant)
                if selected_count > 1:
                    validation_passed = False
            
            # Rückgabe der Auswahl und des Validierungsergebnisses für die aktuelle Untersektion
            return current_selection, validation_passed

        # Iteration über alle Untersektionen
        for section_title, topics in sections:
            # Erstellung der Untersektion und Überprüfung der Auswahl
            current_selection, validation_passed = create_section(section_title, topics)
            
            # Zusammenführen der Auswahl der aktuellen Untersektion mit der Gesamt-Auswahl
            overall_selection.update(current_selection)
            
            # Überprüfen, ob die Validierung in allen Untersektionen erfolgreich war
            if not validation_passed:
                all_validation_passed = False

        # Speichern-Button wird am Ende des Formulars angezeigt
        submitted = st.form_submit_button("💾 Auswahl speichern")
        
        # Wenn der Speichern-Button gedrückt wurde
        if submitted:
            # Wenn die Validierung in allen Untersektionen erfolgreich ist
            if all_validation_passed:
                # Aktualisierung des Session-State mit den neuen Werten
                st.session_state['relevance_selection'] = {
                    **st.session_state.get('relevance_selection', {}),
                    **overall_selection
                }
                st.success("Auswahl erfolgreich gespeichert!")
                
                # Speichern des Session-States in einer Datei
                save_session_state()
                
                # Neuladen der Seite, um die neuen Werte anzuzeigen
                st.rerun()
            else:
                # Warnung, wenn mehr als eine Checkbox pro Thema ausgewählt wurde
                st.warning("Es darf nur eine Checkbox pro Zeile markiert sein.")


# Funktion zur Anzeige der Themen rund um Klimawandel
def display_E1_Klimawandel():
    # Definition der Themen innerhalb des Bereichs Klimawandel
    topics = [("Anpassung an Klimawandel", "Anpassung_an_den_Klimawandel"), ("Klimaschutz", "Klimaschutz"), ("Energie", "Energie")]
    # Aufruf der display_section Funktion, um die Themen in diesem Bereich anzuzeigen
    display_section(topics, "E1", "Klimawandel")

# Funktion zur Anzeige der Themen im Bereich Umweltverschmutzung
def display_E2_Umweltverschmutzung():
    # Definition der Themen, die Umweltverschmutzung betreffen
    topics = [
        ("Luftverschmutzung", "Luftverschmutzung"), ("Wasserverschmutzung", "Wasserverschmutzung"), ("Bodenverschmutzung", "Bodenverschmutzung"),
        ("Verschmutzung von lebenden Organismen und Nahrungsressourcen", "Verschmutzung_von_lebenden_Organismen_und_Nahrungsressourcen"),
        ("Besorgniserregende Stoffe", "Besorgniserregende_Stoffe"), ("Besonders besorgniserregende Stoffe", "Besonders_besorgniserregende_Stoffe"), ("Mikroplastik", "Mikroplastik")
    ]
    # Aufruf der display_section Funktion, um die Themen in diesem Bereich anzuzeigen
    display_section(topics, "E2", "Umweltverschmutzung")

# Funktion zur Anzeige der Themen im Bereich Wasser- und Meeresressourcen
def display_E3_Wasser_und_Meeresressourcen():
    # Definition der Themen, die Wasser- und Meeresressourcen betreffen
    topics = [
        ("Wasserverbrauch", "Wasserverbrauch"), ("Wasserentnahme", "Wasserentnahme"), ("Ableitung von Wasser", "Ableitung_von_Wasser"),
        ("Ableitung von Wasser in die Ozeane", "Ableitung_von_Wasser_in_die_Ozeane"), ("Gewinnung und Nutzung von Meeresressourcen", "Gewinnung_und_Nutzung_von_Meeresressourcen")
    ]
    # Aufruf der display_section Funktion, um die Themen in diesem Bereich anzuzeigen
    display_section(topics, "E3", "Wasser- und Meeresressourcen")

# Funktion zur Anzeige der komplexeren Themen im Bereich Biodiversität
def display_E4_Biodiversität():
    # Definition der Untersektionen und der zugehörigen Themen für Biodiversität
    sections = [
        ("Direkte Ursachen des Biodiversitätsverlusts", [
            ("Klimawandel", "Klimawandel"),
            ("Land-, Süßwasser- und Meeresnutzungsänderungen", "Land-,_Süßwasser-_und_Meeresnutzungsänderungen"),
            ("Direkte Ausbeutung", "Direkte_Ausbeutung"),
            ("Invasive gebietsfremde Arten", "Invasive_gebietsfremde_Arten"),
            ("Umweltverschmutzung", "Umweltverschmutzung"),
            ("Sonstige", "Sonstige")
        ]),
        ("Auswirkungen auf den Zustand der Arten", [
            ("Populationsgröße von Arten", "Populationsgröße_von_Arten"),
            ("Globales Ausrottungsrisiko von Arten", "Globales_Ausrottungsrisiko_von_Arten")
        ]),
        ("Auswirkungen auf den Umfang und den Zustand von Ökosystemen", [
            ("Landdegradation", "Landdegradation"),
            ("Wüstenbildung", "Wüstenbildung"),
            ("Bodenversiegelung", "Bodenversiegelung")
        ]),
        ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", [
            ("Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen", "Auswirkungen_und_Abhängigkeiten_von_Ökosystemdienstleistungen")
        ])
    ]
    # Aufruf der display_complex_section Funktion, um die Untersektionen und Themen in diesem Bereich anzuzeigen
    display_complex_section(sections, "E4", "Biodiversität")

# Funktion zur Anzeige der Themen im Bereich Kreislaufwirtschaft
def display_E5_Kreislaufwirtschaft():
    # Definition der Themen, die zur Kreislaufwirtschaft gehören
    topics = [("Ressourcenzuflüsse, einschließlich Ressourcennutzung", "Ressourcenzuflüsse,_einschließlich_Ressourcennutzung"), ("Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen", "Ressourcenabflüsse_im_Zusammenhang_mit_Produkten_und_Dienstleistungen"), ("Abfälle", "Abfälle")]
    # Aufruf der display_section Funktion, um die Themen in diesem Bereich anzuzeigen
    display_section(topics, "E5", "Kreislaufwirtschaft")

# Funktion zur Anzeige der Themen im Bereich eigene Belegschaft
def display_S1_Eigene_Belegschaft():
    # Definition der Untersektionen und Themen für die eigene Belegschaft
    sections = [
        ("Arbeitsbedingungen", [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"), ("Sozialer Dialog", "Sozialer_Dialog"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Berufs- und Privatleben", "Vereinbarkeit_von_Berufs-_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
        ]),
        ("Gleichbehandlung und Chancengleichheit für alle", [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
        ]),
        ("Sonstige arbeitsbezogene Rechte", [
            ("Kinderarbeit", "Kinderarbeit"), ("Zwangsarbeit", "Zwangsarbeit"), ("Angemessene Unterbringung", "Angemessene_Unterbringung"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"), ("Datenschutz", "Datenschutz")
        ])
    ]
    # Aufruf der display_complex_section Funktion, um die Untersektionen und Themen in diesem Bereich anzuzeigen
    display_complex_section(sections, "S1", "Eigene Belegschaft")

# Funktion zur Anzeige der Themen im Bereich Belegschaft in der Lieferkette
def display_S2_Belegschaft_Lieferkette():
    # Definition der Untersektionen und Themen für die Belegschaft in der Lieferkette
    sections = [
        ("Arbeitsbedingungen", [
            ("Sichere Beschäftigung", "Sichere Beschäftigung"), ("Arbeitszeit", "Arbeitszeit"), ("Angemessene Entlohnung", "Angemessene_Entlohnung"), ("Sozialer Dialog", "Sozialer_Dialog"),
            ("Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung", "Vereinigungsfreiheit,_Existenz_von_Betriebsräten_und_Rechte_der_Arbeitnehmer_auf_Information,_Anhörung_und_Mitbestimmung"),
            ("Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften", "Tarifverhandlungen,_einschließlich_der_Quote_der_durch_Tarifverträge_abgedeckten_Arbeitskräften"),
            ("Vereinbarkeit von Berufs- und Privatleben", "Vereinbarkeit_von_Berufs-_und_Privatleben"), ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit")
        ]),
        ("Gleichbehandlung und Chancengleichheit für alle", [
            ("Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit", "Gleichstellung_der_Geschlechter_und_gleicher_Lohn_für_gleiche_Arbeit"), ("Schulungen und Kompetenzentwicklung", "Schulungen_und_Kompetenzentwicklung"),
            ("Beschäftigung und Inklusion von Menschen mit Behinderungen", "Beschäftigung_und_Inklusion_von_Menschen_mit_Behinderungen"), ("Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz", "Maßnahmen_gegen_Gewalt_und_Belästigung_am_Arbeitsplatz"), ("Vielfalt", "Vielfalt")
        ]),
        ("Sonstige arbeitsbezogene Rechte", [
            ("Kinderarbeit", "Kinderarbeit"), ("Zwangsarbeit", "Zwangsarbeit"), ("Angemessene Unterbringung", "Angemessene_Unterbringung"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"), ("Datenschutz", "Datenschutz")
        ])
    ]
    # Aufruf der display_complex_section Funktion, um die Untersektionen und Themen in diesem Bereich anzuzeigen
    display_complex_section(sections, "S2", "Belegschaft in der Lieferkette")

# Funktion zur Anzeige der Themen im Bereich betroffene Gemeinschaften
def display_S3_Betroffene_Gemeinschaften():
    # Definition der Untersektionen und Themen für betroffene Gemeinschaften
    sections = [
        ("Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften", [
            ("Angemessene Unterbringung", "Angemessene_Unterbringung"), ("Angemessene Ernährung", "Angemessene_Ernährung"), ("Wasser- und Sanitäreinrichtungen", "Wasser-_und_Sanitäreinrichtungen"),
            ("Bodenbezogene Auswirkungen", "Bodenbezogene_Auswirkungen"), ("Sicherheitsbezogene Auswirkungen", "Sicherheitsbezogene_Auswirkungen")
        ]),
        ("Bürgerrechte und politische Rechte von Gemeinschaften", [
            ("Meinungsfreiheit", "Meinungsfreiheit"), ("Versammlungsfreiheit", "Versammlungsfreiheit"), ("Auswirkungen auf Menschenrechtsverteidiger", "Auswirkungen_auf_Menschenrechtsverteidiger")
        ]),
        ("Rechte indigener Völker", [
            ("Freiwillige und in Kenntnis der Sachlage erteilte vorherige Zustimmung", "Freiwillige_und_in_Kenntnis_der_Sachlage_erteilte_vorherige_Zustimmung"), ("Selbstbestimmung", "Selbstbestimmung"), ("Kulturelle Rechte", "Kulturelle_Rechte")
        ])
    ]
    # Aufruf der display_complex_section Funktion, um die Untersektionen und Themen in diesem Bereich anzuzeigen
    display_complex_section(sections, "S3", "Betroffene Gemeinschaften")

# Funktion zur Anzeige der Themen im Bereich Verbraucher und Endnutzer
def display_S4_Verbraucher_und_Endnutzer():
    # Definition der Untersektionen und Themen für Verbraucher und Endnutzer
    sections = [
        ("Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer", [
            ("Datenschutz", "Datenschutz"), ("Meinungsfreiheit", "Meinungsfreiheit"), ("Zugang zu (hochwertigen) Informationen", "Zugang_zu_(hochwertigen)_Informationen")
        ]),
        ("Persönliche Sicherheit von Verbrauchern und/oder Endnutzern", [
            ("Gesundheitsschutz und Sicherheit", "Gesundheitsschutz_und_Sicherheit"), ("Persönliche Sicherheit", "Persönliche_Sicherheit"), ("Kinderschutz", "Kinderschutz")
        ]),
        ("Soziale Inklusion von Verbrauchern und/oder Endnutzern", [
            ("Nichtdiskriminierung", "Nichtdiskriminierung"), ("Zugang zu Produkten und Dienstleistungen", "Zugang_zu_Produkten_und_Dienstleistungen"), ("Verantwortliche Vermarktungspraktiken", "Verantwortliche_Vermarktungspraktiken")
        ])
    ]
    # Aufruf der display_complex_section Funktion, um die Untersektionen und Themen in diesem Bereich anzuzeigen
    display_complex_section(sections, "S4", "Verbraucher und Endnutzer")

# Funktion zur Anzeige der Themen im Bereich Unternehmenspolitik
def display_G1_Unternehmenspolitik():
    # Definition der Themen, die zur Unternehmenspolitik gehören
    topics = [
        ("Unternehmenskultur", "Unternehmenskultur"), ("Schutz von Hinweisgebern (Whistleblowers)", "Schutz_von_Hinweisgebern_(Whistleblowers)"), ("Tierschutz", "Tierschutz"),
        ("Politisches Engagement und Lobbytätigkeiten", "Politisches_Engagement_und_Lobbytätigkeiten"), ("Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken", "Management_der_Beziehungen_zu_Lieferanten,_einschließlich_Zahlungspraktiken"),
        ("Vermeidung und Aufdeckung einschließlich Schulung", "Vermeidung_und_Aufdeckung_einschließlich_Schulung"), ("Vorkomnisse", "Vorkomnisse")
    ]
    # Aufruf der display_section Funktion, um die Themen in diesem Bereich anzuzeigen
    display_section(topics, "G1", "Unternehmenspolitik")

# Funktion zur Anzeige der gesamten Seite mit allen Tabs und Sektionen
def display_page():
    # Erstellen von zwei Spalten für das Layout der Seite
    col1, col2 = st.columns([6, 1.5])
    
    # In der ersten Spalte wird der Haupttitel angezeigt
    with col1:
        st.header("Themenspezifische ESRS") 
    
    # In der zweiten Spalte wird der Zähler der Checkboxen angezeigt
    with col2:
        # Container zur Umrahmung der Anzeige
        container = st.container(border=False)
        with container:
            # Zählen der markierten Checkboxen und Anzeige des Ergebnisses
            checkbox_count = count_checkboxes()
            st.metric(label="**Markierte Checkboxen von 93:**", value=checkbox_count)

    # Anzeige der Textbeschreibung und Anleitung
    Text()
    
    # Erstellung der Tabs für die verschiedenen Themenbereiche
    tabs = st.tabs(["Klimawandel", "Umweltverschmutzung", "Wasser- und Meeressourcen", "Biodiversität", "Kreislaufwirtschaft", "Eigene Belegschaft", "Belegschaft Lieferkette", "Betroffene Gemeinschaften", "Verbraucher und Endnutzer", "Unternehmenspolitik"])
    
    # Inhalte der einzelnen Tabs
    with tabs[0]:
        display_E1_Klimawandel()
    with tabs[1]:    
        display_E2_Umweltverschmutzung()
    with tabs[2]:  
        display_E3_Wasser_und_Meeresressourcen()
    with tabs[3]:  
        display_E4_Biodiversität()  
    with tabs[4]: 
        display_E5_Kreislaufwirtschaft()
    with tabs[5]:
        display_S1_Eigene_Belegschaft()
    with tabs[6]:
        display_S2_Belegschaft_Lieferkette()
    with tabs[7]:
        display_S3_Betroffene_Gemeinschaften()
    with tabs[8]:
        display_S4_Verbraucher_und_Endnutzer()
    with tabs[9]:
        display_G1_Unternehmenspolitik()

# Diese Codezeile sorgt dafür, dass der Session-State beim Laden der Seite geladen wird
load_session_state()
