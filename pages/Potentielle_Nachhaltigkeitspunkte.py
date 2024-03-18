import streamlit as st
import pandas as pd

def display_page():
    # Initialisiere den Session State für die hochgeladenen Dateien, falls noch nicht geschehen
    if 'uploaded_files' not in st.session_state:
        st.session_state['uploaded_files'] = None

    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_files = st.file_uploader("Wählen Sie ein Dokument aus", accept_multiple_files=True, key="file_uploader")
    
    with col2:
        if st.button("Analysieren", key="analyze_button"):
            # Speichere die hochgeladenen Dateien im Session State, wenn der Button gedrückt wurde
            st.session_state['uploaded_files'] = uploaded_files
    
    # Verwende die hochgeladenen Dateien aus dem Session State, wenn vorhanden
    if st.session_state['uploaded_files'] is not None:
        for uploaded_file in st.session_state['uploaded_files']:
            bytes_data = uploaded_file.read()
            # Zeige den Dateinamen und den Inhalt hier an
            st.write("Dateiname:", uploaded_file.name)
            # Für eine bessere Handhabung großer Dateien oder binärer Daten, könnte man hier weitere Logik implementieren
            st.write(bytes_data)

    

    html_table = """
        <table>
            <tr>
                <th>ESRS</th>
                <th>Topic</th>
                <th>Sub Topic</th>
                <th>Sub-sub-Topic</th>
            </tr>
            <tr>
                <td rowspan="3">E1</td>
                <td rowspan="3">Climate Change</td>
                <td>Climate change adaptation</td>
                <td>Detail 1 für Climate change adaptation</td>
            </tr>
            <tr>
                <td>Climate change mitigation</td>
                <td>Detail 2 für Climate change mitigation</td>
            </tr>
            <tr>
                <td>Energy</td>
                <td>Detail 3 für Energy</td>
            </tr>
            <tr>
                <td rowspan="5">E2</td>
                <td rowspan="5">Pollution</td>
                <td>Air pollution</td>
                <td>Detail 1 für Air pollution</td>
            <tr>
                <td>Water pollution</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Soil pollution</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Pollution of living organisms and food resources</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Pollution: Substances of concern</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td rowspan="5">E3</td>
                <td rowspan="5">Water and marine resources</td>
                <td>Water withdrawals</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Water consumption</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Water use</td>  
                <td>Detail 1 für Air pollution</td>  
            </tr>
            <tr>
                <td>Water discharges to water bodies and oceans</td>
                <td>Detail 1 für Air pollution</td>
            </tr>
            <tr>
                <td>Degradation of aquatic/marine habitats and intensity of impact on marine resources</td>
                <td>Detail 1 für Air pollution</td>
            </tr> 
    </table>
    """
    # Verwende HTML, um die Inhalte anzuzeigen
    st.markdown(html_table, unsafe_allow_html=True)
  
   