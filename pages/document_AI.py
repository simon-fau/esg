import streamlit as st
import pandas as pd
import requests

# Azure Form Recognizer Konfiguration
FORM_RECOGNIZER_ENDPOINT = "https://sustainability-fau.cognitiveservices.azure.com/"
API_KEY = "DNjmy8Ljo0XverRQ9e1a9vu104RcZ5mAegO0B3jwN7PxFKY6mkblJQQJ99AKACPV0roXJ3w3AAALACOGE42s"
MODEL_ID = "prebuilt-document"

# Excel-Liste mit den Anforderungen
REQUIREMENTS_FILE = "requirements.xlsx"

# Funktion: Anforderungen laden
@st.cache
def load_requirements(file_path):
    return pd.read_excel(file_path)

# Funktion: Dokument analysieren
def analyze_document(file_bytes, content_type):
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": content_type,
    }
    analyze_url = f"{FORM_RECOGNIZER_ENDPOINT}formrecognizer/documentModels/{MODEL_ID}:analyze?api-version=2023-07-31"
    response = requests.post(analyze_url, headers=headers, data=file_bytes)
    response.raise_for_status()
    return response.json()

# Funktion: Daten mit Anforderungen abgleichen
def match_requirements(extracted_data, requirements_df):
    results = []
    for _, row in requirements_df.iterrows():
        field_name = row["Feldname"]
        description = row["Beschreibung"]
        # Suche nach passenden extrahierten Feldern
        matching_data = [
            field.get("content", "") for field in extracted_data.get("fields", {}).values() if field_name.lower() in field.get("content", "").lower()
        ]
        results.append({
            "Feldname": field_name,
            "Beschreibung": description,
            "Gefundene Werte": ", ".join(matching_data) if matching_data else "Keine Daten gefunden"
        })
    return pd.DataFrame(results)

# Streamlit UI
st.title("Nachhaltigkeitsdaten-Extraktion")
st.write("Lade ein Dokument hoch und vergleiche extrahierte Daten mit den Anforderungen aus der Excel-Liste.")

# Datei-Upload
uploaded_file = st.file_uploader("Dokument hochladen", type=["pdf", "jpg", "png"])

# Anforderungen laden
requirements = load_requirements(REQUIREMENTS_FILE)

if uploaded_file:
    file_bytes = uploaded_file.read()
    content_type = "application/pdf" if uploaded_file.type == "application/pdf" else "image/jpeg"
    
    with st.spinner("Dokument wird analysiert..."):
        analysis_result = analyze_document(file_bytes, content_type)
    
    st.subheader("Analysierte Inhalte")
    st.json(analysis_result)  # Zeige Rohdaten an (optional)
    
    # Anforderungen abgleichen
    st.subheader("Abgleich mit Anforderungen")
    matched_data = match_requirements(analysis_result, requirements)
    st.dataframe(matched_data)

    # Export der Ergebnisse
    st.download_button(
        "Ergebnisse als Excel herunterladen",
        data=matched_data.to_csv(index=False),
        file_name="extraction_results.csv",
        mime="text/csv"
    )
