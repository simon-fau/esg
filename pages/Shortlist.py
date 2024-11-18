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
    # Speichert den aktuellen Sitzungszustand in einer Datei
    with open('SessionStates.pkl', 'wb') as f:
        pickle.dump(dict(st.session_state), f)

# Initialisiert Sitzungszustandswerte, falls diese noch nicht gesetzt sind
if 'intersection_value' not in st.session_state:
    st.session_state['intersection_value'] = 350
if 'stakeholder_importance_value' not in st.session_state:
    st.session_state['stakeholder_importance_value'] = 1000
if 'filtered_df' not in st.session_state:
    st.session_state['filtered_df'] = pd.DataFrame()  # Initialisiert als leeres DataFrame

# Funktion zur Darstellung des Charts
def Chart(intersection_value, stakeholder_importance_value):

    # Prüft, ob Spalten ausgewählt wurden und mehr als 0 vorhanden sind
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Daten vorbereiten
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns

        # Wählt die anzuzeigenden Spalten aus
        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]
        required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']

        # Prüft, ob das DataFrame nach dem Filtern leer ist
        if selected_columns_df.empty:
            st.info("Keine Daten vorhanden, um den Chart anzuzeigen.")
            return  # Beendet die Funktion, wenn keine Daten vorliegen

        # Funktion zur Zuweisung von Farben basierend auf dem Thema
        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'

        # Fügt eine Spalte 'color' hinzu, die auf der Themenzuweisung basiert
        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        # Berechnet die Stakeholder-Wichtigkeit und skaliert sie
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        selected_columns['Stakeholder Wichtigkeit'] = ((selected_columns['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        selected_columns['Stakeholder Wichtigkeit'] = selected_columns['Stakeholder Wichtigkeit'].fillna(100)

        # Basis-Scatter-Chart
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

        # Linie für den Schnittpunkt
        line = alt.Chart(pd.DataFrame({
            'x': [0, st.session_state['intersection_value']],
            'y': [st.session_state['intersection_value'], 0]
        })).mark_line(color='red').encode(
            x='x:Q',
            y='y:Q'
        )

        # Fläche links von der Linie
        area = alt.Chart(pd.DataFrame({
            'x': [0, 0, st.session_state['intersection_value']],
            'y': [0, st.session_state['intersection_value'], 0]
        })).mark_area(opacity=0.3, color='lightcoral').encode(
            x='x:Q',
            y='y:Q'
        )

        # Kombiniert Fläche, Scatter und Linie zum Chart
        chart = area + scatter + line

        # Zeigt den Chart an
        st.altair_chart(chart)
    else:
        st.info("Keine Daten ausgewählt.")  # Nachricht, wenn keine Daten vorhanden sind

# Funktion zum Filtern und Anzeigen der Tabelle
def filter_table(intersection_value, stakeholder_importance_value):
    st.header("Shortlist")

    # Prüft, ob Spalten ausgewählt wurden und mehr als 0 vorhanden sind
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Daten vorbereiten
        if isinstance(selected_columns, list):
            selected_columns_df = pd.DataFrame(selected_columns)
        else:
            selected_columns_df = selected_columns
        
        # Filtert die Daten basierend auf dem Summe von 'Score Finanzen' und 'Score Auswirkung'
        st.session_state.filtered_df = selected_columns_df[
            (selected_columns_df['Score Finanzen'] + selected_columns_df['Score Auswirkung'] > st.session_state['intersection_value']) |
            (selected_columns_df['Stakeholder Wichtigkeit'] > st.session_state['stakeholder_importance_value'])
        ]
        
        # Stellt sicher, dass die notwendigen Spalten vorhanden sind
        columns_to_display = ['ID', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Score Finanzen', 'Score Auswirkung']
        filtered_df = st.session_state.filtered_df[columns_to_display]

        if filtered_df.empty:
            st.info("Keine Inhalte verfügbar")  # Nachricht, wenn keine Inhalte verfügbar sind
        else:
            # Konfiguriert das Grid
            gb = GridOptionsBuilder.from_dataframe(filtered_df)
            gb.configure_side_bar()
            gb.configure_selection('single', use_checkbox=False, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
            grid_options = gb.build()
            
            # Zeigt das Grid an
            AgGrid(filtered_df, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)

    else:
        st.info("Keine Inhalte vorhanden")  # Nachricht, wenn keine Inhalte vorhanden sind


def display_slider():
    st.sidebar.markdown("---")
    # Slider für den Schwellenwert der Wesentlichkeit
    intersection_value = st.sidebar.slider("Schwellenwert festlegen", min_value=0, max_value=1000, value=st.session_state['intersection_value'], step=10)

    # Slider für den Stakeholder-Wichtigkeitswert
    stakeholder_importance_value = st.sidebar.slider("Grenzwert für Stakeholder Wichtigkeit angeben", min_value=0, max_value=1000, value=st.session_state['stakeholder_importance_value'], step=50)

    # Button, um die Auswahl anzuwenden und die Werte zu aktualisieren
    if st.sidebar.button('Auswahl anwenden'):
        st.session_state['intersection_value'] = intersection_value
        st.session_state['stakeholder_importance_value'] = stakeholder_importance_value
        st.session_state['apply_changes'] = True
        st.rerun()  # Seite wird neu geladen, um die Änderungen anzuwenden

# Funktion zur Erstellung einer Checkbox, um den Abschluss der Shortlist anzugeben
def check_abgeschlossen_shortlist():
    if 'checkbox_state_7' not in st.session_state:
        st.session_state['checkbox_state_7'] = False
    # Checkbox erstellen und Zustand in st.session_state speichern
    st.session_state['checkbox_state_7'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_7'])

# Platzhalterfunktion, um den Layoutabstand auf der Seite zu wahren
def placeholder():
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

# Hauptfunktion zur Darstellung der Seite
def display_page():
   
    # Layout mit zwei Spalten erstellen
    col1, col2 = st.columns([7, 1])
    with col1:
        st.header("Erstellung der Shortlist")
        # Beschreibungen zur Funktionsweise der Shortlist und der empfohlenen Schwellenwerte
        st.write("Hier können Sie die Shortlist auf Basis Ihrer Bewertungen in der Longlist erstellen. Um die Shortlist zu erstellen, müssen Sie zunächst die Grenzwerte für die Relevanz der Themen und Stakeholder festlegen.")
        st.write("Sobald Sie sich für Schwellenwerte entschieden haben, wird Ihnen die Shortlist unterhalb der Wesentlichkeitsmatrix ausgegeben.")
        st.write("- Empfehlung Schwellenwert für Wesentlichkeit: 250 - 400")
        st.write("- Empfehlung Schwellenwert für Stakeholder-Wichtigkeit: 700 - 850 ")
    with col2:
        # Zeigt die Checkbox für den Abschlussstatus der Shortlist an
        check_abgeschlossen_shortlist()
    
    # Zeigt die Slider für die Auswahl der Schwellenwerte an
    display_slider()

    # Überprüft, ob Änderungen angewendet wurden und zeigt den Chart sowie die gefilterte Tabelle an
    if 'apply_changes' in st.session_state and st.session_state['apply_changes']:
        placeholder()
        # Chart und gefilterte Tabelle basierend auf den benutzerdefinierten Schwellenwerten anzeigen
        Chart(st.session_state['intersection_value'], st.session_state['stakeholder_importance_value'])
        filter_table(st.session_state['intersection_value'], st.session_state['stakeholder_importance_value'])
    else:
        placeholder()
        # Standardchart anzeigen, wenn keine Filter angewendet wurden
        Chart(350,1000)

    # Speichert den aktuellen Sitzungszustand
    save_state()

#-------------------------------------------- Abschnitt zur Erstellung von unterschiedlichen Charts für die Übersicht ---------------------------------------#

def chart_übersicht_allgemein_test_2(width, height):
    # Überprüfen, ob in der Session 'selected_columns' vorhanden sind und ob Spalten ausgewählt wurden
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']

        # Überprüfen, ob die ausgewählten Spalten eine Liste oder ein DataFrame sind
        if isinstance(selected_columns, list):  # Wenn es sich um eine Liste handelt, in DataFrame umwandeln
            selected_columns_df = pd.DataFrame(selected_columns)
        else:  # Falls es bereits ein DataFrame ist, direkt zuweisen
            selected_columns_df = selected_columns

        # Definiere die Spalten, die für die Anzeige relevant sind
        columns_to_display = ['Score Finanzen', 'Score Auswirkung']
        selected_columns_df = selected_columns_df[columns_to_display]  # Filtere nur diese Spalten

        # Definiere die benötigten Spalten für die weitere Verarbeitung
        required_columns = [
            'ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema',
            'Unter-Unterthema', 'Stakeholder Wichtigkeit', 'Art der Auswirkung',
            'Eigenschaft der Auswirkung', 'Finanzielle Auswirkung'
        ]

        # Überprüfe, ob das DataFrame leer ist und zeige eine Info-Meldung, falls keine Daten vorhanden sind
        if selected_columns_df.empty:
            st.info("Keine Daten vorhanden, um den Chart anzuzeigen.")
            return  # Beende die Funktion, wenn keine Daten verfügbar sind

        # Funktion zur Farbzuteilung basierend auf dem 'Thema'
        def assign_color_by_theme(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'  # Umweltbezogene Themen
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'  # Soziale Themen
            elif theme == 'Unternehmenspolitik':
                return 'Governance'  # Themen zu Unternehmensführung
            else:
                return 'Sonstige'  # Andere Themen, die keiner Kategorie zugeordnet sind

        # Funktion zur Farbzuteilung basierend auf der finanziellen Auswirkung
        def assign_color_by_financial_impact(financial_impact):
            if financial_impact == 'Chance':
                return 'Chance'  # Positive finanzielle Auswirkung
            elif financial_impact == 'Risiko':
                return 'Risiko'  # Negative finanzielle Auswirkung
            elif financial_impact == 'Keine Auswirkung':
                return 'Keine finanzielle Auswirkung'  # Keine finanzielle Auswirkung
            else:
                return 'Keine finanzielle Auswirkung'  # Standardfall für unbekannte Werte

        # Extrahiere die Art der Auswirkung aus der Spalte 'Auswirkung'
        def extract_impact_type(impact):
            if 'Positive' in impact:
                return 'Positive Auswirkung'  # Positive Auswirkung erkennen
            elif 'Negative' in impact:
                return 'Negative Auswirkung'  # Negative Auswirkung erkennen
            else:
                return 'Keine Auswirkung'  # Keine Auswirkung erkannt

        # Extrahiere die Eigenschaft der Auswirkung (tatsächlich oder potenziell)
        def extract_impact_property(impact):
            if 'Tatsächliche' in impact:
                return 'Tatsächliche Auswirkung'  # Tatsächliche Auswirkung erkennen
            elif 'Potenzielle' in impact:
                return 'Potenzielle Auswirkung'  # Potenzielle Auswirkung erkennen
            else:
                return 'Keine Auswirkung'  # Keine spezifische Eigenschaft erkannt

        # Bestimme die Farbe basierend auf der Art der Auswirkung
        def determine_color(impact_type):
            if impact_type == 'Positive Auswirkung':
                return 'Positive Auswirkung'  # Positive Auswirkungen erhalten eine bestimmte Farbe
            elif impact_type == 'Negative Auswirkung':
                return 'Negative Auswirkung'  # Negative Auswirkungen erhalten eine bestimmte Farbe
            else:
                return None  # Ignoriere Fälle ohne Auswirkung

        # Bestimme die Form basierend auf der Eigenschaft der Auswirkung
        def determine_shape(impact_property):
            if impact_property == 'Tatsächliche Auswirkung':
                return 'Tatsächliche Auswirkung'  # Tatsächliche Auswirkungen erhalten eine bestimmte Form
            elif impact_property == 'Potenzielle Auswirkung':
                return 'Potenzielle Auswirkung'  # Potenzielle Auswirkungen erhalten eine bestimmte Form
            else:
                return None  # Ignoriere Fälle ohne spezifische Eigenschaft

        # Wende die Funktionen an, um die Spalten 'Art der Auswirkung' und 'Eigenschaft der Auswirkung' zu extrahieren
        selected_columns['Art der Auswirkung'] = selected_columns['Auswirkung'].apply(extract_impact_type)
        selected_columns['Eigenschaft der Auswirkung'] = selected_columns['Auswirkung'].apply(extract_impact_property)

        # Extrahiere die finanzielle Auswirkung aus der Spalte 'Finanziell'
        def extract_financial_impact(financial):
            if 'Risiko' in financial:
                return 'Risiko'  # Wenn das Wort "Risiko" in der Beschreibung auftaucht
            elif 'Chance' in financial:
                return 'Chance'  # Wenn das Wort "Chance" in der Beschreibung auftaucht
            elif 'Keine Auswirkung' in financial:
                return 'Keine finanzielle Auswirkung'  # Wenn keine finanzielle Auswirkung vorhanden ist
            else:
                return 'Keine finanzielle Auswirkung'  # Standardfall

        # Wende die Funktion auf die Spalte 'Finanziell' an
        selected_columns['Finanzielle Auswirkung'] = selected_columns['Finanziell'].apply(extract_financial_impact)

        # Berechne die Stakeholder-Wichtigkeit basierend auf einer Bewertungs-Skala
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()  # Kleinste Bewertung finden
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()  # Größte Bewertung finden

        # Überprüfe, ob es Unterschiede in den Stakeholder-Bewertungen gibt
        if min_rating == max_rating:
            # Falls keine Variation in den Bewertungen vorhanden ist, eine Warnung anzeigen und einen Standardwert verwenden
            st.warning("Stakeholder Bewertung hat keine Unterschiede. Standardwert wird verwendet.")
            selected_columns['Stakeholder Wichtigkeit'] = 100  # Standardwert zuweisen
        else:
            # Normierte Berechnung der Stakeholder-Wichtigkeit auf einer Skala von 100 bis 1000
            selected_columns['Stakeholder Wichtigkeit'] = (
                (selected_columns['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)
            ) * (1000 - 100) + 100  # Linear skalieren zwischen 100 und 1000

        # Falls fehlende Werte vorhanden sind, fülle sie mit dem Standardwert 100
        selected_columns['Stakeholder Wichtigkeit'] = selected_columns['Stakeholder Wichtigkeit'].fillna(100)

        # Layout: Erstellen von drei Spalten für die Radio-Buttons und den Slider
        top_col1, top_col2, top_col3_placeholder = st.columns([1, 1, 3], gap="small")
        
        with top_col1:
            # Radio-Button zur Auswahl der Darstellungsart (Kategorien, finanzielle oder auswirkungsbezogene Ansicht)
            legend_option = st.radio("Darstellung der Graphik:", ["Kategorien", "Finanzbezogene Ansicht", "Auswirkungsbezogene Ansicht"])
            placeholder()  # Platzhalter

        with top_col2:
            # Slider zur Auswahl der minimalen Stakeholder-Wichtigkeit, nur wenn die Werte variieren
            if selected_columns['Stakeholder Wichtigkeit'].min() != selected_columns['Stakeholder Wichtigkeit'].max():
                min_importance = st.slider(
                    "Minimale Stakeholder Wichtigkeit",
                    min_value=int(selected_columns['Stakeholder Wichtigkeit'].min()),  # Minimaler Wert aus den Daten
                    max_value=int(selected_columns['Stakeholder Wichtigkeit'].max()),  # Maximaler Wert aus den Daten
                    value=int(selected_columns['Stakeholder Wichtigkeit'].min())  # Standardwert auf den minimalen Wert setzen
                )
            else:
                # Warnung anzeigen, wenn keine ausreichenden Daten vorhanden sind, um den Slider zu verwenden
                st.warning("Keine ausreichenden Daten für die Stakeholder Bewertung.")
                return  # Beende die Funktion, wenn nicht genügend Daten vorhanden sind
        
        with top_col3_placeholder:
            st.empty()  # Platzhalter für die dritte Spalte

        bar_chart_2 = None  # Initialisiere zweite Bar-Chart-Variable (für spätere Verwendung)

        # Erstelle Balkendiagramme basierend auf der ausgewählten Darstellung
        if legend_option == "Kategorien":
            # Zuweisung von Farben basierend auf den Themenkategorien
            selected_columns['color'] = selected_columns['Thema'].apply(assign_color_by_theme)
            color_scale = alt.Scale(
                domain=['Environmental', 'Social', 'Governance', 'Sonstige'],  # Definierte Kategorien
                range=['green', 'yellow', 'blue', 'gray']  # Entsprechende Farben für die Kategorien
            )
            legend_title = "Kategorien"  # Legendentitel für diese Ansicht

            # Erstelle ein Balkendiagramm basierend auf den Kategorien und deren Häufigkeit
            bar_data = selected_columns['color'].value_counts().reset_index()  # Zähle die Kategorien
            bar_data.columns = ['color', 'Anzahl']  # Benenne die Spalten um

            # Altair-Chart für die Darstellung
            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),  # X-Achse für die Anzahl der Themen
                y=alt.Y('color:N', sort='-x', title='Kategorien'),  # Y-Achse für die Kategorien
                color=alt.Color('color:N', scale=color_scale, legend=None)  # Farben zuweisen
            ).properties(
                width=650,
                height=200  # Festlegen der Diagrammgröße
            )
        
        elif legend_option == "Finanzbezogene Ansicht":
            # Zuweisung von Farben basierend auf der finanziellen Auswirkung
            selected_columns['color'] = selected_columns['Finanzielle Auswirkung'].apply(assign_color_by_financial_impact)
            color_scale = alt.Scale(
                domain=['Chance', 'Risiko', 'Keine finanzielle Auswirkung'],  # Definierte finanzielle Kategorien
                range=['green', 'red', 'gray']  # Farben für Chancen, Risiken und keine finanzielle Auswirkung
            )
            legend_title = "Finanzielle Auswirkung"  # Legendentitel für die finanzielle Ansicht

            # Erstelle ein Balkendiagramm basierend auf den finanziellen Auswirkungen und deren Häufigkeit
            bar_data = selected_columns['color'].value_counts().reset_index()  # Zähle die Vorkommen der finanziellen Auswirkungen
            bar_data.columns = ['color', 'Anzahl']  # Benenne die Spalten um

            # Altair-Chart für die Darstellung
            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),  # X-Achse für die Anzahl der finanziellen Auswirkungen
                y=alt.Y('color:N', sort='-x', title='Finanzielle Auswirkung'),  # Y-Achse für die Kategorien der finanziellen Auswirkungen
                color=alt.Color('color:N', scale=color_scale, legend=None)  # Farben zuweisen
            ).properties(
                width=650,
                height=200  # Festlegen der Diagrammgröße
            )

        elif legend_option == "Auswirkungsbezogene Ansicht":
            # Zuweisung von Farben basierend auf der Art der Auswirkung (positiv oder negativ)
            selected_columns['color'] = selected_columns['Art der Auswirkung'].apply(determine_color)
            selected_columns = selected_columns[selected_columns['color'].notnull()]  # Entferne Zeilen ohne Auswirkung

            # Zuweisung von Formen basierend auf der Eigenschaft der Auswirkung (tatsächlich oder potenziell)
            selected_columns['shape'] = selected_columns['Eigenschaft der Auswirkung'].apply(determine_shape)

            # Definiere die Farbskala für positive und negative Auswirkungen
            color_scale = alt.Scale(
                domain=['Positive Auswirkung', 'Negative Auswirkung'],
                range=['green', 'red']  # Farben für positive und negative Auswirkungen
            )
            # Definiere die Formskala für tatsächliche und potenzielle Auswirkungen
            shape_scale = alt.Scale(
                domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'],
                range=['circle', 'square']  # Formen für tatsächliche und potenzielle Auswirkungen
            )
            legend_title = "Art der Auswirkung"  # Legendentitel für die auswirkungsbezogene Ansicht

            # Gruppiere Daten nach Art und Eigenschaft der Auswirkung und zähle die Häufigkeit
            bar_data = selected_columns.groupby(['Art der Auswirkung', 'Eigenschaft der Auswirkung']).size().reset_index(name='Anzahl')

            # Altair-Chart für die Darstellung der Art der Auswirkung
            bar_chart = alt.Chart(bar_data).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),  # X-Achse für die Anzahl der Auswirkungen
                y=alt.Y('Art der Auswirkung:N', sort=['Positive Auswirkung', 'Negative Auswirkung'], title='Art der Auswirkung'),  # Y-Achse für die Art der Auswirkung
                color=alt.Color('Eigenschaft der Auswirkung:N', scale=alt.Scale(domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'], range=['blue', 'orange']), legend=alt.Legend(
                    title="Typ der Auswirkung",  # Legende für die Eigenschaft der Auswirkung
                    orient="top",  # Platzierung der Legende
                    titleColor='black',
                    labelColor='black',
                    titleFontSize=12,
                    labelFontSize=10
                ))
            ).properties(
                width=650,
                height=200  # Festlegen der Diagrammgröße
            )

            # Zweites Balkendiagramm, gruppiert nach Eigenschaft und Art der Auswirkung
            bar_data_2 = selected_columns.groupby(['Eigenschaft der Auswirkung', 'Art der Auswirkung']).size().reset_index(name='Anzahl')

            # Altair-Chart für die Darstellung der Eigenschaft der Auswirkung
            bar_chart_2 = alt.Chart(bar_data_2).mark_bar(size=15).encode(
                x=alt.X('Anzahl:Q', title='Anzahl'),  # X-Achse für die Anzahl der Auswirkungen
                y=alt.Y('Eigenschaft der Auswirkung:N', sort=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'], title='Eigenschaft der Auswirkung'),  # Y-Achse für die Eigenschaft der Auswirkung
                color=alt.Color('Art der Auswirkung:N', scale=alt.Scale(domain=['Positive Auswirkung', 'Negative Auswirkung'], range=['green', 'red']), legend=alt.Legend(
                    title="Art der Auswirkung",  # Legende für die Art der Auswirkung
                    orient="top",  # Platzierung der Legende
                    titleColor='black',
                    labelColor='black',
                    titleFontSize=12,
                    labelFontSize=10
                ))
            ).properties(
                width=650,
                height=200  # Festlegen der Diagrammgröße
            )


       # Daten filtern basierend auf der Mindest-Stakeholder Wichtigkeit
        filtered_columns = selected_columns[selected_columns['Stakeholder Wichtigkeit'] >= min_importance]
        # Nur Zeilen mit Stakeholder Wichtigkeit >= dem vom Benutzer festgelegten Minimum beibehalten

        # Layout: Untere Zeile mit Scatter-Chart und Balkendiagramm
        bottom_col1, bottom_col2 = st.columns([1.5 , 1], gap="small")  # Breitere linke Spalte für Scatter-Chart
        # Zwei Spalten: linke Spalte für Scatter-Chart (größer) und rechte Spalte für Balkendiagramme

        with bottom_col1:
            if legend_option == "Auswirkungsbezogene Ansicht":  # Wenn der Nutzer die auswirkungsbezogene Ansicht gewählt hat
                # Interaktiver Selektor für die Legende (Mehrfachauswahl)
                color_selection = alt.selection_multi(fields=['color'], bind='legend')
                shape_selection = alt.selection_multi(fields=['shape'], bind='legend')
                importance_selection = alt.selection_interval(fields=['Stakeholder Wichtigkeit'], bind='scales')
                # Ermöglicht die Auswahl der Farben, Formen und Wichtigkeitsskala über die Legende oder Achsen
                
                # Scatter-Chart erstellen (Punkte werden ausgefüllt dargestellt)
                scatter = alt.Chart(filtered_columns, width=width, height=height).mark_point(filled=True).encode(
                    x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
                    # X-Achse für die finanzielle Wesentlichkeit mit Skala von 0 bis 1000
                    y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
                    # Y-Achse für die auswirkungsbezogene Wesentlichkeit mit Skala von 0 bis 1000
                    color=alt.Color('color:N', scale=color_scale, legend=alt.Legend(
                        title=legend_title,  # Farblegende basierend auf der Kategorie 'color'
                        orient="right",  # Legende wird rechts positioniert
                        titleColor='black',  # Schwarzer Titeltext der Legende
                        labelColor='black',  # Schwarze Labels in der Legende
                        titleFontSize=12, labelFontSize=10,  # Schriftgrößen für Titel und Labels in der Legende
                        values=['Positive Auswirkung', 'Negative Auswirkung']  # Nur diese Werte anzeigen
                    )),
                    shape=alt.Shape('shape:N', scale=shape_scale, legend=alt.Legend(
                        title="Typ der Auswirkung",  # Formlegende für den Typ der Auswirkung (z.B. 'Tatsächliche' oder 'Potenzielle')
                        orient="right",  # Legende wird rechts positioniert
                        titleColor='black',  # Schwarzer Titeltext der Legende
                        labelColor='black',  # Schwarze Labels in der Legende
                        titleFontSize=12, labelFontSize=10,  # Schriftgrößen für Titel und Labels in der Legende
                        values=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung']  # Nur diese Werte anzeigen
                    )),
                    size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                        title="Stakeholder Wichtigkeit",  # Größenlegende für die Stakeholder-Wichtigkeit
                        orient="right",  # Legende wird rechts positioniert
                        titleColor='black',  # Schwarzer Titeltext der Legende
                        labelColor='black',  # Schwarze Labels in der Legende
                        titleFontSize=12, labelFontSize=10  # Schriftgrößen für Titel und Labels in der Legende
                    )),
                    tooltip=required_columns,  # Tooltips anzeigen mit allen notwendigen Informationen
                    opacity=alt.condition(
                        shape_selection & color_selection & importance_selection, alt.value(1), alt.value(0.2)
                        # Sichtbarkeit der Punkte basierend auf der Auswahl von Farbe, Form und Wichtigkeit
                    )
                ).add_selection(
                    color_selection, shape_selection, importance_selection  # Hinzufügen der interaktiven Auswahlen zur Legende
                )
            else:  # Andernfalls, wenn die Option nicht die auswirkungsbezogene Ansicht ist
                # Interaktiver Selektor für die Farblegende (ohne Formauswahl)
                color_selection = alt.selection_multi(fields=['color'], bind='legend')
                importance_selection = alt.selection_interval(fields=['Stakeholder Wichtigkeit'], bind='scales')
                # Interaktiver Selektor für Stakeholder Wichtigkeit

                # Scatter-Chart erstellen (Punkte werden als Kreise dargestellt)
                scatter = alt.Chart(filtered_columns, width=width, height=height).mark_circle().encode(
                    x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
                    # X-Achse für die finanzielle Wesentlichkeit mit Skala von 0 bis 1000
                    y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
                    # Y-Achse für die auswirkungsbezogene Wesentlichkeit mit Skala von 0 bis 1000
                    color=alt.Color('color:N', scale=color_scale, legend=alt.Legend(
                        title=legend_title,  # Farblegende basierend auf der Kategorie 'color'
                        orient="right",  # Legende wird rechts positioniert
                        titleColor='black',  # Schwarzer Titeltext der Legende
                        labelColor='black',  # Schwarze Labels in der Legende
                        titleFontSize=12, labelFontSize=10  # Schriftgrößen für Titel und Labels in der Legende
                    )),
                    size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                        title="Stakeholder Wichtigkeit",  # Größenlegende für die Stakeholder-Wichtigkeit
                        orient="right",  # Legende wird rechts positioniert
                        titleColor='black',  # Schwarzer Titeltext der Legende
                        labelColor='black',  # Schwarze Labels in der Legende
                        titleFontSize=12, labelFontSize=10  # Schriftgrößen für Titel und Labels in der Legende
                    )),
                    tooltip=required_columns,  # Tooltips anzeigen mit allen notwendigen Informationen
                    opacity=alt.condition(color_selection & importance_selection, alt.value(1), alt.value(0.2))
                    # Sichtbarkeit der Punkte basierend auf der Auswahl von Farbe und Wichtigkeit
                ).add_selection(
                    color_selection, importance_selection  # Hinzufügen der interaktiven Auswahlen zur Legende
                )

            # Streudiagramm in der linken Spalte anzeigen
            st.altair_chart(scatter)

        with bottom_col2:
            # Balkendiagramme in der rechten Spalte anzeigen
            st.altair_chart(bar_chart)  # Hauptbalkendiagramm anzeigen
            if bar_chart_2 is not None:  # Wenn ein zweites Balkendiagramm vorhanden ist, auch dieses anzeigen
                st.altair_chart(bar_chart_2)  # Zweites Balkendiagramm anzeigen

    # Wenn keine Daten in der Session ausgewählt sind, zeigt eine Info-Meldung
    else:
        st.info("Keine Daten ausgewählt.")

