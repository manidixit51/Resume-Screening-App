# 🧠 Resume Screening App

A smart, ML-powered Resume Screening App that automatically classifies resumes into job categories and calculates how well a resume matches a given job description. Built with Streamlit, Tesseract OCR, and scikit-learn.

---

## 🚀 Features

- 📄 Upload resumes (PDF, DOCX, TXT, or images)  
- 🧠 Resume category prediction using a trained SVM model  
- 🔍 Resume vs. Job Description similarity score using cosine similarity  
- 🧾 OCR support for image-based resumes (via Tesseract)  
- 📊 Word count, character count, and basic statistics  
- 🎯 Interactive Streamlit dashboard  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- scikit-learn (SVM, TF-IDF)  
- Tesseract OCR  
- spaCy (optional for NER)  
- Pandas & NumPy  

---

## 📂 Folder Structure

```

Resume-Screening-App/
├── app.py                # Streamlit frontend
├── clf.pkl               # Trained SVM model (Git LFS required)
├── tfidf.pkl             # TF-IDF vectorizer
├── utils.py              # Helper functions
├── requirements.txt      # Python dependencies
└── README.md             # Project overview

````

---

## 🧪 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/manidixit51/Resume-Screening-App.git
   cd Resume-Screening-App
````

2. **Set up the environment**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 🔍 Example Use Case

> Upload a software engineer resume and a job description for a backend developer role.
> The app predicts the category as `Software Development` and gives a **Resume–JD match score** of `85%`.

---

## 🧠 Future Enhancements

* Named Entity Recognition for skills, degrees, and companies
* Resume ranking based on skill match
* Upload job description as PDF/DOCX
* Admin dashboard with filters

---

## 🙋‍♀️ Author

**Mani Dixit**
GitHub: [@manidixit51](https://github.com/manidixit51)

---

## 📄 License

MIT License — Feel free to use, modify, and share.

```

---

If you want, I can help you generate a README with sample screenshots or badges next!
```
