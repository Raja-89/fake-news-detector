# model_train.py

import pandas as pd
import numpy as np
import string
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import nltk
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Show versions
print('Numpy', np.__version__)
print('Pandas', pd.__version__)
print('Sklearn', sklearn.__version__)

# Download necessary resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load datasets
df_true = pd.read_csv("True.csv")
df_fake = pd.read_csv("Fake.csv")

# Add labels
df_fake["label"] = 0  # Fake
df_true["label"] = 1  # True

# Combine datasets
df = pd.concat([df_fake, df_true], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

# Preprocessing
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words and len(word) > 2]
    return " ".join(words)

print("Cleaning text...")
df['text_clean'] = df['text'].apply(clean_text)
df = df[df['text_clean'].str.len() > 0].reset_index(drop=True)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.95, ngram_range=(1, 2))
X = vectorizer.fit_transform(df['text_clean'])
y = df['label'].values

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Save model + vectorizer
with open("fake_news_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Model and vectorizer saved!")

# Evaluate
y_pred = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Fake', 'True']))

# Confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=['Fake', 'True'], yticklabels=['Fake', 'True'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()
