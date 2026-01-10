from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
CORS(app)

# Load model and vectorizer once at startup
with open("fake_news_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

# Attempt to load resources; degrade gracefully if unavailable
try:
    stop_words = set(stopwords.words("english"))
except Exception:
    stop_words = set()

try:
    lemmatizer = WordNetLemmatizer()
except Exception:
    class _IdentityLemma:
        def lemmatize(self, w):
            return w
    lemmatizer = _IdentityLemma()

def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"<.*?>+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    try:
        words = [lemmatizer.lemmatize(word) for word in text.split()
                 if word not in stop_words and len(word) > 2]
    except Exception:
        words = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return " ".join(words)

@app.post('/predict')
def predict():
    try:
        payload = request.get_json(force=True) or {}
        text = payload.get('text', '')
        if not text.strip():
            return jsonify({"error": "Empty text"}), 400

        cleaned = clean_text(text)
        vectorized = vectorizer.transform([cleaned])
        pred = model.predict(vectorized)[0]
        proba = model.predict_proba(vectorized)[0]
        label = 'TRUE' if pred == 1 else 'FAKE'
        confidence = float(max(proba))
        return jsonify({"label": label, "confidence": confidence})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)