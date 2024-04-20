import streamlit as st
import pandas as pd

def display_essential_topics():
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
    st.write("Liste aller Themen eigene:")
    st.dataframe(df2)

    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df3' in st.session_state:
        df3 = st.session_state.df3
    else:
        df3 = pd.DataFrame({
            "Thema": [],
            "Unterthema": [],
            "Unter-Unterthema": []
        })

    # Zeige alle Themen unabhängig von ihrer Bewertung
    st.write("Liste aller Themen stakeholder:")
    st.dataframe(df3)

    # Filtere und zeige nur die als 'Wesentlich' markierten Themen
    essential_topics = []
    for topic, values in st.session_state.items():
        if isinstance(values, dict) and values.get('Wesentlich', False):
            essential_topics.append(topic)
    
    df_essential = pd.DataFrame(essential_topics, columns=['Wesentliche Themen'])
    st.write("Liste der als 'Wesentlich' markierten Themen:")
    st.dataframe(df_essential)

def display_page():
    display_essential_topics()



