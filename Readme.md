# Fake News Detector

Detect misinformation with a fast, lightweight ML pipeline. This project provides both a Streamlit UI and a Flask + HTML frontend, backed by a Logistic Regression model over TF‑IDF features.

## Quick Start

On Windows PowerShell:

```powershell
# 1) (Recommended) Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Ensure NLTK data is available (first run only)
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# 4) Run one of the UIs
# Streamlit (interactive UI)
python run_streamlit.py

# OR Flask (serves static HTML + REST API)
python run_flask.py
```

If you don’t have a trained model yet, run the training script first (see Training).

## Features

- Real-time classification of news as FAKE or TRUE
- Confidence score for each prediction
- Curated sample headlines (Fake vs True) for one‑click testing
- Two UIs: Streamlit and Flask + HTML
- Clean, modular architecture (services, utils, config)

## Project Structure

```
fake-news-detector/
├── src/
│   ├── config.py                 # Central configuration (paths, hyperparams, UI)
│   ├── utils/
│   │   └── text_processor.py    # Text cleaning & preprocessing
│   ├── services/
│   │   ├── model_service.py     # Model loading & prediction
│   │   └── sample_service.py    # Sample headlines management
│   ├── data/
│   │   └── samples.json         # Curated sample headlines
│   └── ui/
│       ├── streamlit_app.py     # Streamlit interface
│       └── flask_app.py         # Flask API serving static HTML
├── static/
│   └── index.html               # HTML interface (uses Flask endpoints)
├── models/
│   └── fake_news_model.pkl      # Trained model (with vectorizer)
├── scripts/
│   └── train_model.py           # Training script (LogReg + TF‑IDF)
├── index.html                   # Optional Vite dev server entry
├── vite.config.ts               # Vite proxy to Flask /predict
├── package.json                 # Vite frontend scripts
├── run_flask.py                 # Convenience launcher (Flask)
├── run_streamlit.py             # Convenience launcher (Streamlit)
├── requirements.txt
└── Readme.md
```

## Running the Apps

### Streamlit (Recommended)

```powershell
python run_streamlit.py
```
Then open http://localhost:8501. Includes dark theme, tabs for samples, one‑click testing, and confidence display.

### Flask + HTML (Lightweight)

```powershell
python run_flask.py
```
Then open http://127.0.0.1:5000. Serves `static/index.html` which calls the Flask REST endpoints.

### Optional: Vite Frontend Dev Server

If you prefer running a modern dev server for the HTML page:

```powershell
# In one terminal, run Flask (backend)
python run_flask.py

# In another terminal, run Vite (frontend)
npx vite
# or
npm run dev
```

The Vite server (default at http://localhost:5173) proxies `/predict` to the Flask backend (see `vite.config.ts`). Use `index.html` (root) for dev, or `static/index.html` when served by Flask.

## API (Flask)

Base URL: `http://127.0.0.1:5000`

- `POST /predict`
  - Request body:
    ```json
    { "text": "News headline or article text" }
    ```
  - Response body:
    ```json
    { "label": "FAKE", "confidence": 0.95, "is_fake": true }
    ```

- `GET /samples` — All samples
- `GET /samples/fake?count=5` — Fake samples
- `GET /samples/true?count=5` — True samples
- `GET /health` — Health check

Quick test from PowerShell:

```powershell
curl -Method Post -Uri http://127.0.0.1:5000/predict -ContentType 'application/json' -Body '{"text":"Breaking: Aliens land in NYC"}'
```

## Training

Train your own model (Logistic Regression over TF‑IDF):

1) Place `True.csv` and `Fake.csv` in the project root, each with a `text` column.

2) Run:

```powershell
python scripts/train_model.py
```

3) Output: `models/fake_news_model.pkl` (contains both the classifier and vectorizer).

Model defaults are controlled in `src/config.py`:

- `MAX_FEATURES = 5000`
- `MIN_DF = 2`
- `MAX_DF = 0.95`
- `NGRAM_RANGE = (1, 2)`
- `MIN_WORD_LENGTH = 2`

## Troubleshooting

- Model not found: Ensure `models/fake_news_model.pkl` exists. If missing, run the training script.
- NLTK data missing: Run `python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"` once.
- Port already in use: Change `FLASK_PORT` in `src/config.py` or stop the conflicting process.
- Windows execution policy blocks venv activation: Run PowerShell as Administrator and execute `Set-ExecutionPolicy RemoteSigned` (understanding the security implications), or use `cmd.exe` to activate: `.\.venv\Scripts\activate.bat`.

## Tech Stack

- Python (Flask, Streamlit)
- scikit‑learn (Logistic Regression)
- NLTK (stopwords, lemmatization)
- Tailwind CSS (static UI)
- Vite (optional frontend dev server)

## Architecture Highlights

- `TextProcessor` — robust cleaning pipeline (URLs, HTML, non‑alpha, stopwords, lemmatization)
- `ModelService` — loads/caches model + vectorizer; returns label, confidence, is_fake
- `SampleService` — loads curated samples from `src/data/samples.json`
- `Config` — all paths, hyperparameters, and UI settings in one place

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

## Contact

**Raja Rathour**

- Instagram: [@raja.rathour.89](https://www.instagram.com/raja.rathour.89/?hl=en)
- GitHub: [@Raja-89](https://github.com/Raja-89)
- LinkedIn: [Raja Rathour](https://www.linkedin.com/in/raja-rathour-067965325/)

---

Made with ❤️
