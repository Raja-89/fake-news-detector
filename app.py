import streamlit as st
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

# Load model and vectorizer
with open("fake_news_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

# Setup NLTK
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = [lemmatizer.lemmatize(word) for word in text.split()
             if word not in stop_words and len(word) > 2]
    return " ".join(words)

def predict_news(text):
    try:
        if not text.strip():
            return "Invalid input", 0.0
        cleaned = clean_text(text)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]
        probability = model.predict_proba(vectorized)[0]
        result = "🟢 TRUE" if prediction == 1 else "🔴 FAKE"
        confidence = max(probability)
        return result, confidence
    except Exception as e:
        return f"Error: {str(e)}", 0.0

@st.cache_data
def load_sample_data():
    df_true = pd.read_csv("True.csv")
    df_fake = pd.read_csv("Fake.csv")
    df_true["label"] = 1
    df_fake["label"] = 0
    df = pd.concat([df_true, df_fake], ignore_index=True)
    return df

# --- Custom CSS for Tailwind-inspired styling ---
custom_css = """
<style>
body {
    background-color: #121212;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #bb86fc;
}

textarea, input {
    background-color: #1e1e1e;
    color: white;
    border: 1px solid #6a0dad;
    border-radius: 8px;
    padding: 10px;
    width: 100%;
}

button {
    background-color: #6a0dad;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
    cursor: pointer;
}

button:hover {
    background-color: #8e44ad;
}

.sample-box {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
    border: 1px solid #6a0dad;
}

.center-img {
    display: flex;
    justify-content: center;
    margin: 2rem 0;
}

.center-img img {
    max-width: 100%;
    height: auto;
    border-radius: 10px;
}
</style>
"""

# --- Streamlit Config and Layout ---
st.set_page_config(page_title="Fake News Detector", layout="centered")
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown("""
    <h1 style='text-align: center;'>Fake News Detector</h1>
    <p style='text-align: center; color: #ccc;'>Use machine learning to detect fake news in real time.</p>
""", unsafe_allow_html=True)

#st.markdown('<div class="center-img"></div>', unsafe_allow_html=True)

text_input = st.text_area("Paste a news headline or short article:", height=150)
if st.button("Detect News"):
    result, confidence = predict_news(text_input)
    st.markdown(f"""
        <div class='sample-box'>
            <h3>🔍 Prediction: {result}</h3>
            <p>Confidence: <b>{confidence:.2%}</b></p>
        </div>
    """, unsafe_allow_html=True)

# Sample Headlines
st.markdown("""
---
<h3>Try Sample Headlines</h3>
""", unsafe_allow_html=True)

df = load_sample_data()
col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 Try Fake Headline"):
        fake_sample = df[df['label'] == 0]['text'].sample(1).values[0]
        st.text_area("Fake Sample", value=fake_sample, height=100)

with col2:
    if st.button("🟢 Try True Headline"):
        true_sample = df[df['label'] == 1]['text'].sample(1).values[0]
        st.text_area("True Sample", value=true_sample, height=100)

# About Section
st.markdown("""
---
<h3 id='about'>About the Fake News Detector</h3>
<p>This tool uses Natural Language Processing (NLP) and a Logistic Regression model to identify whether a piece of news is real or fake.</p>
<ul>
  <li>Preprocessing with stopword removal, lemmatization</li>
  <li>TF-IDF vectorization (unigrams + bigrams)</li>
  <li>Logistic Regression classification</li>
  <li>Confidence scoring</li>
</ul>
<p>Trained on labeled news datasets with historical data.</p>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style='text-align: center; font-size: 0.9rem; color: #aaa;'>
  <p> Contact: <a href='https://www.instagram.com/raja.rathour.89/?hl=en' style='color: #bb86fc;'>Raja Rathour</a></p>
  <p><a href='https://github.com/Raja-89' style='color: #bb86fc;'>GitHub</a> | <a href='https://www.linkedin.com/in/raja-rathour-067965325/' style='color: #bb86fc;'>LinkedIn</a></p>
</div>
""", unsafe_allow_html=True)
