import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from pages.Bottom_up_stakeholder import stakeholder_punkte
import altair as alt
import numpy as np


def stakeholder_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Bottom_up_stakeholder.py über session_state
    if 'stakeholder_punkte_df' not in st.session_state:
        st.session_state.stakeholder_punkte_df = pd.DataFrame(columns=["Platzierung", "Thema", "Unterthema", "Unter-Unterthema", "NumericalRating"])
    df3 = st.session_state.stakeholder_punkte_df.copy()
    df3['Quelle'] = 'Stakeholder'

    # Berechnen Sie die Größe der Klassen
    class_size = (df3['NumericalRating'].max() - df3['NumericalRating'].min()) / 4

    # Fügen Sie zwei Spalten hinzu, wobei die erste Spalte halb so breit ist wie die zweite
    col1, col2 = st.columns([1,3])
    
    # Fügen Sie einen Schieberegler in der ersten Spalte hinzu
    with col1:
        options = ['Nicht Wesentlich', 'Eher nicht wesentlich', 'Eher Wesentlich', 'Wesentlich']
        st.sidebar.markdown("---")
        st.sidebar.text("Grenzwert für die Auswahl der Stakeholderpunkte:")
    
        # Überprüfen, ob 'slider_value' bereits im session_state gespeichert ist, wenn nicht, initialisieren Sie es mit einem Standardwert
        if 'slider_value' not in st.session_state:
            st.session_state.slider_value = options[0]
    
        # Speichern Sie den aktuellen Zustand des Schiebereglers
        current_slider_value = st.sidebar.select_slider('', options=options, value=st.session_state.slider_value)

        # Fügen Sie einen Button hinzu
        if st.sidebar.button('Auswahl übernehmen'):
            # Aktualisieren Sie 'slider_value' im session_state, wenn der Benutzer den Button drückt
            st.session_state.slider_value = current_slider_value
            st.experimental_rerun()
    
        st.markdown("""
            <style>
            .st-emotion-cache-183lzff,
            .st-emotion-cache-1inwz65 {
                font-family: "Source Sans Pro", sans-serif;
            }
            </style>
            """, unsafe_allow_html=True)
    
    # Die zweite Spalte bleibt leer
    with col2:
        pass

    # Berechnen Sie die Anzahl der ausgewählten Zeilen basierend auf der Auswahl
    if st.session_state.slider_value == 'Wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > 3 * class_size + df3['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher Wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > 2 * class_size + df3['NumericalRating'].min()]
    elif st.session_state.slider_value == 'Eher nicht wesentlich':
        selected_rows_st = df3[df3['NumericalRating'] > class_size + df3['NumericalRating'].min()]
    else:  # Nicht Wesentlich
        selected_rows_st = df3[df3['NumericalRating'] > 0]
    
    # Speichern Sie die ausgewählten Zeilen im session_state
    st.session_state.selected_rows_st = selected_rows_st
    
    return selected_rows_st

def eigene_Nachhaltigkeitspunkte():
    # Zugriff auf den DataFrame aus Eigene.py über session_state
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
    # Erstellen Sie eine Kopie von df2
    df4 = st.session_state.df2.copy()
    df4['Quelle'] = 'Eigene'
    return df4


def Top_down_Nachhaltigkeitspunkte():
    if 'yes_no_selection' not in st.session_state:
        st.session_state['yes_no_selection'] = {
            'Wesentlich_Klimawandel': False,
            'Eher_wesentlich_Klimawandel': False,
            'Eher_nicht_wesentlich_Klimawandel': False,
            'Nicht_wesentlich_Klimawandel': False,
            'Wesentlich_Klimawandel_2': False,
            'Eher_Wesentlich_Klimawandel_2': False,
            'Eher_nicht_wesentlich_2': False,
            'Nicht_Wesentlich_Klimawandel_2': False
        }

    wesentliche_themen = {
        'Wesentlich_Klimawandel': 'Anpassung an den Klimawandel',
        'Eher_Wesentlich_Klimawandel': 'Anpassung an den Klimawandel',
        'Wesentlich_Klimawandel_2': 'Klimaschutz',
        'Eher_Wesentlich_Klimawandel_2': 'Klimaschutz'
    }

    # Erstellen eines Dataframes für die wesentlichen Themen
    themen_liste = []
    for key, unterthema in wesentliche_themen.items():
        if st.session_state['yes_no_selection'][key]:
            themen_liste.append({
                'Thema': 'Klimawandel',
                'Unterthema': unterthema,
                'Unter-Unterthema': ''
            })

    if themen_liste:
        df_themen = pd.DataFrame(themen_liste)
        st.session_state['wesentliche_themen_df'] = df_themen
        st.write("Wesentliche Themen Dataframe:")
        st.dataframe(df_themen)
    else:
        st.write("Keine wesentlichen Themen ausgewählt.")

