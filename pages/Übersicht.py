import streamlit as st
from pages.Stakeholder_Management import stakeholder_ranking, stakeholder_network
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import merge_dataframes, bewertung_Uebersicht
from pages.Shortlist import chart_übersicht_allgemein, chart_auswirkungsbezogen, chart_finanzbezogen

def display_stakeholder_table():
    class_size = calculate_class_size(st.session_state.stakeholder_punkte_df)
    stakeholder_punkte_filtered = calculate_selected_rows(st.session_state.stakeholder_punkte_df, class_size)
    st.session_state.stakeholder_punkte_filtered = stakeholder_punkte_filtered

    if not stakeholder_punkte_filtered.empty:
        stakeholder_punkte_filtered.reset_index(inplace=True)
        stakeholder_punkte_filtered.rename(columns={'index': '_index'}, inplace=True)

        # Ensure "Platzierung" is the first column
        columns = stakeholder_punkte_filtered.columns.tolist()
        if 'Platzierung' in columns:
            columns.insert(0, columns.pop(columns.index('Platzierung')))
        stakeholder_punkte_filtered = stakeholder_punkte_filtered[columns]

        # Remove the "Quelle" column if it exists
        if 'Quelle' in stakeholder_punkte_filtered.columns:
            stakeholder_punkte_filtered = stakeholder_punkte_filtered.drop(columns=['Quelle'])

        # Display the table without checkboxes
        grid_response = display_aggrid(stakeholder_punkte_filtered.drop(columns=['_index']), with_checkboxes=False)
    else:
        st.warning("Es wurden noch keine Inhalte im Excel-Upload hochgeladen. Bitte laden Sie eine Excel-Datei hoch.")

#Anzahl der Punkte in der Longlist für die Darstellung in der Übersicht
def anzahl_punkte_Longlist():
    if 'longlist' in st.session_state:
        count = len(st.session_state.longlist)
        st.metric(label="Anzahl der Punkte in der Longlist:", value=count)

# Function to count top-down points
def count_top_down_points():
    combined_df = st.session_state.combined_df
    count = combined_df[combined_df['Quelle'].str.contains("Top-Down|Top-Down Bewertung|Top-Down & Top-Down Bewertung", na=False)].shape[0]
    st.metric("davon themespezifische Punkte:", count)

# Function to count internal points
def count_internal_points():
    combined_df = st.session_state.combined_df
    count = combined_df[combined_df['Quelle'].str.contains("Eigene & Intern", na=False)].shape[0]
    st.metric("davon interne Punkte", count)

# Function to count stakeholder points
def count_stakeholder_points():
    combined_df = st.session_state.combined_df
    count = combined_df[~combined_df['Quelle'].str.contains("Top-Down|Top-Down Bewertung|Top-Down & Top-Down Bewertung|Eigene & Intern", na=False)].shape[0]
    st.metric("davon externe Punkte", count)

def count_shortlist_points():
    if 'filtered_df' in st.session_state:
        count = len(st.session_state.filtered_df)
        st.metric("Anzahl der Punkte in der Shortlist:", count)

def companies_in_stakeholder_table():
    if 'company_names' in st.session_state: 
        st.markdown("Nachhaltigkeitspunkte von folgenden Stakeholdern einbezogen:")
        for index, row in st.session_state.company_names.iterrows():
            st.markdown(f"- {row['Company Name']}")

def display_page():
    tab1, tab2, tab3 = st.tabs(["Allgemeine Übersicht", "Longlist", "Shortlist"])

    with tab1:
        col = st.columns((1.5, 4.5, 2), gap='medium')
        
        with col[0]:
            container = st.container(border=True)
            with container:
                st.markdown('#### Longlist')
                anzahl_punkte_Longlist()
                count_top_down_points()
                count_internal_points()
                count_stakeholder_points()

            container_2 = st.container(border=True)
            with container_2:
                st.markdown('#### Fortschritt Bewertungen')
                bewertung_Uebersicht()
        
        with col[1]:
                chart_übersicht_allgemein(width=900, height=800)

        with col[2]:
            container_3 = st.container(border=True)
            with container_3:
                st.markdown('#### Shortlist')
                count_shortlist_points()

            container_4 = st.container(border=True)
            with container_4:
                st.markdown('#### Stakeholder')
                companies_in_stakeholder_table()
      

    with tab2:
        st.write("Longlist")
        
        chart_übersicht_allgemein()
        chart_auswirkungsbezogen()
        chart_finanzbezogen()
        merge_dataframes()

    with tab3:
        col1, col2 = st.columns ([3, 1])
        with col1:
            st.write("Identifikation und Bewertung von Stakeholdern")
            stakeholder_ranking()
        with col2:
            st.write("Stakeholder Netzwerk")
            stakeholder_network()
       
        companies_in_stakeholder_table()
        display_stakeholder_table()
        bewertung_Uebersicht()

        