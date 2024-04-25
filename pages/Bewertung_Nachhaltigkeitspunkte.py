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

    # Iterate over items in session_state to collect essential and more essential topics
    for topic, values in st.session_state.items():
        if isinstance(values, dict):
            if values.get('Wesentlich', False) or values.get('Eher Wesentlich', False):
                # Assuming topic names are stored in the format "Thema - Unterthema - Unter-Unterthema"
                topic_details = topic.split(' - ')
                while len(topic_details) < 3:
                    topic_details.append('')
                # Check if the topic is one of the specified ones and change the theme and subtheme accordingly
                if topic_details[0] in ['Anpassung an den Klimawandel', 'Energie', 'Klimaschutz']:
                    topic_details = ['Klimawandel', topic_details[0], topic_details[1]]
                elif topic_details[0] in ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung', 'Verschmutzung von lebenden Organismen und Nahrungsressourcen', 'Besorgniserregende Stoffe', 'Besonders besorgniserregende Stoffe', 'Mikroplastik']:
                    topic_details = ['Umweltverschmutzung', topic_details[0], topic_details[1]]
                elif topic_details[0] in ['Wasserverbrauch', 'Wasserentnahme', 'Ableitung von Wasser', 'Ableitung von Wasser in die Ozeane', 'Gewinnung und Nutzung von Meeresressourcen']:
                    topic_details = ['Wassernutzung', topic_details[0], topic_details[1]]
                elif topic_details[0] in ['Ressourcenzuflüsse einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle']:
                    topic_details = ['Kreislaufwirtschaft', topic_details[0], topic_details[1]]
                elif topic_details[0] in ['Klimawandel', 'Landnutzungsänderungen', 'Süßwasser- und Meeresnutzungsänderungen', 'Direkte Ausbeutung', 'Invasive gebietsfremde Arten', 'Umweltverschmutzung', 'Sonstige']:
                    topic_details = ['Biodiversität', 'Direkte Ursachen des Biodiversitätsverlusts', topic_details[0]]
                elif topic_details[0] in ['Populationsgröße von Arten', 'Globales Ausrottungsrisiko von Arten']:
                    topic_details = ['Biodiversität', 'Auswirkungen auf den Zustand der Arten', topic_details[0]]
                elif topic_details[0] in ['Landdegradation', 'Wüstenbildung', 'Bodenversiegelung']:
                    topic_details = ['Biodiversität', 'Auswirkungen auf den Umfang und den Zustand von Ökosystemen', topic_details[0]]   
                
                
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


        



