"""
Model training script for the Fake News Detector.
Trains a Logistic Regression classifier with TF-IDF features.
"""
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import nltk
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Import config
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.config import config

# Show versions
print('Numpy', np.__version__)
print('Pandas', pd.__version__)
print('Sklearn', sklearn.__version__)

# Download necessary resources
print("\nDownloading NLTK resources...")
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Load datasets
print("\nLoading datasets...")
df_true = pd.read_csv("True.csv")
df_fake = pd.read_csv("Fake.csv")

# Add labels
df_fake["label"] = 0  # Fake
df_true["label"] = 1  # True

# Combine datasets
df = pd.concat([df_fake, df_true], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
print(f"Total samples: {len(df)}")
print(f"Fake samples: {len(df_fake)}")
print(f"True samples: {len(df_true)}")

# Preprocessing
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """Clean and preprocess text."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words and len(word) > config.MIN_WORD_LENGTH
    ]
    return " ".join(words)

print("\nCleaning text...")
df['text_clean'] = df['text'].apply(clean_text)
df = df[df['text_clean'].str.len() > 0].reset_index(drop=True)
print(f"Samples after cleaning: {len(df)}")

# TF-IDF vectorization
print("\nVectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=config.MAX_FEATURES,
    min_df=config.MIN_DF,
    max_df=config.MAX_DF,
    ngram_range=config.NGRAM_RANGE
)
X = vectorizer.fit_transform(df['text_clean'])
y = df['label'].values

print(f"Feature matrix shape: {X.shape}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# Train model
print("\nTraining model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
print("Training complete!")

# Save model + vectorizer
model_path = Path(config.MODEL_PATH)
model_path.parent.mkdir(parents=True, exist_ok=True)

with open(model_path, "wb") as f:
    pickle.dump((model, vectorizer), f)

print(f"\nModel and vectorizer saved to: {model_path}")

# Evaluate
print("\nEvaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Fake', 'True']))

# Confusion matrix
print("\nGenerating confusion matrix...")
plt.figure(figsize=(6, 4))
sns.heatmap(
    confusion_matrix(y_test, y_pred),
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=['Fake', 'True'],
    yticklabels=['Fake', 'True']
)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()
print("Confusion matrix saved to: confusion_matrix.png")

print("\n✓ Training complete!")
