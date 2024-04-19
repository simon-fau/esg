import streamlit as st
import pandas as pd

# Funktion, um die Hierarchie zu füllen, falls höhere Ebenen leer sind
def fill_hierarchy(row):
    if pd.isna(row['Unter-Unterthema']):
        if pd.isna(row['Unterthema']):
            return row['Thema']
        else:
            return row['Unterthema']
    return row['Unter-Unterthema']

def get_numerical_rating(value):
    ratings = {
        'Wesentlich': 3,
        'Eher Wesentlich': 2,
        'Eher nicht Wesentlich': 1,
        'Nicht Wesentlich': 0
    }
    return ratings.get(value, 0)

def aggregate_rankings(aggregate_df):
    aggregate_df['Hierarchie'] = aggregate_df.apply(fill_hierarchy, axis=1)
    aggregate_df['NumericalRating'] = aggregate_df['Bewertung'].apply(get_numerical_rating)
    ranking = aggregate_df.groupby(['Hierarchie'], as_index=False)['NumericalRating'].sum()
    return ranking.sort_values(by='NumericalRating', ascending=False)

# Funktion, um neue Bewertungen zu den bestehenden hinzuzufügen
def update_rankings(new_df):
    if 'ranking_df' not in st.session_state or st.session_state.ranking_df.empty:
        st.session_state.ranking_df = new_df.copy()
    else:
        st.session_state.ranking_df = pd.concat([st.session_state.ranking_df, new_df])
        st.session_state.ranking_df = aggregate_rankings(st.session_state.ranking_df)

# Hauptfunktion für Streamlit-Seite
def display_page():
    st.title("Ranking der Bewertungen")
    uploaded_files = st.file_uploader("Excel-Dateien hochladen", accept_multiple_files=True, type=['xlsx'])
    df_list = []

    for uploaded_file in uploaded_files:
        if uploaded_file:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            df_list.append(df)

    if st.button('Ranking erstellen'):
        if df_list:
            combined_df = pd.concat(df_list)
            update_rankings(combined_df)
            st.write("Aktuelles Ranking basierend auf hochgeladenen Dateien:")
            st.dataframe(st.session_state.ranking_df)
        else:
            st.error("Bittee laden Sie mindestens eine Excel-Datei hoch.")


display_page()





