import streamlit as st
import requests
import json

# Azure Form Recognizer Settings
FORM_RECOGNIZER_ENDPOINT = "https://sustainability-fau.cognitiveservices.azure.com/"
API_KEY = "DNjmy8Ljo0XverRQ9e1a9vu104RcZ5mAegO0B3jwN7PxFKY6mkblJQQJ99AKACPV0roXJ3w3AAALACOGE42s"
#MODEL_ID = "prebuilt-document"  # Für generelle Dokumente

# Streamlit App
st.title("Azure Document Intelligence in Streamlit")
st.write("Lade ein Dokument hoch, um Inhalte zu analysieren.")

# Datei-Upload
uploaded_file = st.file_uploader("Lade ein Dokument hoch", type=["pdf", "jpg", "png"])

if uploaded_file:
    # Datei lesen
    file_bytes = uploaded_file.read()
    
    # Azure Form Recognizer API aufrufen
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/pdf" if uploaded_file.type == "application/pdf" else "image/jpeg"
    }
    
    analyze_url = f"{FORM_RECOGNIZER_ENDPOINT}formrecognizer/documentModels/{MODEL_ID}:analyze?api-version=2023-07-31"
    response = requests.post(analyze_url, headers=headers, data=file_bytes)
    
    if response.status_code == 200:
        # Extrahierte Daten anzeigen
        result = response.json()
        st.subheader("Analysierte Inhalte")
        st.json(result)
        
        # Optional: Strukturierte Daten filtern
        st.subheader("Strukturierte Inhalte")
        if "documents" in result:
            for doc in result["documents"]:
                for field_name, field_value in doc["fields"].items():
                    st.write(f"**{field_name}:** {field_value.get('content', 'N/A')}")
        else:
            st.write("Keine strukturierten Daten erkannt.")
    else:
        st.error(f"Fehler bei der Analyse: {response.status_code}")
        st.json(response.json())
