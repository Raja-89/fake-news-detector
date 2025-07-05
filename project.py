import pickle

with open("fake_news_model.pkl", "rb") as file:
    model, vectorizer = pickle.load(file)


import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text



# New news article to test
new_article = """
WASHINGTON (Reuters) - Alabama Secretary of State John Merrill said he will certify Democratic Senator-elect Doug Jones as winner on Thursday despite opponent Roy Mooreâ€™s challenge, in a phone call on CNN. Moore, a conservative who had faced allegations of groping teenage girls when he was in his 30s, filed a court challenge late on Wednesday to the outcome of a U.S. Senate election he unexpectedly lost. 
"""

# Clean and vectorize
cleaned = clean_text(new_article)
vectorized = vectorizer.transform([cleaned])  # Note: transform, not fit_transform

# Predict
prediction = model.predict(vectorized)[0]

# Output
print("Prediction:", "REAL" if prediction == 1 else "FAKE")
