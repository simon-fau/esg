import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import altair as alt
import pickle
import os
import shutil
import io
from openpyxl import load_workbook

# Funktion zum Speichern des Zustands
def save_state():
    with open('SessionStates.pkl', 'wb') as f:
        pickle.dump(dict(st.session_state), f)

# Set initial session state values if they are not already set
if 'intersection_value' not in st.session_state:
    st.session_state['intersection_value'] = 350
if 'stakeholder_importance_value' not in st.session_state:
    st.session_state['stakeholder_importance_value'] = 1000
if 'filtered_df' not in st.session_state:
    st.session_state['filtered_df'] = pd.DataFrame()  # Initialize as an empty DataFrame

def Chart(intersection_value, stakeholder_importance_value):

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Prepare the data
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]
        required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']

        # Check if the DataFrame is empty after filtering
        if selected_columns_df.empty:
            st.info("Keine Daten vorhanden, um den Chart anzuzeigen.")
            return  # Stop the function execution

        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'

        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        selected_columns['Stakeholder Wichtigkeit'] = ((selected_columns['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        selected_columns['Stakeholder Wichtigkeit'] = selected_columns['Stakeholder Wichtigkeit'].fillna(100)

        # Base scatter chart
        scatter = alt.Chart(selected_columns, width=1000, height=800).mark_circle().encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Environmental', 'Social', 'Governance', 'Sonstige'],
                range=['green', 'yellow', 'blue', 'gray']
            ), legend=alt.Legend(
                title="Thema",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Environmental', 'Social', 'Governance', 'Sonstige']
            )),
            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=required_columns
        )

        # Line
        line = alt.Chart(pd.DataFrame({
            'x': [0, st.session_state['intersection_value']],
            'y': [st.session_state['intersection_value'], 0]
        })).mark_line(color='red').encode(
            x='x:Q',
            y='y:Q'
        )

        # Area to the left of the line
        area = alt.Chart(pd.DataFrame({
            'x': [0, 0, st.session_state['intersection_value']],
            'y': [0, st.session_state['intersection_value'], 0]
        })).mark_area(opacity=0.3, color='lightcoral').encode(
            x='x:Q',
            y='y:Q'
        )

        chart = area + scatter + line

        st.altair_chart(chart)
    else:
        st.info("Keine Daten ausgewählt.")

