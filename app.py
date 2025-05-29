import streamlit as st
import pickle
#import docx
#import PyPDF2
import re
import pytesseract
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model and encoders
svc_model = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

# Tesseract config (set correct path if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # ← Adjust this if you're on Mac/Linux

# === Text Cleaning ===
def clean_text(text):
    text = re.sub('http\S+\s', ' ', text)
    text = re.sub('RT|cc', ' ', text)
    text = re.sub('#\S+\s', ' ', text)
    text = re.sub('@\S+', ' ', text)
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text.strip()

# === File Handling ===
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return ''.join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file):
    try:
        return file.read().decode('utf-8')
    except:
        return file.read().decode('latin-1')

def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

def process_uploaded_file(file):
    ext = file.name.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file)
    elif ext == 'docx':
        return extract_text_from_docx(file)
    elif ext == 'txt':
        return extract_text_from_txt(file)
    elif ext in ['png', 'jpg', 'jpeg']:
        return extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, TXT, or image.")

# === Prediction ===
def predict_category(text):
    cleaned = clean_text(text)
    vect = tfidf.transform([cleaned]).toarray()  # Ensure dense input
    pred = svc_model.predict(vect)
    return le.inverse_transform(pred)[0]

# === Cosine Similarity ===
def calculate_similarity(text1, text2):
    vects = tfidf.transform([clean_text(text1), clean_text(text2)]).toarray()
    return round(float(cosine_similarity([vects[0]], [vects[1]])[0][0]), 2)

# === Stats ===
def text_stats(text):
    return {
        'Words': len(text.split()),
        'Characters': len(text)
    }

# === UI ===
def main():
    st.set_page_config(page_title="Resume Screening Dashboard", layout="wide")
    st.title("📄 Resume Category Predictor & JD Matcher")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Upload Resume")
        resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT, Image)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])
    with col2:
        st.header("Upload Job Description")
        jd_file = st.file_uploader("Upload JD (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

    if resume_file is not None:
        try:
            resume_text = process_uploaded_file(resume_file)
            category = predict_category(resume_text)
            st.success(f"✅ Predicted Resume Category: **{category}**")

            if jd_file is not None:
                jd_text = process_uploaded_file(jd_file)
                match_score = calculate_similarity(resume_text, jd_text)
                st.info(f"📊 JD–Resume Match Score: **{match_score}**")
            else:
                jd_text = None

            st.divider()
            st.header("📌 Dashboard View")

            options = st.multiselect("Choose what to display:", ["Resume Text", "JD Text", "Resume Stats", "JD Stats"])

            if "Resume Text" in options:
                st.subheader("📄 Resume Text")
                st.text_area("Extracted Resume", resume_text, height=300)

            if jd_text and "JD Text" in options:
                st.subheader("📋 JD Text")
                st.text_area("Extracted Job Description", jd_text, height=300)

            if "Resume Stats" in options:
                st.subheader("📊 Resume Stats")
                stats = text_stats(resume_text)
                st.write(stats)

            if jd_text and "JD Stats" in options:
                st.subheader("📊 JD Stats")
                stats = text_stats(jd_text)
                st.write(stats)

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