def initialize_bewertet_column(longlist):
    if 'selected_data' in st.session_state:
        longlist['Bewertet'] = longlist['ID'].apply(lambda x: 'Ja' if x in st.session_state.selected_data['ID'].values else 'Nein')
    else:
        longlist['Bewertet'] = 'Nein'
    return longlist

def submit_bewertung(longlist, ausgewaehlte_werte):
    if st.button("Bewertung absenden") and any(ausgewaehlte_werte.values()):
        if 'selected_rows' in st.session_state:
            new_data = pd.DataFrame(st.session_state['selected_rows'])
            if '_selectedRowNodeInfo' in new_data.columns:
                new_data.drop('_selectedRowNodeInfo', axis=1, inplace=True)

            # Zuordnung der Slider-Auswahlen zu numerischen Werten für die finanzielle Bewertung
            ausmass_finanziell_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            wahrscheinlichkeit_finanziell_mapping = {
                "Tritt nicht ein": 1, "Unwahrscheinlich": 2, "Eher unwahrscheinlich": 3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
            }
            auswirkung_finanziell_mapping = {
                "Keine": 1, "Sehr gering": 2, "Eher gering": 3, "Eher Hoch": 4, "Hoch": 5, "Sehr hoch": 6
            }
            # Zuordnung der Slider-Auswahlen zu numerischen Werten für die Auswirkungsbewertung
            ausmass_neg_tat_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_neg_tat_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_neg_tat_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            ausmass_neg_pot_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_neg_pot_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_neg_pot_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            wahrscheinlichkeit_neg_pot_mapping = {
                "Tritt nicht ein": 1, "Unwahrscheinlich": 2, "Eher unwahrscheinlich": 3, "Eher wahrscheinlich": 4, "Wahrscheinlich": 5, "Sicher": 6
            }
            ausmass_pos_tat_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_pos_tat_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            ausmass_pos_pot_mapping = {
                "Keine": 1, "Minimal": 2, "Niedrig": 3, "Medium": 4, "Hoch": 5, "Sehr hoch": 6
            }
            umfang_pos_pot_mapping = {
                "Keine": 1, "Lokal": 2, "Regional": 3, "National": 4, "International": 5, "Global": 6
            }
            behebbarkeit_pos_pot_mapping = {
                "Kein Aufwand": 1, "Leicht zu beheben": 2, "Mit Aufwand": 3, "Mit hohem Aufwand": 4, "Mit sehr hohem Aufwand": 5, "Nicht behebbar": 6
            }
            
            # Kombinieren der Bewertungen zu einer String-Beschreibung
            auswirkung_string = ' ; '.join(part for part in [
                ausgewaehlte_werte.get('auswirkung_option', ''),
                ausgewaehlte_werte.get('auswirkung_art_option', ''),
                ausgewaehlte_werte.get('ausmass_neg_tat', '') if ausgewaehlte_werte.get('ausmass_neg_tat') else '',
                ausgewaehlte_werte.get('umfang_neg_tat', '') if ausgewaehlte_werte.get('umfang_neg_tat') else '',
                ausgewaehlte_werte.get('behebbarkeit_neg_tat', '') if ausgewaehlte_werte.get('behebbarkeit_neg_tat') else '',
                ausgewaehlte_werte.get('ausmass_neg_pot', '') if ausgewaehlte_werte.get('ausmass_neg_pot') else '',
                ausgewaehlte_werte.get('umfang_neg_pot', '') if ausgewaehlte_werte.get('umfang_neg_pot') else '',
                ausgewaehlte_werte.get('behebbarkeit_neg_pot', '') if ausgewaehlte_werte.get('behebbarkeit_neg_pot') else '',
                ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', '') if ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot') else '',
                ausgewaehlte_werte.get('ausmass_pos_tat', '') if ausgewaehlte_werte.get('ausmass_pos_tat') else '',
                ausgewaehlte_werte.get('umfang_pos_tat', '') if ausgewaehlte_werte.get('umfang_pos_tat') else '',
                ausgewaehlte_werte.get('ausmass_pos_pot', '') if ausgewaehlte_werte.get('ausmass_pos_pot') else '',
                ausgewaehlte_werte.get('umfang_pos_pot', '') if ausgewaehlte_werte.get('umfang_pos_pot') else '',
                ausgewaehlte_werte.get('behebbarkeit_pos_pot', '') if ausgewaehlte_werte.get('behebbarkeit_pos_pot') else ''
            ] if part)

            new_data['Auswirkung'] = auswirkung_string
            finanziell_string = f"{ausgewaehlte_werte.get('ausmass_finanziell', '')} ; {ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', '')} ; {ausgewaehlte_werte.get('auswirkung_finanziell', '')}"
            new_data['Finanziell'] = finanziell_string
            
            # Berechnung des Scores für finanzielle Bewertungen normalized_score = ((produkt - min_produkt) / (max_produkt - min_produkt)) * 99 + 1
            new_data['Score Finanzen'] = np.round((
                                        ausmass_finanziell_mapping.get(ausgewaehlte_werte.get('ausmass_finanziell', 'Keine'), 1) *
                                        wahrscheinlichkeit_finanziell_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_finanziell', 'Keine'), 1) *
                                        auswirkung_finanziell_mapping.get(ausgewaehlte_werte.get('auswirkung_finanziell', 'Keine'), 1) - 1) / (216 - 1) * 99 + 1
                                        , 1)
            
            # Berechnung Tatsächliche negative Auswirkungen
            tatsaechlich_negativ = np.round(((
                ausmass_neg_tat_mapping.get(ausgewaehlte_werte.get('ausmass_neg_tat', 'Keine'), 1) *
                umfang_neg_tat_mapping.get(ausgewaehlte_werte.get('umfang_neg_tat', 'Keine'), 1) *
                behebbarkeit_neg_tat_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_tat', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Potenzielle negative Auswirkungen
            potentiell_negativ = np.round(((
                ausmass_neg_pot_mapping.get(ausgewaehlte_werte.get('ausmass_neg_pot', 'Keine'), 1) *
                umfang_neg_pot_mapping.get(ausgewaehlte_werte.get('umfang_neg_pot', 'Keine'), 1) *
                behebbarkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_neg_pot', 'Kein Aufwand'), 1) *
                wahrscheinlichkeit_neg_pot_mapping.get(ausgewaehlte_werte.get('wahrscheinlichkeit_neg_pot', 'Tritt nicht ein'), 1) - 1) / (1296 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Tatsächliche positive Auswirkungen
            tatsaechlich_positiv = np.round(((
                ausmass_pos_tat_mapping.get(ausgewaehlte_werte.get('ausmass_pos_tat', 'Keine'), 1) *
                umfang_pos_tat_mapping.get(ausgewaehlte_werte.get('umfang_pos_tat', 'Keine'), 1) - 1) / (36 - 1) * 99 + 1
                ), 1)
            
            # Berechnung Potenzielle positive Auswirkungen
            potentiell_positiv = np.round(((
                ausmass_pos_pot_mapping.get(ausgewaehlte_werte.get('ausmass_pos_pot', 'Keine'), 1) *
                umfang_pos_pot_mapping.get(ausgewaehlte_werte.get('umfang_pos_pot', 'Keine'), 1) *
                behebbarkeit_pos_pot_mapping.get(ausgewaehlte_werte.get('behebbarkeit_pos_pot', 'Kein Aufwand'), 1) - 1) / (216 - 1) * 99 + 1
                ), 1)
            
            # Berechnung des Gesamtscores für die Auswirkungsbewertung
            new_data['Score Auswirkung'] = tatsaechlich_negativ * tatsaechlich_positiv * potentiell_negativ * potentiell_positiv

            # Aktualisieren oder Erstellen des `selected_data` DataFrames im Session State
            if 'selected_data' in st.session_state:
                st.session_state.selected_data = pd.concat([st.session_state.selected_data, new_data], ignore_index=True)
                st.session_state.selected_data.drop_duplicates(subset='ID', keep='last', inplace=True)
            else:
                st.session_state.selected_data = new_data
            
            longlist['Bewertet'] = longlist['ID'].isin(st.session_state.selected_data['ID']).replace({True: 'Ja', False: 'Nein'})
        else:
            st.error("Bitte wählen Sie mindestens eine Zeile aus, bevor Sie eine Bewertung absenden.")
    return longlist


def display_selected_data():
    if 'selected_data' in st.session_state and not st.session_state.selected_data.empty:
        # Füllen Sie fehlende Werte in 'Thema', 'Unterthema' und 'Unter-Unterthema' mit einem leeren String
        for column in ['Thema', 'Unterthema', 'Unter-Unterthema']:
            st.session_state.selected_data[column] = st.session_state.selected_data[column].fillna('')

        # Auswahl der benötigten Spalten
        selected_columns = st.session_state.selected_data[['ID', 'Auswirkung', 'Finanziell', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']]

        # Extrahieren Sie die Spalte 'NumericalRating' aus 'combined_df' und fügen Sie sie zu 'selected_columns' hinzu
        if 'combined_df' in st.session_state and 'NumericalRating' in st.session_state.combined_df.columns:
            combined_df_with_numerical_rating = st.session_state.combined_df[['ID', 'NumericalRating']]
            selected_columns = pd.merge(selected_columns, combined_df_with_numerical_rating, on='ID', how='left')
        
        # Speichern Sie 'selected_columns' in 'st.session_state'
        st.session_state['selected_columns'] = selected_columns

        # Definieren der gridOptions
        gridOptions = {
            'defaultColDef': {
                'resizable': True,
                'width': 150,
                'minWidth': 50
            },
            'columnDefs': [
                {'headerName': 'ID', 'field': 'ID', 'width': 100, 'minWidth': 50},
                {'headerName': 'Auswirkung', 'field': 'Auswirkung', 'flex': 1},
                {'headerName': 'Finanziell', 'field': 'Finanziell', 'flex': 1},
                {'headerName': 'Finanz-Score', 'field': 'Score Finanzen', 'width': 150, 'minWidth': 50},
                {'headerName': 'Auswirkungs-Score', 'field': 'Score Auswirkung', 'width': 150, 'minWidth': 50},
                {'headerName': 'Thema', 'field': 'Thema', 'flex': 1},
                {'headerName': 'Unterthema', 'field': 'Unterthema', 'flex': 1},
                {'headerName': 'Unter-Unterthema', 'field': 'Unter-Unterthema', 'flex': 1},
                {'headerName': 'NumericalRating', 'field': 'NumericalRating', 'width': 150, 'minWidth': 50}
            ]
        }

def bewertung():
    if 'selected_columns' in st.session_state and not st.session_state.selected_columns.empty:
        selected_columns = st.session_state['selected_columns']

        # Create a selectbox for IDs
        selected_id = st.selectbox('ID auswählen', selected_columns['ID'].unique())

        # Filter the row with the selected ID
        selected_row = selected_columns[selected_columns['ID'] == selected_id]

        if not selected_row.empty:

            # Split the 'Auswirkung' string into parts by ';'
            auswirkung_parts = selected_row['Auswirkung'].values[0].split(';')

            # Split the 'Finanziell' string into parts by ';'
            finanziell_parts = selected_row['Finanziell'].values[0].split(';')

            # Display each part of 'Auswirkung'
            auswirkung_mapping = {
                1: 'Eigenschaft',
                2: 'Art',
                3: 'Ausmaß',
                4: 'Umfang',
                5: 'Behebarkeit',
                6: 'Wahrscheinlichkeit'
            }

            # Display each part of 'Finanziell'
            finanziell_mapping = {
                1: 'Ausmaß',
                2: 'Wahrscheinlichkeit',
                3: 'Finanzielle Auswirkung'
            }

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write("**Auswirkung**")
            
                for i, part in enumerate(auswirkung_parts, start=1):
                    if i in auswirkung_mapping:
                        st.write(f'{auswirkung_mapping[i]}:', part.strip())
                    else:
                        st.write(f'Auswirkung Teil {i}:', part.strip())

                st.write('Score:', selected_row['Score Auswirkung'].values[0])

            with col2:
                st.write("**Finanziell**")

                for i, part in enumerate(finanziell_parts, start=1):
                    if i in finanziell_mapping:
                        st.write(f'{finanziell_mapping[i]}:', part.strip())
                    else:
                        st.write(f'Finanziell Teil {i}:', part.strip())

                st.write('Score:', selected_row['Score Finanzen'].values[0])
            
            with col3:

                return
           
def display_grid(longlist):
    gb = GridOptionsBuilder.from_dataframe(longlist)
      # Set the number of rows per page to 10
    gb.configure_side_bar()
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children", rowMultiSelectWithClick=False)
    grid_options = gb.build()
    grid_response = AgGrid(longlist, gridOptions=grid_options, enable_enterprise_modules=True, update_mode=GridUpdateMode.MODEL_CHANGED, fit_columns_on_grid_load=True)
    st.session_state['selected_rows'] = grid_response['selected_rows']

# Erstellen Sie ein leeres Wörterbuch zur Speicherung von Inhalt-ID-Zuordnungen
content_id_map = {}

# Dies ist die nächste ID, die zugewiesen werden soll
next_id = 1

def merge_dataframes():
    global next_id  # Zugriff auf die globale Variable next_id
    # Abrufen der Daten von verschiedenen Quellen
    df4 = eigene_Nachhaltigkeitspunkte()
    df_essential = Top_down_Nachhaltigkeitspunkte()
    selected_rows_st = stakeholder_Nachhaltigkeitspunkte()

    # Kombinieren der Daten in einem DataFrame
    combined_df = pd.concat([df_essential, df4, selected_rows_st], ignore_index=True)

    # Entfernen von Zeilen, die nur NaN-Werte enthalten
    combined_df = combined_df.dropna(how='all')

    # Entfernen von führenden und nachfolgenden Leerzeichen in den Spalten 'Thema', 'Unterthema' und 'Unter-Unterthema'
    combined_df['Thema'] = combined_df['Thema'].str.strip()
    combined_df['Unterthema'] = combined_df['Unterthema'].str.strip()
    combined_df['Unter-Unterthema'] = combined_df['Unter-Unterthema'].str.strip()

    # Entfernen von Zeilen, in denen das 'Thema' NaN ist
    combined_df = combined_df.dropna(subset=['Thema'])

    # Gruppieren der Daten nach 'Thema', 'Unterthema' und 'Unter-Unterthema' und Zusammenführen der 'Quelle'-Werte
    combined_df = combined_df.groupby(['Thema', 'Unterthema', 'Unter-Unterthema']).agg({'Quelle': lambda x: ' & '.join(sorted(set(x)))}).reset_index()

    # Hinzufügen der 'NumericalRating' Spalte aus 'selected_rows_st'
    combined_df = pd.merge(combined_df, selected_rows_st[['Thema', 'Unterthema', 'Unter-Unterthema', 'NumericalRating']], on=['Thema', 'Unterthema', 'Unter-Unterthema'], how='left')

    # Entfernen von Duplikaten
    combined_df = combined_df.drop_duplicates(subset=['Thema', 'Unterthema', 'Unter-Unterthema'])

    # Hinzufügen einer 'ID'-Spalte
    combined_df.insert(0, 'ID', range(1, 1 + len(combined_df)))

     # Hinzufügen einer 'ID'-Spalte
    for index, row in combined_df.iterrows():
        content = (row['Thema'], row['Unterthema'], row['Unter-Unterthema'])

        # Überprüfen Sie, ob der Inhalt bereits eine ID hat
        if content in content_id_map:
            # Verwenden Sie die vorhandene ID
            id = content_id_map[content]
        else:
            # Erstellen Sie eine neue ID und speichern Sie die Zuordnung
            id = next_id
            content_id_map[content] = id
            next_id += 1  # Inkrementieren Sie die nächste ID

        # Setzen Sie die ID im DataFrame
        combined_df.at[index, 'ID'] = id
    
    # Erstellen eines session_state von combined_df
    st.session_state.combined_df = combined_df

    #Erstellung einer Kopie von combined_df ohne NumericalRating zur Darstellung der Longlist mit lediglich relevanten Spalten
    combined_df_without_numerical_rating = st.session_state.combined_df.drop(columns='NumericalRating')
    # Speichern Sie die neue DataFrame in 'st.session_state'
    st.session_state['combined_df_without_numerical_rating'] = combined_df_without_numerical_rating

    # Erstellen eines neuen DataFrame 'longlist', um Probleme mit der Zuordnung von 'selected_rows' zu vermeiden
    longlist = pd.DataFrame(combined_df_without_numerical_rating)

    # Initialisieren der 'Bewertet'-Spalte in 'longlist'
    longlist = initialize_bewertet_column(longlist)

    # Initialize all required variables for ausgewaehlte_werte
    option = auswirkung_option = auswirkung_art_option = ausmass_neg_tat = umfang_neg_tat = behebbarkeit_neg_tat = ''
    ausmass_neg_pot = umfang_neg_pot = behebbarkeit_neg_pot = wahrscheinlichkeit_neg_pot = ''  
    ausmass_pos_tat = umfang_pos_tat = ausmass_pos_pot = umfang_pos_pot = behebbarkeit_pos_pot = ''
    wahrscheinlichkeit_finanziell = ausmass_finanziell = auswirkung_finanziell = ''

    col1, col2, col_3_placeholder, col4 = st.columns([1, 1, 0.2, 1])
    with col1:
        st.subheader("Auwirkungsbewertung")
        auswirkung_option = st.selectbox('Bitte wählen Sie die Eigenschaft der Auswirkung:', ['Negative Auswirkung','Positive Auswirkung', 'Keine Auswirkung'], index=2, key="auswirkung_option")
        if auswirkung_option == 'Negative Auswirkung':
            auswirkung_art_option = st.selectbox('Bitte wählen Sie die Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option")      
            with col2:
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    ausmass_neg_tat = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_tat")
                    umfang_neg_tat = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_tat")
                    behebbarkeit_neg_tat = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    ausmass_neg_pot = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_neg_pot")
                    umfang_neg_pot = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_neg_pot")
                    behebbarkeit_neg_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_neg_pot")
                    wahrscheinlichkeit_neg_pot = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_neg_pot")
        elif auswirkung_option == 'Positive Auswirkung':
            auswirkung_art_option = st.selectbox('Bitte wählen Sie die Art der Auswirkung:', ['Tatsächliche Auswirkung', 'Potenzielle Auswirkung', ''], index=2, key="auswirkung_art_option_pos")
            with col2:
                if auswirkung_art_option == 'Tatsächliche Auswirkung':
                    ausmass_pos_tat = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_tat")
                    umfang_pos_tat = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_tat")
                elif auswirkung_art_option == 'Potenzielle Auswirkung':
                    ausmass_pos_pot = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_pos_pot")
                    umfang_pos_pot = st.select_slider("Umfang:", options=["Keine", "Lokal", "Regional", "National", "International", "Global"], key="umfang_pos_pot")
                    behebbarkeit_pos_pot = st.select_slider("Behebbarkeit:", options=["Kein Aufwand", "Leicht zu beheben", "Mit Aufwand", "Mit hohem Aufwand", "Mit sehr hohem Aufwand", "Nicht behebbar"], key="behebbarkeit_pos_pot")
    with col_3_placeholder:
        pass
    with col4:
        st.subheader("Finanzielle Bewertung")
        ausmass_finanziell = st.select_slider("Ausmaß:", options=["Keine", "Minimal", "Niedrig", "Medium", "Hoch", "Sehr hoch"], key="ausmass_finanziell")
        wahrscheinlichkeit_finanziell = st.select_slider("Wahrscheinlichkeit:", options=["Tritt nicht ein", "Unwahrscheinlich", "Eher unwahrscheinlich", "Eher wahrscheinlich", "Wahrscheinlich", "Sicher"], key="wahrscheinlichkeit_finanziell")
        auswirkung_finanziell = st.select_slider("Finanzielle Auswirkung:", options=["Keine", "Sehr gering", "Eher gering", "Eher hoch", "Hoch", "Sehr hoch"], key="auswirkung_finanziell")

    # Store selected values
    ausgewaehlte_werte = {
        "option": option,
        "auswirkung_option": auswirkung_option,
        "auswirkung_art_option": auswirkung_art_option,
        "ausmass_neg_tat": ausmass_neg_tat,
        "umfang_neg_tat": umfang_neg_tat,
        "behebbarkeit_neg_tat": behebbarkeit_neg_tat,
        "ausmass_neg_pot": ausmass_neg_pot,
        "umfang_neg_pot": umfang_neg_pot,
        "behebbarkeit_neg_pot": behebbarkeit_neg_pot,
        "wahrscheinlichkeit_neg_pot": wahrscheinlichkeit_neg_pot,
        "ausmass_pos_tat": ausmass_pos_tat,
        "umfang_pos_tat": umfang_pos_tat,
        "ausmass_pos_pot": ausmass_pos_pot,
        "umfang_pos_pot": umfang_pos_pot,
        "behebbarkeit_pos_pot": behebbarkeit_pos_pot,
        "wahrscheinlichkeit_finanziell": wahrscheinlichkeit_finanziell,
        "ausmass_finanziell": ausmass_finanziell,
        "auswirkung_finanziell": auswirkung_finanziell
    }

    # Proceed with the rest of the logic
    longlist = submit_bewertung(longlist, ausgewaehlte_werte)
    display_grid(longlist)
    

def Scatter_chart():
    # Überprüfen Sie, ob 'selected_data' und 'combined_df' initialisiert wurden
    if "selected_data" not in st.session_state or st.session_state.selected_data.empty or "combined_df" not in st.session_state or st.session_state.combined_df.empty:
        return

    # Stellen Sie sicher, dass 'selected_data' ein DataFrame mit den benötigten Spalten ist
    required_columns = ['ID', 'Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema']
    if all(column in st.session_state.selected_data.columns for column in required_columns):
        selected_columns = st.session_state.selected_data[required_columns]

        # Innerer Join zwischen selected_columns und combined_df auf der Basis der 'ID'
        selected_columns = pd.merge(selected_columns, st.session_state.combined_df[['ID', 'NumericalRating']], on='ID', how='inner')

        # Erstellen Sie eine neue Spalte 'color', die auf dem Wert der Spalte 'Thema' basiert
        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'green'
            elif theme in ['Eigene Belegschaft', 'Arbeitskräfte in der Wertschöpfungskette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'yellow'
            elif theme == 'Unternehmenspolitik':
                return 'blue'
            else:
                return 'gray'

        selected_columns['color'] = selected_columns['Thema'].apply(assign_color)

        # Normalisieren Sie die 'NumericalRating' Werte auf den Bereich [100, 600] und speichern Sie sie in der neuen Spalte 'size'
        min_rating = st.session_state.combined_df['NumericalRating'].min()
        max_rating = st.session_state.combined_df['NumericalRating'].max()
        selected_columns['size'] = ((selected_columns['NumericalRating'] - min_rating) / (max_rating - min_rating)) * (1000 - 100) + 100
        
        # Füllen Sie fehlende Werte in der 'size' Spalte mit 100
        selected_columns['size'] = selected_columns['size'].fillna(100)
        
        # Erstellen Sie ein Scatter-Chart mit Altair
        chart = alt.Chart(selected_columns, width=800, height=600).mark_circle().encode(
            x=alt.X('Score Finanzen', scale=alt.Scale(domain=(0, 100)), title='Finanzielle Wesentlichkeit'),
            y=alt.Y('Score Auswirkung', scale=alt.Scale(domain=(0, 100)), title='Auswirkungsbezogene Wesentlichkeit'),
            color=alt.Color('color:N', scale=alt.Scale(
                domain=['green', 'yellow', 'blue', 'gray'],
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
            size=alt.Size('size', scale=alt.Scale(range=[100, 1000]), legend=None),  # Keine Legende für die Größe der Punkte
            tooltip=required_columns
        )
        
        # Zeigen Sie das Diagramm in Streamlit an
        st.altair_chart(chart)

def display_page():
    tab1, tab2, tab3, tab4 = st.tabs(["Bewertung der Nachhaltigkeitspunkte", "Graphische Übersicht", "Stakeholder", "Gesamtübersicht"])
    with tab1:    
        merge_dataframes()
        display_selected_data()    
        with st.expander("Bewertungen"):
            bewertung()
    with tab2:
        st.write("Graphische Übersicht")
        Scatter_chart()
         
    with tab3:
        with st.expander("In Bewertung aufgenommene Stakeholderpunkte"):
            AgGrid(st.session_state.selected_rows_st)
    with tab4:
        st.write("Gesamtübersicht")