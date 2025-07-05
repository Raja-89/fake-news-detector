import pandas as pd
import numpy as np
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Load datasets
df_true = pd.read_csv("True.csv")
df_fake = pd.read_csv("Fake.csv")

# Label data
df_true["label"] = 1
df_fake["label"] = 0

# Combine and shuffle
df = pd.concat([df_true, df_fake], ignore_index=True).sample(frac=1, random_state=42)

# Clean text
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

df['text_clean'] = df['text'].apply(clean_text)
df = df[df['text_clean'].str.len() > 0]

# Features and labels
X_text = df['text_clean']
y = df['label']

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2), min_df=2, max_df=0.95)
X = vectorizer.fit_transform(X_text)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model and vectorizer
with open("fake_news_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model and vectorizer saved to 'fake_news_model.pkl'")
