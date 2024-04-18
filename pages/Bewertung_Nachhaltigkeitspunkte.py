import streamlit as st
import pandas as pd


def display_essential_topics():
    essential_topics = []
    for topic, values in st.session_state.items():
        if isinstance(values, dict) and values.get('Wesentlich', False):
            essential_topics.append(topic)
    
    df = pd.DataFrame(essential_topics, columns=['Wesentliche Themen'])
    st.write("Liste der als 'Wesentlich' markierten Themen:")
    st.dataframe(df)

def display_page():
    display_essential_topics()