def filter_table(intersection_value, stakeholder_importance_value):
    st.header("Shortlist")

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Prepare the data
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns
        
        # Filter the data based on the sum of 'Score Finanzen' and 'Score Auswirkung' being greater than intersection_value
        st.session_state.filtered_df = selected_columns_df[
            (selected_columns_df['Score Finanzen'] + selected_columns_df['Score Auswirkung'] > st.session_state['intersection_value']) |
            (selected_columns_df['Stakeholder Wichtigkeit'] > st.session_state['stakeholder_importance_value'])
        ]
        
        # Ensure necessary columns are present
        columns_to_display = ['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Finanzen', 'Score Auswirkung']
        filtered_df = st.session_state.filtered_df[columns_to_display]

        if filtered_df.empty:
            st.info("Keine Inhalte verfügbar")
        else:
            # Configure the grid
            gb = GridOptionsBuilder.from_dataframe(filtered_df)
            gb.configure_side_bar()
            gb.configure_selection('single', use_checkbox=False, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
            grid_options = gb.build()
            
            # Display the grid
            AgGrid(filtered_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)

    else:
        st.info("Keine Inhalte vorhanden")

def display_slider():
    st.sidebar.markdown("---")
    # Slider for intersection value
    intersection_value = st.sidebar.slider("Schwellenwert festlegen", min_value=0, max_value=1000, value=st.session_state['intersection_value'], step=10)

    # Slider for stakeholder importance value
    stakeholder_importance_value = st.sidebar.slider("Grenzwert für Stakeholder Wichtigkeit angeben", min_value=0, max_value=1000, value=st.session_state['stakeholder_importance_value'], step=50)

    if st.sidebar.button('Auswahl anwenden'):
        st.session_state['intersection_value'] = intersection_value
        st.session_state['stakeholder_importance_value'] = stakeholder_importance_value
        st.session_state['apply_changes'] = True
        st.rerun()

def check_abgeschlossen_shortlist():
    if 'checkbox_state_7' not in st.session_state:
        st.session_state['checkbox_state_7'] = False
    # Checkbox erstellen und Zustand in st.session_state speichern
    st.session_state['checkbox_state_7'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_7'])

def placeholder():
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

def display_page():
   
    col1, col2 = st.columns([7, 1])
    with col1:
        st.header("Erstellung der Shortlist")
    with col2:
        check_abgeschlossen_shortlist()
        st.write("Hier können Sie die Shortlist auf Basis Ihrer Bewertungen in der Longlist erstellen. Um die Shortlist zu erstellen, müssen Sie zunächst die Grenzwerte für die Relevanz der Themen und Stakeholder festlegen. Sobald Sie sich für Schwellenwerte entschieden haben, wird Ihnen die Shortlist unterhalb der Wesentlichkeitsmatrix ausgegeben.")
        st.write("- Empfehlung Schwellenwert für Wesentlichkeit: 250 - 400")
        st.write("- Empfehlung Schwellenwert für Stakeholder-Wichtigkeit: 700 - 850 ")
    display_slider()
    if 'apply_changes' in st.session_state and st.session_state['apply_changes']:
        placeholder()
        Chart(st.session_state['intersection_value'], st.session_state['stakeholder_importance_value'])
        filter_table(st.session_state['intersection_value'], st.session_state['stakeholder_importance_value'])
    else:
        placeholder()
        Chart(350,1000)  # Display initial chart without any filter

    save_state()
    

#-------- Abschnitt zur Erstellung von unterschiedlichen Charts für die Übersicht ---------#

def chart_übersicht_allgemein_test_2(width, height):
    # Überprüfen, ob Daten ausgewählt wurden
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Daten vorbereiten
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]
        required_columns = [
            'ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema',
            'Unter-Unterthema', 'Stakeholder Wichtigkeit', 'Art der Auswirkung',
            'Eigenschaft der Auswirkung', 'Finanzielle Auswirkung'
        ]

        if selected_columns_df.empty:
            st.info("Keine Daten vorhanden, um den Chart anzuzeigen.")
            return

        # Farbzuteilungs-Funktionen
        def assign_color_by_theme(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'

        def assign_color_by_financial_impact(financial_impact):
            if financial_impact == 'Chance':
                return 'Chance'
            elif financial_impact == 'Risiko':
                return 'Risiko'
            elif financial_impact == 'Keine Auswirkung':
                return 'Keine finanzielle Auswirkung'
            else:
                return 'Keine finanzielle Auswirkung'

        # Extrahiere 'Art der Auswirkung' und 'Eigenschaft der Auswirkung' aus der Spalte 'Auswirkung'
        def extract_impact_type(impact):
            if 'Positive' in impact:
                return 'Positive Auswirkung'
            elif 'Negative' in impact:
                return 'Negative Auswirkung'
            else:
                return 'Keine Auswirkung'

        def extract_impact_property(impact):
            if 'Tatsächliche' in impact:
                return 'Tatsächliche Auswirkung'
            elif 'Potenzielle' in impact:
                return 'Potenzielle Auswirkung'
            else:
                return 'Keine Auswirkung'

        def determine_color(impact_type):
            if impact_type == 'Positive Auswirkung':
                return 'Positive Auswirkung'
            elif impact_type == 'Negative Auswirkung':
                return 'Negative Auswirkung'
            else:
                return None  # Ignore "Keine Auswirkung"

        def determine_shape(impact_property):
            if impact_property == 'Tatsächliche Auswirkung':
                return 'Tatsächliche Auswirkung'
            elif impact_property == 'Potenzielle Auswirkung':
                return 'Potenzielle Auswirkung'
            else:
                return None

        selected_columns['Art der Auswirkung'] = selected_columns['Auswirkung'].apply(extract_impact_type)
        selected_columns['Eigenschaft der Auswirkung'] = selected_columns['Auswirkung'].apply(extract_impact_property)

        # Extrahiere 'Finanzielle Auswirkung' aus der Spalte 'Finanziell'
        def extract_financial_impact(financial):
            if 'Risiko' in financial:
                return 'Risiko'
            elif 'Chance' in financial:
                return 'Chance'
            elif 'Keine Auswirkung' in financial:
                return 'Keine finanzielle Auswirkung'
            else:
                return 'Keine finanzielle Auswirkung'

        selected_columns['Finanzielle Auswirkung'] = selected_columns['Finanziell'].apply(extract_financial_impact)

        # Berechnung der Stakeholder Wichtigkeit
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()

        if min_rating == max_rating:
            # If no variation in 'Stakeholder Gesamtbew', set a default value and show a warning
            st.warning("Stakeholder Bewertung hat keine Unterschiede. Standardwert wird verwendet.")
            selected_columns['Stakeholder Wichtigkeit'] = 100
        else:
            selected_columns['Stakeholder Wichtigkeit'] = (
                (selected_columns['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)
            ) * (1000 - 100) + 100

        selected_columns['Stakeholder Wichtigkeit'] = selected_columns['Stakeholder Wichtigkeit'].fillna(100)

        # Layout: Obere Zeile mit Radio-Buttons und Slider
        top_col1, top_col2, top_col3_placeholder = st.columns([1, 1, 3], gap="small")
        
        with top_col1:
            legend_option = st.radio("Darstellung der Graphik:", ["Kategorien", "Finanzbezogene Ansicht", "Auswirkungsbezogene Ansicht"])
            placeholder()
        with top_col2:
            # Add a check for min and max values before creating the slider
            if selected_columns['Stakeholder Wichtigkeit'].min() != selected_columns['Stakeholder Wichtigkeit'].max():
                min_importance = st.slider(
                    "Minimale Stakeholder Wichtigkeit",
                    min_value=int(selected_columns['Stakeholder Wichtigkeit'].min()),
                    max_value=int(selected_columns['Stakeholder Wichtigkeit'].max()),
                    value=int(selected_columns['Stakeholder Wichtigkeit'].min())
                )
            else:
                st.warning("Keine ausreichenden Daten für die Stakeholder Bewertung.")
                return
        
        with top_col3_placeholder:
            st.empty()

        bar_chart_2 = None

        # Farbzuteilung und Formen basierend auf der Legendenauswahl
        if legend_option == "Kategorien":
            # Code für Kategorien
            selected_columns['color'] = selected_columns['Thema'].apply(assign_color_by_theme)
            color_scale = alt.Scale(
                domain=['Environmental', 'Social', 'Governance', 'Sonstige'],
                range=['green', 'yellow', 'blue', 'gray']
            )
            legend_title = "Kategorien"

            bar_data = selected_columns['color'].value_counts().reset_index()
            bar_data.columns = ['color', 'Anzahl']

            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),
                y=alt.Y('color:N', sort='-x', title='Kategorien'),
                color=alt.Color('color:N', scale=color_scale, legend=None)
            ).properties(
                width=650,
                height=200
            )
        elif legend_option == "Finanzbezogene Ansicht":
            # Code für Finanzbezogene Ansicht
            selected_columns['color'] = selected_columns['Finanzielle Auswirkung'].apply(assign_color_by_financial_impact)
            color_scale = alt.Scale(
                domain=['Chance', 'Risiko', 'Keine finanzielle Auswirkung'],
                range=['green', 'red', 'gray']
            )
            legend_title = "Finanzielle Auswirkung"

            bar_data = selected_columns['color'].value_counts().reset_index()
            bar_data.columns = ['color', 'Anzahl']

            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),
                y=alt.Y('color:N', sort='-x', title='Finanzielle Auswirkung'),
                color=alt.Color('color:N', scale=color_scale, legend=None)
            ).properties(
                width=650,
                height=200
            )
        elif legend_option == "Auswirkungsbezogene Ansicht":
            # Code für Auswirkungsbezogene Ansicht
            selected_columns['color'] = selected_columns['Art der Auswirkung'].apply(determine_color)
            selected_columns = selected_columns[selected_columns['color'].notnull()]

            selected_columns['shape'] = selected_columns['Eigenschaft der Auswirkung'].apply(determine_shape)

            color_scale = alt.Scale(
                domain=['Positive Auswirkung', 'Negative Auswirkung'],
                range=['green', 'red']
            )
            shape_scale = alt.Scale(
                domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'],
                range=['circle', 'square']
            )
            legend_title = "Art der Auswirkung"

            bar_data = selected_columns.groupby(['Art der Auswirkung', 'Eigenschaft der Auswirkung']).size().reset_index(name='Anzahl')

            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),
                y=alt.Y('Art der Auswirkung:N', sort=['Positive Auswirkung', 'Negative Auswirkung'], title='Art der Auswirkung'),
                color=alt.Color('Eigenschaft der Auswirkung:N', scale=alt.Scale(domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'], range=['blue', 'orange']), legend=alt.Legend(
                    title="Typ der Auswirkung",
                    orient="top",
                    titleColor='black',
                    labelColor='black',
                    titleFontSize=12,
                    labelFontSize=10
                ))
            ).properties(
                width=650,
                height=200
            )

            bar_data_2 = selected_columns.groupby(['Eigenschaft der Auswirkung', 'Art der Auswirkung']).size().reset_index(name='Anzahl')

            bar_chart_2 = alt.Chart(bar_data_2).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),
                y=alt.Y('Eigenschaft der Auswirkung:N', sort=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'], title='Eigenschaft der Auswirkung'),
                color=alt.Color('Art der Auswirkung:N', scale=alt.Scale(domain=['Positive Auswirkung', 'Negative Auswirkung'], range=['green', 'red']), legend=alt.Legend(
                    title="Art der Auswirkung",
                    orient="top",
                    titleColor='black',
                    labelColor='black',
                    titleFontSize=12,
                    labelFontSize=10
                ))
            ).properties(
                width=650,
                height=200
            )

            

        # Daten filtern basierend auf der Mindest-Stakeholder Wichtigkeit
        filtered_columns = selected_columns[selected_columns['Stakeholder Wichtigkeit'] >= min_importance]

        # Layout: Untere Zeile mit Scatter-Chart und Balkendiagramm
        bottom_col1, bottom_col2 = st.columns([1.5 , 1], gap="small")  # Breitere linke Spalte für Scatter-Chart

        with bottom_col1:
            if legend_option == "Auswirkungsbezogene Ansicht":
                # Interaktiver Selektor für die Legende
                color_selection = alt.selection_multi(fields=['color'], bind='legend')
                shape_selection = alt.selection_multi(fields=['shape'], bind='legend')
                importance_selection = alt.selection_interval(fields=['Stakeholder Wichtigkeit'], bind='scales')

                # Scatter-Chart erstellen
                scatter = alt.Chart(filtered_columns, width=width, height=height).mark_point(filled=True).encode(
                    x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
                    y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
                    color=alt.Color('color:N', scale=color_scale, legend=alt.Legend(
                        title=legend_title,
                        orient="right",
                        titleColor='black',
                        labelColor='black',
                        titleFontSize=12,
                        labelFontSize=10,
                        values=['Positive Auswirkung', 'Negative Auswirkung']
                    )),
                    shape=alt.Shape('shape:N', scale=shape_scale, legend=alt.Legend(
                        title="Typ der Auswirkung",
                        orient="right",
                        titleColor='black',
                        labelColor='black',
                        titleFontSize=12,
                        labelFontSize=10,
                        values=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung']
                    )),
                    size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                        title="Stakeholder Wichtigkeit",
                        orient="right",
                        titleColor='black',
                        labelColor='black',
                        titleFontSize=12,
                        labelFontSize=10
                    )),
                    tooltip=required_columns,
                    opacity=alt.condition(
                        shape_selection & color_selection & importance_selection, alt.value(1), alt.value(0.2)
                    )  # Sichtbarkeit basierend auf Auswahl
                ).add_selection(
                    color_selection, shape_selection, importance_selection  # Legendenauswahl hinzufügen
                )
            else:
                # Interaktiver Selektor für die Legende
                color_selection = alt.selection_multi(fields=['color'], bind='legend')
                importance_selection = alt.selection_interval(fields=['Stakeholder Wichtigkeit'], bind='scales')

                # Scatter-Chart erstellen
                scatter = alt.Chart(filtered_columns, width=width, height=height).mark_circle().encode(
                    x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
                    y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
                    color=alt.Color('color:N', scale=color_scale, legend=alt.Legend(
                        title=legend_title,
                        orient="right",
                        titleColor='black',
                        labelColor='black',
                        titleFontSize=12,
                        labelFontSize=10
                    )),
                    size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                        title="Stakeholder Wichtigkeit",
                        orient="right",
                        titleColor='black',
                        labelColor='black',
                        titleFontSize=12,
                        labelFontSize=10
                    )),
                    tooltip=required_columns,
                    opacity=alt.condition(color_selection & importance_selection, alt.value(1), alt.value(0.2))  # Sichtbarkeit basierend auf Auswahl
                ).add_selection(
                    color_selection, importance_selection  # Legendenauswahl hinzufügen
                )

            st.altair_chart(scatter)

        with bottom_col2:
            # Balkendiagramme anzeigen
            st.altair_chart(bar_chart)
            if bar_chart_2 is not None:
                st.altair_chart(bar_chart_2)
    else:
        st.info("Keine Daten ausgewählt.")


