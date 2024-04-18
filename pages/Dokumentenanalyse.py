import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

def display_page():

    # Laden der Paragraphen und Inhalte aus der Excel-Datei
    def load_paragraphs_and_contents_from_excel(excel_path):
        df = pd.read_excel(excel_path)
        return df['Paragraph'].tolist(), df['Inhalt'].tolist()

    # Initialisieren des Sentence Transformers-Modells
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

    st.title('Paragraphenabdeckungsanalyse')

    uploaded_files = st.file_uploader("Lade Dokumente hoch", accept_multiple_files=True, type=['txt', 'pdf', 'docx'])


    if uploaded_files:
        paragraphs, contents = load_paragraphs_and_contents_from_excel('E1.xlsx')
        results = {
            paragraph: {
                'content': content,
                'covered': False,
                'matches': []  # Eine Liste von Tupeln (Satz, Übereinstimmungsquote)
            } for paragraph, content in zip(paragraphs, contents)
        }

        for uploaded_file in uploaded_files:
            document_text = uploaded_file.getvalue().decode('utf-8')
            document_sentences = document_text.split('.')

            for paragraph, content in zip(paragraphs, contents):
                content_embedding = model.encode([content], convert_to_tensor=True)

                for sentence in document_sentences:
                    sentence_embedding = model.encode([sentence], convert_to_tensor=True)
                    cos_sim = util.pytorch_cos_sim(content_embedding, sentence_embedding)
                    if cos_sim > 0.5:  # Schwellenwert für die Übereinstimmung
                        results[paragraph]['covered'] = True
                        results[paragraph]['matches'].append((sentence, cos_sim.item() * 100))  # Speichern mit Übereinstimmungsquote

        # Ergebnisse in der linken Spalte anzeigen
        
        st.write("Abgedeckte Paragraphen und Übereinstimmungsquoten:")
        for paragraph, data in results.items():
            if data['covered']:
                st.write(f"Paragraph {paragraph}:")
                for match in data['matches']:
                    sentence, match_percent = match
                    st.write(f"- Satz: \"{sentence.strip()}\". Übereinstimmungsquote: {match_percent:.2f}%")