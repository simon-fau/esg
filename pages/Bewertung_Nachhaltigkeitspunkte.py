import streamlit as st
import pandas as pd
from pages.Bottom_up_stakeholder import stakeholder_punkte

def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' in st.session_state:
        df2 = st.session_state.df2
    else:
        df2 = pd.DataFrame({
            "Thema": [],
            "Unterthema": [],
            "Unter-Unterthema": []
        })

    # Zeige alle Themen unabhängig von ihrer Bewertung
    st.write("Liste aller eigens hinzugefügten Themen:")
    st.dataframe(df2)

def Top_down_Nachhaltigkeitspunkte():
    # Initialize a list to store topic details
    essential_topics_data = []
    # Anpassung der Inahlte für die Tabelle aus der Top_down.py, für Inhalte nur mit Thema und Unterthema
    for topic, values in st.session_state.items():
        if isinstance(values, dict):
            if values.get('Wesentlich', False) or values.get('Eher Wesentlich', False):
                # Assuming topic names are stored in the format "Thema - Unterthema - Unter-Unterthema"
                topic_details = topic.split(' - ')
                while len(topic_details) < 3:
                    topic_details.append('')
                # Check if the topic starts with "climate_change", "pollution_" or "water_usage_" and change the theme and subtheme accordingly
                if topic_details[0].startswith('climate_change'):
                    topic_details = ['Klimawandel', topic_details[0].replace('climate_change', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('pollution_'):
                    topic_details = ['Umweltverschmutzung', topic_details[0].replace('pollution_', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('water_usage_'):
                    topic_details = ['Wasser- & Meeresressourcen', topic_details[0].replace('water_usage_', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('kreislaufwirtschaft'):
                    topic_details = ['Kreislaufwirtschaft', topic_details[0].replace('kreislaufwirtschaft', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('unternehmenspolitik'):
                    topic_details = ['Unternehmenspolitik', topic_details[0].replace('unternehmenspolitik', '').strip().replace('_', ' '), topic_details[1]]
                elif topic_details[0].startswith('biodiversity_'):
                    if topic_details[0] in ['biodiversity_Populationsgröße von Arten', 'biodiversity_Globales Ausrottungsrisiko von Arten']:
                        topic_details = ['Biodiversität', 'Auswirkungen auf den Zustand der Arten', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['biodiversity_Landdegradation', 'biodiversity_Wüstenbildung', 'biodiversity_Bodenversiegelung']:
                        topic_details = ['Biodiversität', 'Auswirkungen auf den Umfang und den Zustand von Ökosystemen', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['biodiversity_Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen']:
                        topic_details = ['Biodiversität','Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                    else:
                        topic_details = ['Biodiversität', 'Direkte Ursachen des Biodiversitätsverlusts', topic_details[0].replace('biodiversity_', '').strip().replace('_', ' ')]
                elif topic_details[0].startswith('eigene_belegschaft_'):
                    if topic_details[0] in ['eigene_belegschaft_Sichere Beschäftigung', 'eigene_belegschaft_Arbeitszeit', 'eigene_belegschaft_Angemessene Entlohnung', 'eigene_belegschaft_Sozialer Dialog', 'eigene_belegschaft_Vereinigungsfreiheit, Existenz von Betriebsräten und Rechte der Arbeitnehmer auf Information, Anhörung und Mitbestimmung', 'eigene_belegschaft_Tarifverhandlungen, einschließlich der Quote der durch Tarifverträge abgedeckten Arbeitskräften', 'eigene_belegschaft_Vereinbarkeit von Berufs- und Privatleben', 'eigene_belegschaft_Gesundheitsschutz und Sicherheit']:
                        topic_details = ['Eigene Belegschaft','Arbeitsbedingungen', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['eigene_belegschaft_Gleichstellung der Geschlechter und gleicher Lohn für gleiche Arbeit', 'eigene_belegschaft_Schulungen und Kompetenzentwicklung', 'eigene_belegschaft_Beschäftigung und Inklusion von Menschen mit Behinderungen', 'eigene_belegschaft_Maßnahmen gegen Gewalt und Belästigung am Arbeitsplatz','eingene_belegschaft_Vielfalt']:
                        topic_details = ['Eigene Belegschaft','Gleichbehandlung und Chancengleichheit', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                    elif topic_details[0] in ['eigene_belegschaft_Kinderarbeit', 'eigene_belegschaft_Zwangsarbeit', 'eigene_belegschaft_Angemessene Unterbringung', 'eigene_belegschaft_Datenschutz']:
                        topic_details = ['Eigene Belegschaft','Sonstige arbeitsbezogene Rechte', topic_details[0].replace('eigene_belegschaft_', '').strip().replace('_', ' ')]
                # Append to the list with importance level
                essential_topics_data.append(topic_details + ['Wesentlich' if values.get('Wesentlich', False) else 'Eher Wesentlich'])


    # Create a DataFrame from the collected data
    df_essential = pd.DataFrame(essential_topics_data, columns=['Thema', 'Unterthema', 'Unter-Unterthema', 'Wichtigkeit'])
    df_essential = df_essential.sort_values(by=['Wichtigkeit', 'Thema'], ascending=[False, True])

    # Display the DataFrame
    st.write("Liste der als 'Wesentlich' oder 'Eher Wesentlich' markierten Themen aus Top_down:")
    st.dataframe(df_essential)

def display_page():
    eigene_Nachhaltigkeitspunkte()
    Top_down_Nachhaltigkeitspunkte()


        



