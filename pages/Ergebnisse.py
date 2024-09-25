import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import altair as alt
from vl_convert import vl_convert as altair_save
from openpyxl.drawing.image import Image as ExcelImage
import os
from pages.Themenspezifische_ESRS import calculate_percentages
from pages.Longlist import bewertung_Uebersicht_Nein

# Function to create the Excel file based on filtered_df and Allgemeine_Angaben from session_state
def Ausleitung_Excel():
    # Check if the filtered_df exists in the session state
    if 'filtered_df' not in st.session_state:
        st.error("Es gibt keine gefilterten Daten in der Session-State.")
        return

    # Load the existing 'Ergebnisse.xlsx' file
    template_file = 'Ergebnisse.xlsx'
    
    if not os.path.exists(template_file):
        st.error(f"Die Datei {template_file} wurde nicht gefunden.")
        return

    # Create a new workbook based on the template
    try:
        workbook = load_workbook(template_file)
    except Exception as e:
        st.error(f"Fehler beim Laden der Excel-Datei: {str(e)}")
        return
    
    #----------Wesentlichkeitsmatrix der Shortlist----------#

    # Check if the data required for the chart is available in session_state
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Prepare the data
        selected_columns_df = pd.DataFrame(selected_columns)
        columns_to_display = ['Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        
        # Check if Thema column exists and handle missing values
        if 'Thema' not in selected_columns_df.columns:
            st.error("Die Spalte 'Thema' fehlt in den Daten.")
            return
        
        selected_columns_df = selected_columns_df.dropna(subset=['Thema'])
        selected_columns_df['Thema'] = selected_columns_df['Thema'].astype(str)

        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'
        
        selected_columns_df['color'] = selected_columns_df['Thema'].apply(assign_color)

        # Create the base scatter chart
        scatter = alt.Chart(selected_columns_df, width=1000, height=800).mark_circle().encode(
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
            tooltip=['Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        # Add red diagonal line
        line = alt.Chart(pd.DataFrame({
            'x': [0, st.session_state['intersection_value']],
            'y': [st.session_state['intersection_value'], 0]
        })).mark_line(color='red').encode(
            x='x:Q',
            y='y:Q'
        )

        # Add shaded area under the line
        area = alt.Chart(pd.DataFrame({
            'x': [0, st.session_state['intersection_value']],
            'y': [st.session_state['intersection_value'], 0]
        })).mark_area(opacity=0.3, color='lightcoral').encode(
            x='x:Q',
            y='y:Q'
        )

        # Combine scatter, line, and area
        chart = area + scatter + line

        # Save the chart as a PNG file using vl-convert
        chart_png_file = 'scatter_chart.png'
        chart.save(chart_png_file, format='png')
        
        chart_sheet = workbook['Shortlist']
        chart_sheet['G1'] = "Schwellenwert für wesentliche Themen:"
        chart_sheet['G2'] = "Schwellenwert für Stakeholder Wichtigkeit:"
        chart_sheet['G3'] = "Wesentlichkeitsmatrix der Shortlist:"

        # Insert the PNG image into the Excel sheet
        img = ExcelImage(chart_png_file)
        img.width, img.height = 600, 400  # Set desired size of the image
        chart_sheet.add_image(img, 'G5')  # Place the image in cell B2
        chart_sheet['K1'] = st.session_state['intersection_value']  # Insert the intersection value
        chart_sheet['K2'] = st.session_state['stakeholder_importance_value']

    else:
        st.info("Keine Daten für die Grafik vorhanden.")

    #----------Wesentlichkeitsmatrix ohne Schwellenwerte----------#

     # Check if the data required for the chart is available in session_state
    if 'selected_columns' in st.session_state and len(st.session_state['selected_columns']) > 0:
        selected_columns = st.session_state['selected_columns']
        
        # Prepare the data
        selected_columns_df = pd.DataFrame(selected_columns)
        columns_to_display = ['Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        
        # Check if Thema column exists and handle missing values
        if 'Thema' not in selected_columns_df.columns:
            st.error("Die Spalte 'Thema' fehlt in den Daten.")
            return
        
        selected_columns_df = selected_columns_df.dropna(subset=['Thema'])
        selected_columns_df['Thema'] = selected_columns_df['Thema'].astype(str)

        def assign_color(theme):
            if theme in ['Klimawandel', 'Umweltverschmutzung', 'Wasser- & Meeresressourcen', 'Biodiversität', 'Kreislaufwirtschaft']:
                return 'Environmental'
            elif theme in ['Eigene Belegschaft', 'Belegschaft Lieferkette', 'Betroffene Gemeinschaften', 'Verbraucher und Endnutzer']:
                return 'Social'
            elif theme == 'Unternehmenspolitik':
                return 'Governance'
            else:
                return 'Sonstige'
        
        selected_columns_df['color'] = selected_columns_df['Thema'].apply(assign_color)

        # Create the base scatter chart
        scatter = alt.Chart(selected_columns_df, width=1000, height=800).mark_circle().encode(
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
            tooltip=['Score Finanzen', 'Score Auswirkung', 'Thema', 'Unterthema', 'Unter-Unterthema', 'Stakeholder Wichtigkeit']
        )

        # Combine scatter, line, and area
        chart = scatter

        # Save the chart as a PNG file using vl-convert
        chart_png_file_2 = 'scatter_chart_without_thresholds.png'
        chart.save(chart_png_file_2, format='png')
        
        chart_sheet_2 = workbook['Übersicht']

        # Insert the PNG image into the Excel sheet
        img = ExcelImage(chart_png_file_2)
        img.width, img.height = 600, 400  # Set desired size of the image
        chart_sheet_2.add_image(img, 'C19')  # Place the image in cell B2

    else:
        st.info("Keine Daten für die Grafik vorhanden.")

    #----------Fortschritt WA----------#

    # Select the 'Übersicht' worksheet
    overview_sheet = workbook['Übersicht']

    # Update 'Übersicht' sheet starting at C3 with progress data from Wesentlichkeitsanalyse
    session_states_to_check = [
        ('checkbox_state_1', '1. Stakeholder Management'),
        ('checkbox_state_2', '2. Stakeholder Auswahl'),
        ('checkbox_state_3', '3. Themenspezifische ESRS'),
        ('checkbox_state_4', '4. Interne Nachhaltigkeitspunkte'),
        ('checkbox_state_5', '5. Externe Nachhaltigkeitspunkte'),
        ('checkbox_state_6', '6. Bewertung der Longlist'),
        ('checkbox_state_7', '7. Shortlist')
    ]
    
    row_start = 3  # Start from C3
    col_name = 'B'  # Task names column
    col_status = 'C'  # Status column
    
    # Retrieve and write the current progress status to Excel
    completed_count = 0
    for key, name in session_states_to_check:
        overview_sheet[f'{col_name}{row_start}'] = name
        
        if key == 'checkbox_state_5':  # Custom handling for checkbox_state_5
            if 'Einbezogene_Stakeholder' in st.session_state and 'sidebar_companies' in st.session_state:
                if not st.session_state['Einbezogene_Stakeholder'] and not st.session_state['sidebar_companies']:
                    overview_sheet[f'{col_status}{row_start}'] = "✘"
                elif not st.session_state['Einbezogene_Stakeholder']:
                    overview_sheet[f'{col_status}{row_start}'] = "✔"
                    completed_count += 1
                else:
                    count = len([opt for opt in st.session_state['Einbezogene_Stakeholder'] if opt not in st.session_state['sidebar_companies']])
                    if st.session_state.get(key) == True:
                        overview_sheet[f'{col_status}{row_start}'] = "✔"
                        completed_count += 1
                    else:
                        overview_sheet[f'{col_status}{row_start}'] = f"Es fehlt noch {count} Stakeholder."
            else:
                overview_sheet[f'{col_status}{row_start}'] = "✘"
        elif key == 'checkbox_state_3':  # Custom handling for checkbox_state_3
            if st.session_state.get(key) == True:
                overview_sheet[f'{col_status}{row_start}'] = "✔"
                completed_count += 1
            else:
                if 'checkbox_count' in st.session_state and st.session_state['checkbox_count'] > 0:
                    percentage_missing = calculate_percentages()  # Assuming this function is available
                    overview_sheet[f'{col_status}{row_start}'] = f"Es fehlen noch {percentage_missing}%."
                else:
                    overview_sheet[f'{col_status}{row_start}'] = "✘"
        elif key == 'checkbox_state_6':  # Custom handling for checkbox_state_6
            if 'longlist' in st.session_state and not st.session_state['longlist'].empty:
                if st.session_state.get(key) == True:
                    overview_sheet[f'{col_status}{row_start}'] = "✔"
                    completed_count += 1
                else:
                    nein_prozent = bewertung_Uebersicht_Nein()  # Assuming this function is available
                    overview_sheet[f'{col_status}{row_start}'] = f"Es fehlen noch {nein_prozent}%."
            else:
                overview_sheet[f'{col_status}{row_start}'] = "✘"
        else:  # Default handling for other states
            if st.session_state.get(key) == True:
                overview_sheet[f'{col_status}{row_start}'] = "✔"
                completed_count += 1
            else:
                overview_sheet[f'{col_status}{row_start}'] = "✘"
        
        row_start += 1

    #----------Fortschritt Themenspezifische ESRS----------#

    # Add checkbox count and percentage to the 'Übersicht' sheet in cell C11
    if 'checkbox_count' in st.session_state:
        checkbox_count = st.session_state['checkbox_count']
        total_checkboxes = 93
        number_of_missing_checkboxes = total_checkboxes - checkbox_count
        
        # Calculate percentage complete
        percentage_complete = round((checkbox_count / total_checkboxes) * 100, 0)
        
        # Write checkbox count in C11
        overview_sheet['C11'] = checkbox_count
        
        # Write the remaining checkbox count and percentage complete
        overview_sheet['C12'] = number_of_missing_checkboxes

    #----------Anzahl Shortlist Punkte----------#

    # Add Shortlist count to the 'Übersicht' sheet in cell C17
    count_shortlist = 0  # Default to 0
    if 'filtered_df' in st.session_state and not st.session_state['filtered_df'].empty:
        count_shortlist = len(st.session_state['filtered_df'])
    
    # Write the Shortlist count in C17
    overview_sheet['C17'] = count_shortlist

    #----------Fortschritt Longlist----------#

    # Add Longlist count to the 'Übersicht' sheet in cell C12
    count_longlist = 0  # Default to 0
    if 'combined_df' in st.session_state and not st.session_state.combined_df.empty:
        count_longlist = len(st.session_state.combined_df)
        
    # Write the Longlist count in C12
    overview_sheet['C14'] = count_longlist 

    #----------Fortschritt Bewertungen in der Longlist----------#

    # Add Ja and Nein Bewertungen to the 'Übersicht' sheet in C13 and D13
    if 'longlist' in st.session_state and not st.session_state['longlist'].empty:
        # Count the number of Bewertungen in the Longlist
        bewertung_counts = st.session_state['longlist']['Bewertet'].value_counts()

        # Calculate Ja Bewertungen
        ja_bewertungen = bewertung_counts.get('Ja', 0)

        # Write the counts to cells C13 and D13
        overview_sheet['C15'] = ja_bewertungen

    #----------Shortlist Sheet----------#

    # Ensure that the 'Shortlist' sheet exists
    if 'Shortlist' not in workbook.sheetnames:
        st.error("Das Blatt 'Shortlist' existiert nicht in der Datei.")
        return

    # Select the 'Shortlist' worksheet
    shortlist_sheet = workbook['Shortlist']

    # Retrieve the filtered data from session_state
    dataframe = st.session_state.filtered_df

    # Write the filtered data (Thema, Unterthema, Unter-Unterthema) into the 'Shortlist' sheet
    first_empty_row = 1
    while shortlist_sheet[f'A{first_empty_row}'].value or shortlist_sheet[f'B{first_empty_row}'].value or shortlist_sheet[f'C{first_empty_row}'].value:
        first_empty_row += 1

    # Schreibe die gefilterten Daten (Thema, Unterthema, Unter-Unterthema) in das 'Shortlist'-Blatt
    for index, row in dataframe.iterrows():
        shortlist_sheet[f'A{first_empty_row}'] = row['Thema']
        shortlist_sheet[f'B{first_empty_row}'] = row['Unterthema']
        shortlist_sheet[f'C{first_empty_row}'] = row['Unter-Unterthema']
        shortlist_sheet[f'D{first_empty_row}'] = row['Score Finanzen']
        shortlist_sheet[f'E{first_empty_row}'] = row['Score Auswirkung']
        first_empty_row += 1

    #----------Allgemeine Angaben Sheet----------#

    # Check if Antwort exists in session state
    if 'Antwort' in st.session_state:
        # Ensure that the 'Allgemeine Angaben' sheet exists
        if 'Allgemeine Angaben' not in workbook.sheetnames:
            st.error("Das Blatt 'Allgemeine Angaben' existiert nicht in der Datei.")
            return

        # Select the 'Allgemeine Angaben' worksheet
        general_sheet = workbook['Allgemeine Angaben']

        # Write Antwort data into column C starting at row 2
        antwort_data = st.session_state.Antwort
        row_index = 2  # Start from row 2

        for entry in antwort_data:
            general_sheet[f'C{row_index}'] = entry
            row_index += 1

    #----------Mindestangaben Sheet----------#

    # Add Mindestangaben to the "Mindestangaben" sheet if it exists
    if 'Antworten_MDR' in st.session_state:
        if 'Mindestangaben' not in workbook.sheetnames:
            st.error("Das Blatt 'Mindestangaben' existiert nicht in der Datei.")
            return
        
        # Select the 'Mindestangaben' worksheet
        min_sheet = workbook['Mindestangaben']

        # Write the Antworten_MDR data into column C starting at row 2
        mdr_data = st.session_state['Antworten_MDR']
        row_index = 2  # Start from row 2 in the Mindestangaben sheet

        for entry in mdr_data:
            min_sheet[f'C{row_index}'] = entry
            row_index += 1

    #----------Stakeholder Ranking----------#

    # Check if the 'Stakeholder' sheet exists
    if 'Stakeholder' not in workbook.sheetnames:
        st.error("Das Blatt 'Stakeholder' existiert nicht in der Datei.")
        return
    
    # Select the 'Stakeholder' worksheet
    stakeholder_sheet = workbook['Stakeholder']
    
    # Get the ranking DataFrame from session_state
    if 'ranking_table' not in st.session_state:
        st.error("Es gibt keine ranking_table in der Session-State.")
        return
    
    ranking_table = st.session_state['ranking_table']

    # Write the ranking_table DataFrame to 'Stakeholder' sheet starting at row 2
    first_empty_row_stakeholder = 3 # Start from the first empty row

    for index, row in ranking_table.iterrows():
        stakeholder_sheet[f'A{first_empty_row_stakeholder}'] = row['Ranking']
        stakeholder_sheet[f'B{first_empty_row_stakeholder}'] = row['Gruppe']
        stakeholder_sheet[f'C{first_empty_row_stakeholder}'] = row['Score']
        first_empty_row_stakeholder += 1


    # Export the 'table_right_df' DataFrame to 'STakeholder' starting at cell E2
    if 'Einbezogene_Stakeholder' in st.session_state and st.session_state.Einbezogene_Stakeholder:
        # Filter the ranking_table for included stakeholders
        table_right_df = st.session_state['ranking_table'][st.session_state['ranking_table']['Gruppe'].isin(st.session_state.Einbezogene_Stakeholder)]

        # Start writing to column E, row 2
        row = 3
        for index, data in table_right_df.iterrows():
            stakeholder_sheet[f'E{row}'] = data['Ranking']
            stakeholder_sheet[f'F{row}'] = data['Gruppe']
            stakeholder_sheet[f'G{row}'] = data['Score']
            row += 1

    #----------Externe Nachhaltigkeitspunkte----------#

    # Export the 'stakeholder_punkte_filtered' DataFrame to 'Externe Nachhaltigkeitspunkte' starting at row 2
    if 'stakeholder_punkte_filtered' in st.session_state:
        # Ensure that the 'Externe Nachhaltigkeitspunkte' sheet exists
        if 'Externe Nachhaltigkeitspunkte' not in workbook.sheetnames:
            # Create a new sheet if it doesn't exist
            workbook.create_sheet('Externe Nachhaltigkeitspunkte')

        # Select the 'Externe Nachhaltigkeitspunkte' worksheet
        sustainability_sheet = workbook['Externe Nachhaltigkeitspunkte']

        # Write the DataFrame to the sheet starting at row 2
        punkt_df = st.session_state['stakeholder_punkte_filtered']

        # Write specific columns to the Excel sheet
        row_start = 2
        for idx, row in punkt_df.iterrows():
            sustainability_sheet[f'A{row_start}'] = row.get('Platzierung', '')  # Platzierung in column A
            sustainability_sheet[f'B{row_start}'] = row.get('Thema', '')        # Thema in column B
            sustainability_sheet[f'C{row_start}'] = row.get('Unterthema', '')   # Unterthema in column C
            sustainability_sheet[f'D{row_start}'] = row.get('Unter-Unterthema', '') # Unter-Unterthema in column D
            sustainability_sheet[f'E{row_start}'] = row.get('Stakeholder Bew Auswirkung', '')       
            sustainability_sheet[f'F{row_start}'] = row.get('Stakeholder Bew Finanzen', '')
            sustainability_sheet[f'G{row_start}'] = row.get('Stakeholder Gesamtbew', '')
            sustainability_sheet[f'H{row_start}'] = row.get('Stakeholder', '')
            sustainability_sheet[f'I{row_start}'] = row.get('Quelle', '')       # Quelle in column J
            row_start += 1

    #----------Longlist----------#

    # Ensure that the 'Longlist' sheet exists
    if 'Longlist' not in workbook.sheetnames:
        # Create a new sheet if it doesn't exist
        workbook.create_sheet('Longlist')

    # Select the 'Longlist' worksheet
    longlist_sheet = workbook['Longlist']

    # Check if longlist exists in the session state
    if 'longlist' in st.session_state:
        # Retrieve longlist from session state
        longlist_df = st.session_state['longlist']

        for r_idx, row in longlist_df.iterrows():
            for c_idx, value in enumerate(row, start=1):
                longlist_sheet.cell(row=r_idx + 2, column=c_idx, value=value)  # Write data starting from row 2
    else:
        st.info("Keine Daten für 'Longlist' vorhanden.")

       #----------Interne Nachhaltigkeitspunkte----------#

    # Ensure that the 'Interne Nachhaltigkeitspunkte' sheet exists
    if 'Interne Nachhaltigkeitspunkte' not in workbook.sheetnames:
        # Create a new sheet if it doesn't exist
        workbook.create_sheet('Interne Nachhaltigkeitspunkte')

    # Select the 'Interne Nachhaltigkeitspunkte' worksheet
    internal_sustainability_sheet = workbook['Interne Nachhaltigkeitspunkte']

    # Check if df2 exists in the session state
    if 'df2' in st.session_state:
        # Retrieve df2 from session state
        df2 = st.session_state['df2']

        # Write the data to the 'Interne Nachhaltigkeitspunkte' sheet
        for r_idx, row in df2.iterrows():
            for c_idx, value in enumerate(row, start=1):
                internal_sustainability_sheet.cell(row=r_idx + 2, column=c_idx, value=value)  # Write data starting from row 3
    else:
        st.info("Keine Daten für 'Interne Nachhaltigkeitspunkte' vorhanden.")

    # Save the new Excel file with the name 'Ergebnisse_WA.xlsx'
    output_file = 'Ergebnisse_WA.xlsx'
    
    try:
        workbook.save(output_file)
        
        # Provide a download link
        with open(output_file, 'rb') as file:
            btn = st.download_button(
                label="Ergebnisse herunterladen",
                data=file,
                file_name=output_file,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    except Exception as e:
        st.error(f"Fehler beim Speichern der Excel-Datei: {str(e)}")

def display_page():
    st.title("Excel-Ausleitung")
    st.write("Klicken Sie auf den Button, um die Daten in eine Excel-Datei zu exportieren.")
    Ausleitung_Excel()