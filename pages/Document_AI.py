import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Azure-Konfiguration
AZURE_FORM_RECOGNIZER_ENDPOINT = "https://sustainability-fau.cognitiveservices.azure.com/"  # z. B. https://<deine-resource>.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY = "DNjmy8Ljo0XverRQ9e1a9vu104RcZ5mAegO0B3jwN7PxFKY6mkblJQQJ99AKACPV0roXJ3w3AAALACOGE42s"

# Initialisiere DocumentAnalysisClient
document_client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
)

st.title("Azure Document Intelligence in Streamlit")

uploaded_file = st.file_uploader("Lade ein Dokument hoch (PDF oder Bild)", type=["pdf", "png", "jpg"])

if uploaded_file:
    st.write("📄 Dokument wird verarbeitet...")
    
    # Datei-Upload in Azure Document Intelligence senden
    with uploaded_file:
        poller = document_client.begin_analyze_document("prebuilt-read", document=uploaded_file)
        result = poller.result()

    # Extrahierte Inhalte anzeigen
    for page in result.pages:
        st.write(f"Seite {page.page_number}:")
        st.write("Text:", page.content)

    # Tabellen analysieren
    for table in result.tables:
        st.write("Tabelle gefunden:")
        table_data = []
        for row in table.cells:
            table_data.append((row.row_index, row.column_index, row.content))
        st.write(table_data)

    st.success("Dokument erfolgreich analysiert!")
