import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

def create_scatter_chart():
    # Erstellen Sie einige zufällige Daten
    x = np.random.rand(2)
    y = np.random.rand(2)

    # Erstellen Sie ein DataFrame
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'Punkt': [f'Punkt {i+1}' for i in range(len(x))]
    })

    # Erstellen Sie ein Scatter-Chart
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x='x',
        y='y',
        tooltip='Punkt'
    )

    # Zeigen Sie das Diagramm in Streamlit an
    st.altair_chart(chart)

# Rufen Sie die Funktion in Ihrem Streamlit-Script auf
create_scatter_chart()