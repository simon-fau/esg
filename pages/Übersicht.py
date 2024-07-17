import streamlit as st
from pages.Stakeholder_Management import stakeholder_ranking
from pages.Externe_Nachhaltigkeitspunkte import calculate_class_size, calculate_selected_rows, display_aggrid
from pages.Longlist import bewertung_Uebersicht, anzahl_punkte_Longlist, count_top_down_points, count_internal_points, count_stakeholder_points
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

    col = st.columns((1.5, 4.5, 1.5), gap='medium')
    
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
        
        container_3 = st.container(border=True)
        with container_3:
            col1, col2 = st.columns([1, 2])
            with col1:
                chart_options = ["Allgemeine Graphik", "Auswirkungsbezoge Graphik", "Finanzbezoge Graphik"]
                selected_chart = st.selectbox("Wähle eine Grafik aus:", chart_options)
            with col2:
                pass
            # Anzeigen der ausgewählten Grafik
            if selected_chart == "Allgemeine Graphik":
                chart_übersicht_allgemein(width=900, height=800)
            elif selected_chart == "Auswirkungsbezoge Graphik":
                chart_auswirkungsbezogen(width=900, height=800)
            elif selected_chart == "Finanzbezoge Graphik":
                chart_finanzbezogen(width=900, height=800)

    with col[2]:
        container_4 = st.container(border=True)
        with container_4:
            st.markdown('#### Shortlist')
            count_shortlist_points()

        container_5 = st.container(border=True)
        with container_5:
            st.markdown('#### Stakeholder')
            companies_in_stakeholder_table()

        container_6 = st.container(border=True)
        with container_6:
            st.markdown('#### Stakeholder Ranking')
            stakeholder_ranking()