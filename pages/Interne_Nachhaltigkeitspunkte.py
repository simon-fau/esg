import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from openpyxl import load_workbook
import shutil
import io

# Constants
STATE_FILE = 'session_states.pkl'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'Templates', 'Stakeholder_Input_Vorlage_V1.xlsx')
TEMP_EXCEL_PATH = 'Stakeholder_Input_Vorlage_V1_Copy.xlsx'

# Session State Functions
def load_session_state(file_path=STATE_FILE):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}

def save_session_state(data, file_path=STATE_FILE):
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    except pickle.PicklingError:
        st.error("PicklingError: Die Daten konnten nicht korrekt gespeichert werden.")
    except Exception as e:
        st.error(f"Ein unerwarteter Fehler ist beim Speichern der Daten aufgetreten: {str(e)}")

def initialize_session_state():
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])

def check_abgeschlossen_intern():
    if 'checkbox_state_4' not in st.session_state:
        st.session_state['checkbox_state_4'] = False
    
    st.session_state['checkbox_state_4'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_4'])
    save_session_state({'checkbox_state_4': st.session_state['checkbox_state_4']})

# UI Functions
def add_entry_form():
    with st.sidebar:
        st.markdown("---")
        st.write("**Inhalte hinzufügen**")

        # Erste Selectbox für die Auswahl des Themas
        thema = st.selectbox('Thema auswählen', options=[
            'Klimawandel', 'Umweltverschmutzung', 'Wasser- und Meeresressourcen', 
            'Biologische Vielfalt und Ökosysteme', 'Kreislaufwirtschaft', 'Eigene Belegschaft',
            'Arbeitskräfte in der Wertschöpfungskette', 'Betroffene Gemeinschaften',
            'Verbraucher und End-nutzer', 'Unternehmenspolitik'
        ], index=0)

        # Zweite Selectbox für die dynamisch angepasste Auswahl des Unterthemas
        unterthema_options = get_unterthema_options(thema)
        unterthema = st.selectbox('Unterthema auswählen', options=unterthema_options, index=0)
        
        # Textfeld für die Eingabe des Unter-Unterthemas
        unter_unterthema = st.text_input('Unter-Unterthema eingeben')
        
        # Submit-Button außerhalb eines Formulars
        if st.button('➕ Hinzufügen'):
            add_row(thema, unterthema, unter_unterthema)

def get_unterthema_options(thema):
    options = {
        'Klimawandel': ['Anpassung an den Klimawandel', 'Klimaschutz', 'Energie'],
        'Umweltverschmutzung': ['Luftverschmutzung', 'Wasserverschmutzung', 'Bodenverschmutzung', 'Verschmutzung von lebenden Organismen und Nahrungsressourcen', 'Besorgniserregende Stoffe', 'Mikroplastik'],
        'Wasser- und Meeresressourcen': ['Wasser', 'Meeresressourcen'],
        'Biologische Vielfalt und Ökosysteme': ['Direkte Ursachen des Biodiversitätsverlusts', 'Auswirkungen auf den Zustand der Arten', 'Auswirkungen auf den Umfang und den Zustand von Ökosystemen'],
        'Kreislaufwirtschaft': ['Auswirkungen und Abhängigkeiten von Ökosystemdienstleistungen', 'Ressourcenzuflüsse, einschließlich Ressourcennutzung', 'Ressourcenabflüsse im Zusammenhang mit Produkten und Dienstleistungen', 'Abfälle'],
        'Eigene Belegschaft': ['Arbeitsbedingungen', 'Gleichbehandlung und Chancengleichheit für alle', 'Sonstige arbeitsbezogene Rechte'],
        'Arbeitskräfte in der Wertschöpfungskette': ['Arbeitsbedingungen', 'Gleichbehandlung und Chancengleichheit für alle', 'Sonstige arbeitsbezogene Rechte'],
        'Betroffene Gemeinschaften': ['Wirtschaftliche, soziale und kulturelle Rechte von Gemeinschaften', 'Bürgerrechte und politische Rechte von Gemeinschaften', 'Rechte indigener Völker'],
        'Verbraucher und End-nutzer': ['Informationsbezogene Auswirkungen für Verbraucher und/oder Endnutzer', 'Persönliche Sicherheit von Verbrauchern und/oder Endnutzern', 'Soziale Inklusion von Verbrauchern und/oder Endnutzern'],
        'Unternehmenspolitik': ['Unternehmenskultur', 'Schutz von Hinweisgebern (Whistleblowers)', 'Tierschutz', 'Politisches Engagement und Lobbytätigkeiten', 'Management der Beziehungen zu Lieferanten, einschließlich Zahlungspraktiken', 'Korruption und Bestechung']
    }
    return options.get(thema, [])

# Example of adding a row to the DataFrame in the session state
def add_row(thema, unterthema, unter_unterthema):
    if 'df2' not in st.session_state:
        st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
        
    empty_row_index = st.session_state.df2[(st.session_state.df2["Thema"] == "") & (st.session_state.df2["Unterthema"] == "") & (st.session_state.df2["Unter-Unterthema"] == "")].first_valid_index()
    if empty_row_index is not None:
        st.session_state.df2.at[empty_row_index, "Thema"] = thema
        st.session_state.df2.at[empty_row_index, "Unterthema"] = unterthema
        st.session_state.df2.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
    else:
        new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
        st.session_state.df2 = st.session_state.df2._append(new_row, ignore_index=True)

def display_data_table():
    if not st.session_state.df2.empty:
        grid_options = configure_grid_options(st.session_state.df2)
        grid_response = AgGrid(
            st.session_state.df2.reset_index(),
            gridOptions=grid_options,
            fit_columns_on_grid_load=True,
            height=300,
            width='100%',
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
            return_mode=DataReturnMode.__members__['AS_INPUT'],
            selection_mode='multiple'
        )

        # Only display these buttons when there is data in df2
        if st.button('Ausgewählte Zeilen löschen', key='delete_rows'):
            delete_selected_rows(grid_response)
        
        if st.button('Änderungen speichern', key='save_changes'):
            st.session_state.df2 = grid_response['data'].set_index('index')
            save_session_state({'df2': st.session_state.df2})
            st.success('Änderungen erfolgreich gespeichert.')
    else:
        st.info("Keine Daten vorhanden.")
    
    # The "add empty row" button is always displayed
    if st.button('Leere Zeile hinzufügen', key='add_empty_row'):
        add_empty_row()


def configure_grid_options(dataframe):
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    gb.configure_default_column(editable=True, resizable=True, sortable=True, filterable=True)
    gb.configure_grid_options(domLayout='autoHeight', enableRowId=True, rowId='index')
    grid_options = gb.build()
    grid_options['columnDefs'] = [{'checkboxSelection': True, 'headerCheckboxSelection': True, 'width': 50}] + grid_options['columnDefs']
    return grid_options

def add_empty_row():
    empty_row = {"Thema": "", "Unterthema": "", "Unter-Unterthema": ""}
    st.session_state.df2 = st.session_state.df2._append(empty_row, ignore_index=True)
    save_session_state({'df2': st.session_state.df2})
    st.rerun()

def delete_selected_rows(grid_response):
    selected_rows = grid_response['selected_rows']
    selected_indices = [row['index'] for row in selected_rows]
    st.session_state.df2 = st.session_state.df2.drop(selected_indices)
    save_session_state({'df2': st.session_state.df2})
    st.rerun()

def transfer_data_to_excel(dataframe):
    # Copy the template file to ensure rules are maintained
    shutil.copyfile(TEMPLATE_PATH, TEMP_EXCEL_PATH)
    
    # Load the workbook and target sheet
    workbook = load_workbook(TEMP_EXCEL_PATH)
    sheet = workbook['Interne Nachhaltigkeitspunkte']

    # Find the first empty row in the sheet (assumes first column is used)
    first_empty_row = None
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        if row[0] is None:
            first_empty_row = row[0].row
            break

    # If no empty row is found, append after the last used row
    if first_empty_row is None:
        first_empty_row = sheet.max_row + 1

    # Write data to the sheet, preserving existing rules (formulas, validations)
    for index, row in dataframe.iterrows():
        # Write data into empty rows
        sheet[f'A{first_empty_row}'] = row['Thema']
        sheet[f'B{first_empty_row}'] = row['Unterthema']
        sheet[f'C{first_empty_row}'] = row['Unter-Unterthema']
        first_empty_row += 1

    # Save the updated Excel file
    workbook.save(TEMP_EXCEL_PATH)
    st.success('Inhalte erfolgreich zur Excel-Datei hinzugefügt.')



def download_excel():
    workbook = load_workbook(TEMP_EXCEL_PATH)
    with io.BytesIO() as virtual_workbook:
        workbook.save(virtual_workbook)
        virtual_workbook.seek(0)
        return virtual_workbook.read()

# Main display function
def display_page():
    initialize_session_state()  # Initialize session state variables
    col1, col2 = st.columns([7, 1])
    
    with col1:
        st.header("Interne Nachhaltigkeitspunkte")
    with col2:
        container = st.container()
        with container:
            check_abgeschlossen_intern()
        
    st.markdown("""
        
Hier können Sie unternehmensspezifische Nachhaltigkeitspunkte hinzufügen und verwalten. Nutzen Sie die Dropdown-Menüs und Textfelder in der Sidebar oder fügen Sie Inhalte direkt in die Tabelle ein. Achten Sie darauf, bei der direkten Eingabe in die Tabelle die Inhalte mit Enter zu bestätigen, damit der rote Rahmen um die Zelle verschwindet. Speichern Sie anschließend die Änderungen.
    """)
    
    add_entry_form()
    display_data_table()
    
    st.sidebar.markdown("---")
    st.sidebar.write("**Excel-Datei für Stakeholderumfrage**")
    
    if st.sidebar.button('🔃 Excel aktualisieren'):
        transfer_data_to_excel(st.session_state.df2)
    
    if st.sidebar.download_button(
        label="⬇️ Excel-Datei herunterladen",
        data=download_excel(),
        file_name="Stakeholder_Input.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        st.success("Download gestartet!")