def chart_auswirkungsbezogen(width, height):
    # Leere Zeilen als Abstandshalter, um das Layout der Seite zu trennen
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Überprüfen, ob Spalten in 'selected_columns' der Session vorhanden sind
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        df = st.session_state['selected_columns']

        # Funktion zur Bestimmung der Farbe basierend auf der Auswirkung
        # Positive Auswirkungen werden grün, negative rot
        def determine_color(impact):
            if 'Positive Auswirkung' in impact:
                return 'Positive Auswirkung'
            elif 'Negative Auswirkung' in impact:
                return 'Negative Auswirkung'
            else:
                return None  # Ignoriert keine Auswirkungen

        # Funktion zur Bestimmung der Form, basierend darauf, ob die Auswirkung tatsächlich oder potenziell ist
        def determine_shape(impact):
            if 'Tatsächliche Auswirkung' in impact:
                return 'Tatsächliche Auswirkung'
            elif 'Potenzielle Auswirkung' in impact:
                return 'Potenzielle Auswirkung'
            else:
                return None

        # Entfernt Zeilen, die keine positive oder negative Auswirkung haben
        df['color'] = df['Auswirkung'].apply(determine_color)
        df = df[df['color'].notnull()]

        # Fügt eine Spalte zur Bestimmung der Form hinzu
        df['shape'] = df['Auswirkung'].apply(determine_shape)

        # Berechnet die Stakeholder-Wichtigkeit, normiert zwischen 100 und 1000
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        df['Stakeholder Wichtigkeit'] = ((df['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        df['Stakeholder Wichtigkeit'] = df['Stakeholder Wichtigkeit'].fillna(100)

        # Erstellen des Scatter-Diagramms
        # Punkte werden farbig und in verschiedenen Formen angezeigt, basierend auf der Art der Auswirkung
        scatter = alt.Chart(df, width=width, height=height).mark_point(filled=True).encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Positive Auswirkung', 'Negative Auswirkung'],
                range=['green', 'red']  # Grüne Punkte für positive, rote für negative Auswirkungen
            ), legend=alt.Legend(
                title="Auswirkung",  # Legende für die Art der Auswirkung
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Positive Auswirkung', 'Negative Auswirkung']
            )),
            shape=alt.Shape('shape:N', scale=alt.Scale(
                domain=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung'],
                range=['circle', 'square']  # Kreise für tatsächliche, Quadrate für potenzielle Auswirkungen
            ), legend=alt.Legend(
                title="Typ der Auswirkung",  # Legende für die Eigenschaft der Auswirkung
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Tatsächliche Auswirkung', 'Potenzielle Auswirkung']
            )),
            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",  # Größe der Punkte basierend auf der Stakeholder-Wichtigkeit
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        # Anzeige des Scatter-Diagramms
        st.altair_chart(scatter)
    else:
        st.info("Keine Daten ausgewählt.")  # Nachricht, wenn keine Daten ausgewählt wurden


def chart_finanzbezogen(width, height):
    # Leere Zeilen als Abstandshalter, um das Layout der Seite zu trennen
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Überprüfen, ob Spalten in 'selected_columns' der Session vorhanden sind
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        df = st.session_state['selected_columns']

        # Funktion zur Bestimmung der Farbe basierend auf der finanziellen Relevanz
        # Chance (grün) oder Risiko (rot) basierend auf der Zeichenkette in "Finanziell"
        def determine_color(finance):
            if 'Chance' in finance:
                return 'Chance'
            elif 'Risiko' in finance:
                return 'Risiko'
            else:
                return None  # Ignoriert keine Relevanz

        # Entfernt Zeilen ohne finanzielle Relevanz
        df['color'] = df['Finanziell'].apply(determine_color)
        df = df[df['color'].notnull()]

        # Berechnet die Stakeholder-Wichtigkeit, normiert zwischen 100 und 1000
        min_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].min()
        max_rating = st.session_state.combined_df['Stakeholder Gesamtbew'].max()
        df['Stakeholder Wichtigkeit'] = ((df['Stakeholder Gesamtbew'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        df['Stakeholder Wichtigkeit'] = df['Stakeholder Wichtigkeit'].fillna(100)

        # Erstellen des Scatter-Diagramms
        # Punkte werden farbig angezeigt basierend auf der finanziellen Relevanz (Chance oder Risiko)
        scatter = alt.Chart(df, width=width, height=height).mark_point(filled=True).encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 1000)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 1000)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['Chance', 'Risiko'],
                range=['green', 'red']  # Grüne Punkte für Chancen, rote für Risiken
            ), legend=alt.Legend(
                title="Finanzielle Relevanz",  # Legende für finanzielle Chancen und Risiken
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10,
                values=['Chance', 'Risiko']
            )),
            size=alt.Size('Stakeholder Wichtigkeit:Q', scale=alt.Scale(range=[100, 1000]), legend=alt.Legend(
                title="Stakeholder Wichtigkeit",  # Größe der Punkte basierend auf der Stakeholder-Wichtigkeit
                orient="right",
                titleColor='black',
                labelColor='black',
                titleFontSize=12,
                labelFontSize=10
            )),
            tooltip=['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        # Anzeige des Scatter-Diagramms
        st.altair_chart(scatter)
    else:
        st.info("Keine Daten ausgewählt.")  # Nachricht, wenn keine Daten ausgewählt wurden


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