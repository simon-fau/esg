import streamlit as st
import pandas as pd
import pickle
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from openpyxl import load_workbook
import shutil
import io

# Constants
STATE_FILE = 'session_state_bottom_up_eigene.pkl'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'Templates', 'Stakeholder_Input_Vorlage_V1.xlsx')
TEMP_EXCEL_PATH = 'Stakeholder_Input_Vorlage_V1_Copy.xlsx'

# Session state management
def load_session_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_session_state(state):
    current_state = load_session_state()
    combined_state = {**current_state, **state}
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(combined_state, f)

# Initialize session state
loaded_state = load_session_state()
if 'df2' not in st.session_state:
    st.session_state.df2 = pd.DataFrame(columns=["Thema", "Unterthema", "Unter-Unterthema"])
if 'df2' in loaded_state:
    st.session_state.df2 = loaded_state['df2']

# UI Functions
def add_entry_form():
    with st.sidebar:
        st.markdown("---")
        st.write("**Inhalte hinzufügen**")
        with st.form(key='add_entry_form', border=False):
            thema = st.selectbox('Thema auswählen', options=[
                'Klimawandel', 'Umweltverschmutzung', 'Wasser- und Meeresressourcen', 
                'Biologische Vielfalt und Ökosysteme', 'Kreislaufwirtschaft', 'Eigene Belegschaft',
                'Arbeitskräfte in der Wertschöpfungskette', 'Betroffene Gemeinschaften',
                'Verbraucher und End-nutzer', 'Unternehmenspolitik'
            ], index=0, key='thema')
            
            unterthema_options = get_unterthema_options(thema)
            unterthema = st.selectbox('Unterthema auswählen', options=unterthema_options, index=0, key='unterthema')
            unter_unterthema = st.text_input('Unter-Unterthema eingeben', key='unter_unterthema')
            
            submitted = st.form_submit_button('➕ Hinzufügen')
            if submitted:
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

def add_row(thema, unterthema, unter_unterthema):
    empty_row_index = st.session_state.df2[(st.session_state.df2["Thema"] == "") & (st.session_state.df2["Unterthema"] == "") & (st.session_state.df2["Unter-Unterthema"] == "")].first_valid_index()
    if empty_row_index is not None:
        st.session_state.df2.at[empty_row_index, "Thema"] = thema
        st.session_state.df2.at[empty_row_index, "Unterthema"] = unterthema
        st.session_state.df2.at[empty_row_index, "Unter-Unterthema"] = unter_unterthema
    else:
        new_row = {"Thema": thema, "Unterthema": unterthema, "Unter-Unterthema": unter_unterthema}
        st.session_state.df2 = st.session_state.df2._append(new_row, ignore_index=True)
    save_session_state({'df2': st.session_state.df2})

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
    else:
        st.info("Keine Daten vorhanden.")
    
    if st.button('➕ Leere Zeile hinzufügen', key='add_empty_row'):
        add_empty_row()
    
    if st.button('🗑️ Ausgewählte Zeilen löschen', key='delete_rows'):
        delete_selected_rows(grid_response)
    
    if st.button('💾 Änderungen speichern', key='save_changes'):
        st.session_state.df2 = grid_response['data'].set_index('index')
        save_session_state({'df2': st.session_state.df2})
        st.success('Änderungen erfolgreich gespeichert.')
    
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
    st.experimental_rerun()

def delete_selected_rows(grid_response):
    selected_rows = grid_response['selected_rows']
    selected_indices = [row['index'] for row in selected_rows]
    st.session_state.df2 = st.session_state.df2.drop(selected_indices)
    save_session_state({'df2': st.session_state.df2})
    st.experimental_rerun()

def transfer_data_to_excel(dataframe):
    shutil.copyfile(TEMPLATE_PATH, TEMP_EXCEL_PATH)
    workbook = load_workbook(TEMP_EXCEL_PATH)
    sheet = workbook['Intern']
    first_empty_row = 2
    
    for index, row in dataframe.iterrows():
        sheet[f'A{first_empty_row}'] = row['Thema']
        sheet[f'B{first_empty_row}'] = row['Unterthema']
        sheet[f'C{first_empty_row}'] = row['Unter-Unterthema']
        first_empty_row += 1

    workbook.save(TEMP_EXCEL_PATH)
    st.success('Inhalte erfolgreich zur Excel-Datei hinzugefügt.')

def download_excel():
    workbook = load_workbook(TEMP_EXCEL_PATH)
    with io.BytesIO() as virtual_workbook:
        workbook.save(virtual_workbook)
        virtual_workbook.seek(0)
        return virtual_workbook.read()

def check_abgeschlossen_intern():
    if 'checkbox_state_4' not in st.session_state:
        st.session_state['checkbox_state_4'] = False
    
    st.session_state['checkbox_state_4'] = st.checkbox("Abgeschlossen", value=st.session_state['checkbox_state_4'])
    save_session_state({'checkbox_state_4': st.session_state['checkbox_state_4']})

def display_page():
    col1, col2 = st.columns([7, 1])
    with col1:
        st.header("Interne Nachhaltigkeitspunkte")
    with col2:
        container = st.container()
        with container:
            check_abgeschlossen_intern()
        
    st.markdown("""
        Hier können Sie unternehmensspezifische Nachhaltigkeitspunkte hinzufügen und verwalten. Nutzen Sie die Dropdown-Menüs und Textfelder in der Sidebar oder tragen Sie Inhalte direkt in die Tabelle ein. Achten Sie darauf, die Inhalte mit Enter zu bestätigen und den Speicher-Button zu drücken. Aktualisieren Sie anschließend die Excel-Datei, laden Sie sie herunter und leiten Sie diese an Ihre Stakeholder weiter.
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


