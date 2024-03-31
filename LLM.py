import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt

# Laden der Paragraphen und Inhalte aus der Excel-Datei
def load_paragraphs_and_contents_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    return df['Paragraph'].tolist(), df['Inhalt'].tolist()

st.set_page_config(page_title='Paragraphenabdeckungsanalyse', page_icon=':memo:', layout='wide')

# Funktion zum Erstellen von Donut-Charts
def create_donut_chart(percent, ax, title):
    sizes = [percent, 100-percent]
    colors = ['green','grey']
    ax.pie(sizes, colors=colors, startangle=90, pctdistance=0.85, wedgeprops=dict(width=0.3))
    # Zeichne ein weißes Kreis in der Mitte
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax.add_artist(centre_circle)
    ax.text(0, 0, f"{percent}%", ha='center', va='center', fontsize=12)
    ax.set_title(title, pad=20)

# Initialisieren des Sentence Transformers-Modells
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

st.title('Paragraphenabdeckungsanalyse')

# Spaltengestaltung
left_column, middle_column, right_column = st.columns([4, 0.8, 0.8])

# Linke Spalte für Donut-Charts
with middle_column:
    fig, axs = plt.subplots(3, 1, figsize=(3, 9))
    create_donut_chart(70, axs[0], 'E1')
    create_donut_chart(55, axs[1], 'E2')
    create_donut_chart(80, axs[2], 'E3')
    st.pyplot(fig)

# Mittlere Spalte für DataUploader
with left_column:
    uploaded_files = st.file_uploader("Lade Dokumente hoch", accept_multiple_files=True, type=['txt', 'pdf', 'docx'])

# Rechte Spalte für Donut-Charts
with right_column:
    fig, axs = plt.subplots(3, 1, figsize=(3, 9))
    create_donut_chart(60, axs[0], 'E4')
    create_donut_chart(45, axs[1], 'E5')
    create_donut_chart(75, axs[2], 'E6')
    st.pyplot(fig)

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
    with left_column:
        st.write("Abgedeckte Paragraphen und Übereinstimmungsquoten:")
        for paragraph, data in results.items():
            if data['covered']:
                st.write(f"Paragraph {paragraph}:")
                for match in data['matches']:
                    sentence, match_percent = match
                    st.write(f"- Satz: \"{sentence.strip()}\". Übereinstimmungsquote: {match_percent:.2f}%")