# Graphik zur Darstellung auswikrungsbezogener Punkte. Unterscheidung positiv & negativ, sowie potentiell und tatsächlich
def chart_auswirkungsbezogen(width, height):

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        df = st.session_state['selected_columns']

    
        # Farbcodierung basierend auf der Untersuchung der Zeichenkette in "Score Auswirkung"
        def determine_color(impact):
            if 'Positive Auswirkung' in impact:
                return 'Positive Auswirkung'
            elif 'Negative Auswirkung' in impact:
                return 'Negative Auswirkung'
            else:
                return None  # Ignore "Keine Auswirkung"

        # Shape determination basierend auf "Tatsächliche Auswirkung" oder "Potenzielle Auswirkung"
        def determine_shape(impact):
            if 'Tatsächliche Auswirkung' in impact:
                return 'Tatsächliche Auswirkung'
            elif 'Potenzielle Auswirkung' in impact:
                return 'Potenzielle Auswirkung'
            else:
                return None

        # Filter out rows with "Keine Auswirkung"
        df['color'] = df['Auswirkung'].apply(determine_color)
        df = df[df['color'].notnull()]

        # Add shape column
        df['shape'] = df['Auswirkung'].apply(determine_shape)

        # Berechnung der Stakeholder Wichtigkeit
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        df['Stakeholder Wichtigkeit'] = ((df['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        df['Stakeholder Wichtigkeit'] = df['Stakeholder Wichtigkeit'].fillna(100)

        # Basis-Scatter-Chart
        scatter = alt.Chart(df, width=width, height=height).mark_point(filled=True).encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Positive Auswirkung', 'Negative Auswirkung'],
                range=['green', 'red']
            ), legend=alt.Legend(
                title="Auswirkung",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Positive Auswirkung', 'Negative Auswirkung']
            )),
            shape=alt.Shape('shape:N', scale=alt.Scale(
                domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'],
                range=['circle', 'square']
            ), legend=alt.Legend(
                title="Typ der Auswirkung",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung']
            )),
            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        st.altair_chart(scatter)
    else:
        st.info("Keine Daten ausgewählt.")

def chart_finanzbezogen(width, height):
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        df = st.session_state['selected_columns']

        # Farbcodierung basierend auf der Untersuchung der Zeichenkette in "Score Finanzen"
        def determine_color(finance):
            if 'Chance' in finance:
                return 'Chance'
            elif 'Risiko' in finance:
                return 'Risiko'
            else:
                return None  # Ignore "Keine Relevanz"

        # Filter out rows with "Keine Relevanz"
        df['color'] = df['Finanziell'].apply(determine_color)
        df = df[df['color'].notnull()]

        # Berechnung der Stakeholder Wichtigkeit
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        df['Stakeholder Wichtigkeit'] = ((df['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        df['Stakeholder Wichtigkeit'] = df['Stakeholder Wichtigkeit'].fillna(100)

        # Basis-Scatter-Chart
        scatter = alt.Chart(df, width=width, height=height).mark_point(filled=True).encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Chance', 'Risiko'],
                range=['green', 'red']
            ), legend=alt.Legend(
                title="Finanzielle Relevanz",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Chance', 'Risiko']
            )),

            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        st.altair_chart(scatter)
    else:
        st.info("Keine Daten ausgewählt.")

def Balken_Auswirkungsbezogen():

    selected_columns = st.session_state.get('selected_columns', pd.DataFrame())

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    necessary_columns = {'Score Auswirkung', 'Unter-Unterthema', 'Unterthema', 'Thema', 'Auswirkung', 'Stakeholder Bew Auswirkung'}
    if not necessary_columns.issubset(selected_columns.columns):
        st.error("Die notwendigen Spalten sind nicht im DataFrame vorhanden.")
        return

    # Funktion zur Extraktion der relevanten Auswirkung
    def extract_impact(value):
        if pd.isna(value):
            return None
        for impact in ['Negative Auswirkung', 'Positive Auswirkung']:
            if impact in value:
                return impact
        return None

    selected_columns['Extracted_Auswirkung'] = selected_columns['Auswirkung'].apply(extract_impact)

    # Filtere Daten mit "Keine Auswirkung" aus
    selected_columns = selected_columns[selected_columns['Auswirkung'] != 'Keine Auswirkung']

    # Erstellen der neuen Spalte 'Name'
    def create_name(row):
        unter_unterthema_count = selected_columns['Unter-Unterthema'].value_counts().get(row['Unter-Unterthema'], 0)
        unterthema_count = selected_columns['Unterthema'].value_counts().get(row['Unterthema'], 0)

        if row['Unter-Unterthema']:
            if unter_unterthema_count > 1:
                return row['Unter-Unterthema'] + '_' + row['Thema']
            else:
                return row['Unter-Unterthema']
        else:
            if unterthema_count > 1:
                return row['Unterthema'] + '_' + row['Thema']
            else:
                return row['Unterthema']

    selected_columns['Name'] = selected_columns.apply(create_name, axis=1)

    # Speichere den vorbereiteten DataFrame in der Session-State
    st.session_state['prepared_df'] = selected_columns

    # Führe die restlichen Schritte durch, um die Top 30 nach Score Auswirkung zu filtern und anzuzeigen
    filtered_df = selected_columns[selected_columns['Score Auswirkung'] > 1]

    top_30_df = filtered_df.nlargest(30, 'Score Auswirkung').sort_values('Score Auswirkung')

    # Bar-Chart erstellen
    if not top_30_df.empty:
        color_scale = alt.Scale(
            domain=['Negative Auswirkung', 'Positive Auswirkung'],
            range=['red', 'green']
        )

        chart = alt.Chart(top_30_df).mark_bar(size=20).encode(  # Setze die maximale Breite der Balken auf 20
            x=alt.X('Name', sort=None, title='Nachhaltigkeitspunkt'),
            y=alt.Y('Score Auswirkung', title='Score Auswirkung', stack=None),
            color=alt.Color('Extracted_Auswirkung', title='Art der Auswirkung', scale=color_scale),
            tooltip=['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Auswirkung']
        ).properties(
            width=800,
            height=400
        )
            
        st.altair_chart(chart)
    else:
        st.warning("Keine Daten verfügbar nach Anwendung der Filter.")

    

def Balken_Finanzbezogen():

    # Beispiel-Session-State (ersetzen durch den tatsächlichen Session-State in der Implementierung)
    selected_columns = st.session_state.get('selected_columns', pd.DataFrame())

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    if not {'Score Finanzen', 'Unter-Unterthema', 'Unterthema', 'Thema', 'Finanziell'}.issubset(selected_columns.columns):
        st.error("Die notwendigen Spalten sind nicht im DataFrame vorhanden.")
        return

    # Funktion zur Extraktion der relevanten Finanziell-Angabe
    def extract_financial(value):
        if pd.isna(value):
            return None
        for financial in ['Chance', 'Risiko']:
            if financial in value:
                return financial
        return None

    selected_columns['Extracted_Finanziell'] = selected_columns['Finanziell'].apply(extract_financial)

    # Filtere Daten mit "Keine Auswirkung" aus
    selected_columns = selected_columns[selected_columns['Finanziell'] != 'Keine Auswirkung']

    # Erstellen der neuen Spalte 'Name'
    def create_name(row):
        unter_unterthema_count = selected_columns['Unter-Unterthema'].value_counts().get(row['Unter-Unterthema'], 0)
        unterthema_count = selected_columns['Unterthema'].value_counts().get(row['Unterthema'], 0)

        if row['Unter-Unterthema']:
            if unter_unterthema_count > 1:
                return row['Unter-Unterthema'] + '_' + row['Thema']
            else:
                return row['Unter-Unterthema']
        else:
            if unterthema_count > 1:
                return row['Unterthema'] + '_' + row['Thema']
            else:
                return row['Unterthema']

    selected_columns['Name'] = selected_columns.apply(create_name, axis=1)

    filtered_df = selected_columns[selected_columns['Score Finanzen'] > 1]

    # Wähle die Top 30 Datensätze basierend auf 'Score Finanzen' und sortiere sie
    top_30_df = filtered_df.nlargest(30, 'Score Finanzen').sort_values('Score Finanzen')

    # Bar-Chart erstellen
    if not top_30_df.empty:
        color_scale = alt.Scale(
            domain=['Chance', 'Risiko'],
            range=['green', 'red']
        )

        chart = alt.Chart(top_30_df).mark_bar(size=20).encode(
            x=alt.X('Name', sort=None, title='Nachhaltigkeitspunkt'),
            y=alt.Y('Score Finanzen', title='Score Finanzen', stack=None),
            color=alt.Color('Extracted_Finanziell', title='Art der finanziellen Auswirkung', scale=color_scale),
            tooltip=['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Finanzen']
        ).properties(
            width=800,
            height=400
        )
        st.altair_chart(chart)
    else:
        st.warning("Keine Daten verfügbar nach Anwendung der Filter.")


def Balken_Auswirkungsbezogen_Stakeholder():
    ausgewählte_spalten = st.session_state.get('selected_columns', pd.DataFrame())

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    notwendige_spalten = {'Stakeholder Bew Auswirkung', 'Unter-Unterthema', 'Unterthema', 'Thema', 'Auswirkung'}
    if not notwendige_spalten.issubset(ausgewählte_spalten.columns):
        st.error("Die notwendigen Spalten sind nicht im DataFrame vorhanden.")
        return

    # Funktion zur Extraktion der relevanten Auswirkung
    def extrahiere_auswirkung(wert):
        if pd.isna(wert):
            return None
        for auswirkung in ['Negative Auswirkung', 'Positive Auswirkung']:
            if auswirkung in wert:
                return auswirkung
        return None

    ausgewählte_spalten['Extrahierte_Auswirkung'] = ausgewählte_spalten['Auswirkung'].apply(extrahiere_auswirkung)

    # Filtere Daten mit "Keine Auswirkung" und nicht-numerische Werte aus
    ausgewählte_spalten = ausgewählte_spalten[
        (ausgewählte_spalten['Auswirkung'] != 'Keine Auswirkung') & 
        (pd.to_numeric(ausgewählte_spalten['Stakeholder Bew Auswirkung'], errors='coerce').notna())
    ]

    # Konvertiere 'Stakeholder Bew Auswirkung' in numerische Werte
    ausgewählte_spalten['Stakeholder Bew Auswirkung'] = pd.to_numeric(ausgewählte_spalten['Stakeholder Bew Auswirkung'], errors='coerce')

    # Erstellen der neuen Spalte 'Bezeichnung'
    def erstelle_name(zeile):
        unter_unterthema_anzahl = ausgewählte_spalten['Unter-Unterthema'].value_counts().get(zeile['Unter-Unterthema'], 0)
        unterthema_anzahl = ausgewählte_spalten['Unterthema'].value_counts().get(zeile['Unterthema'], 0)

        if zeile['Unter-Unterthema']:
            if unter_unterthema_anzahl > 1:
                return zeile['Unter-Unterthema'] + '_' + zeile['Thema']
            else:
                return zeile['Unter-Unterthema']
        else:
            if unterthema_anzahl > 1:
                return zeile['Unterthema'] + '_' + zeile['Thema']
            else:
                return zeile['Unterthema']

    ausgewählte_spalten['Bezeichnung'] = ausgewählte_spalten.apply(erstelle_name, axis=1)

    # Speichere den vorbereiteten DataFrame in der Session-State
    st.session_state['vorbereiteter_df'] = ausgewählte_spalten

    # Führe die restlichen Schritte durch, um die Top 30 nach Stakeholder Bew Auswirkung zu filtern und anzuzeigen
    gefilterte_df = ausgewählte_spalten[ausgewählte_spalten['Stakeholder Bew Auswirkung'] > 0]

    # Prüfe, ob Stakeholder-Bewertung-Auswirkung vorhanden ist, und sortiere die Top 30
    if not gefilterte_df.empty:
        # Sortiere nach 'Stakeholder Bew Auswirkung'
        top_30 = gefilterte_df.nlargest(30, 'Stakeholder Bew Auswirkung').sort_values('Stakeholder Bew Auswirkung')

        if not top_30.empty:
            farbskala = alt.Scale(
                domain=['Negative Auswirkung', 'Positive Auswirkung'],
                range=['red', 'green']
            )

            diagramm = alt.Chart(top_30).mark_bar(size=20).encode(
                x=alt.X('Bezeichnung', sort=None, title='Nachhaltigkeitspunkt'),
                y=alt.Y('Stakeholder Bew Auswirkung', title='Stakeholder Bewertung Auswirkung', stack=None),
                color=alt.Color('Extrahierte_Auswirkung', title='Art der Auswirkung', scale=farbskala),
                tooltip=['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Auswirkung']
            ).properties(
                width=800,  
                height=400  
            )

            st.altair_chart(diagramm)
        else:
            st.warning("Keine Daten verfügbar nach Anwendung der Filter.")
    else:
        st.warning("Keine Stakeholder Bewertung vorhanden.")



def Balken_Finanzbezogen_Stakeholder():

    # Beispiel-Session-State (ersetzen durch den tatsächlichen Session-State in der Implementierung)
    selected_columns = st.session_state.get('selected_columns', pd.DataFrame())

    # Überprüfen, ob die notwendigen Spalten vorhanden sind
    if not {'Stakeholder Bew Finanzen', 'Unter-Unterthema', 'Unterthema', 'Thema', 'Finanziell'}.issubset(selected_columns.columns):
        st.error("Die notwendigen Spalten sind nicht im DataFrame vorhanden.")
        return

    # Funktion zur Extraktion der relevanten Finanziell-Angabe
    def extract_financial(value):
        if pd.isna(value):
            return None
        for financial in ['Chance', 'Risiko']:
            if financial in value:
                return financial
        return None

    selected_columns['Extracted_Finanziell'] = selected_columns['Finanziell'].apply(extract_financial)

    # Filtere Daten mit "Keine Auswirkung" aus
    selected_columns = selected_columns[selected_columns['Finanziell'] != 'Keine Auswirkung']

    # Erstellen der neuen Spalte 'Name'
    def create_name(row):
        unter_unterthema_count = selected_columns['Unter-Unterthema'].value_counts().get(row['Unter-Unterthema'], 0)
        unterthema_count = selected_columns['Unterthema'].value_counts().get(row['Unterthema'], 0)

        if row['Unter-Unterthema']:
            if unter_unterthema_count > 1:
                return row['Unter-Unterthema'] + '_' + row['Thema']
            else:
                return row['Unter-Unterthema']
        else:
            if unterthema_count > 1:
                return row['Unterthema'] + '_' + row['Thema']
            else:
                return row['Unterthema']

    selected_columns['Name'] = selected_columns.apply(create_name, axis=1)

    filtered_df = selected_columns[selected_columns['Stakeholder Bew Finanzen'] > 1]

    # Wähle die Top 30 Datensätze basierend auf 'Stakeholder Bew Finanzen' und sortiere sie
    top_30_df = filtered_df.nlargest(30, 'Stakeholder Bew Finanzen').sort_values('Stakeholder Bew Finanzen')

    # Bar-Chart erstellen
    if not top_30_df.empty:
        color_scale = alt.Scale(
            domain=['Chance', 'Risiko'],
            range=['green', 'red']
        )

        chart = alt.Chart(top_30_df).mark_bar(size=20).encode(
            x=alt.X('Name', sort=None, title='Nachhaltigkeitspunkt'),
            y=alt.Y('Stakeholder Bew Finanzen', title='Stakeholder Bewertung Finanzen', stack=None),
            color=alt.Color('Extracted_Finanziell', title='Art der finanziellen Auswirkung', scale=color_scale),
            tooltip=['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Bew Finanzen']
        ).properties(
            width=800,
            height=400
        )
        
        st.altair_chart(chart)
    else:
        st.warning("Keine Daten verfügbar nach Anwendung der Filter.")