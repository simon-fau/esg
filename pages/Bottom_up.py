import streamlit as st

def create_table_with_rowspan():
    # Beginn der Tabelle mit HTML
    table_html = """
    <style>
        table {
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 5px;
            text-align: left;
        }
        th {
            background-color: #f0f0f0;
        }
    </style>
    <table>
        <tr>
            <th rowspan="3">ESRS E1<br/>Klimawandel</th>
            <td>Anpassung an den Klimawandel</td>
        </tr>
        <tr><td>Klimaschutz</td></tr>
        <tr><td>Energie</td></tr>
        <tr>
            <th rowspan="7">ESRS E2<br/>Umweltverschmutzung</th>
            <td>Luftverschmutzung</td>
        </tr>
        <tr><td>Wasserverschmutzung</td></tr>
        <tr><td>Bodenverschmutzung</td></tr>
        <tr><td>Verschmutzung von lebenden Organismen und Nahrungsressourcen</td></tr>
        <tr><td>Besorgniserregende Stoffe</td></tr>
        <tr><td>Besonders besorgniserregende Stoffe</td></tr>
        <tr><td>Mikroplastik</td></tr>
        <tr>
            <th rowspan="5">ESRS E3<br/>Wasser- und Meeresressourcen</th>
            <td>Wasser</td>
            <td>Wasserverbrauch</td>
        </tr>
        <tr><td>Meeresressourcen</td><td>Wasserentnahme</td></tr>
        <tr><td></td><td>Ableitung von Wasser</td></tr>
        <tr><td></td><td>Ableitung von Wasser in die Ozeane</td></tr>
        <tr><td></td><td>Gewinnung und Nutzung von Meeresressourcen</td></tr>
        <!-- ESRS E4 -->
        <tr>
            <th rowspan="10">ESRS E4<br/>Biologische Vielfalt und Ökosysteme</th>
            <td>Direkte Ursachen des Biodiversitätsverlusts</td>
            <td>Klimawandel</td>
        </tr>
        <tr><td></td><td>Landnutzungsänderungen, Süßwasser- und Meeresnutzungsänderungen</td></tr>
        <tr><td></td><td>Direkte Ausbeutung</td></tr>
        <tr><td></td><td>Invasive gebietsfremde Arten</td></tr>
        <tr><td></td><td>Umweltverschmutzung</td></tr>
        <tr><td></td><td>Sonstige</td></tr>
        <tr><td>Auswirkungen auf den Zustand der Arten</td><td>Populationsgröße von Arten</td></tr>
        <tr><td></td><td>Globales Ausrottungsrisiko von Arten</td></tr>
        <tr><td>Auswirkungen auf den Umfang und den Zustand von Ökosystemen</td><td>Landdegradation</td></tr>
        <tr><td></td><td>Wüstenbildung</td></tr>
    </table>
    """
    
    # Die Tabelle wird im Streamlit-App angezeigt
    st.markdown(table_html, unsafe_allow_html=True)

# Hauptfunktion für die Streamlit-App
def display_page():
    st.title("Tabellenansicht")
    create_table_with_rowspan()


