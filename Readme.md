# Fake News Detector

A machine learning-based fake news detection application with multiple interfaces. This app uses NLP and Logistic Regression to classify news as FAKE or TRUE in real-time, featuring an interactive sample headlines section for easy testing.

## ✨ Features

- **Real-time classification** of news as FAKE or TRUE
- **Interactive sample headlines** - Test with pre-selected examples
- **Dual interfaces** - Streamlit and Flask/HTML options
- **High accuracy** - Trained on labeled news datasets
- **Confidence scores** - See prediction confidence for each classification
- **Clean architecture** - Modular, maintainable codebase

## 📁 Project Structure

```
fake-news-detector/
├── src/
│   ├── config.py                 # Central configuration
│   ├── utils/
│   │   └── text_processor.py    # Text cleaning and preprocessing
│   ├── services/
│   │   ├── model_service.py     # Model loading and prediction
│   │   └── sample_service.py    # Sample headlines management
│   ├── data/
│   │   └── samples.json         # Sample headlines data
│   └── ui/
│       ├── streamlit_app.py     # Streamlit interface
│       └── flask_app.py         # Flask API
├── static/
│   └── index.html               # HTML interface
├── models/
│   └── fake_news_model.pkl      # Trained ML model
├── scripts/
│   └── train_model.py           # Model training script
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Raja-89/fake-news-detector.git
   cd fake-news-detector
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK resources:**
   ```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
   ```

4. **Ensure model file exists:**
   - The trained model should be at `models/fake_news_model.pkl` or `fake_news_model.pkl`
   - If not present, train the model (see Training section below)

## 💻 Usage

### Option 1: Streamlit Interface (Recommended)

Run the Streamlit app for an interactive web interface:

```bash
streamlit run src/ui/streamlit_app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Dark theme interface
- Tabbed sample headlines (Fake vs True)
- One-click testing of samples
- Clear button to reset input
- Confidence score display

### Option 2: Flask/HTML Interface

Run the Flask server for a lightweight HTML interface:

```bash
python src/ui/flask_app.py
```

Then open your browser to `http://localhost:5000`

**Features:**
- Clean, responsive design
- Sample headlines in grid layout
- RESTful API endpoints
- Smooth animations

## 🧪 Sample Headlines Feature

Both interfaces include curated sample headlines for quick testing:

**Fake News Examples (5):**
- Sensational health claims
- Conspiracy theories
- Misleading political stories

**True News Examples (5):**
- Verified political news
- Scientific announcements
- Official government statements

Click any sample to automatically populate the input field and run prediction!

## 🔧 Training the Model

If you need to retrain the model with your own data:

1. **Prepare datasets:**
   - Place `True.csv` and `Fake.csv` in the project root
   - Each CSV should have a `text` column with news articles

2. **Run training script:**
   ```bash
   python scripts/train_model.py
   ```

3. **Model will be saved to:**
   - `models/fake_news_model.pkl`

**Training details:**
- Algorithm: Logistic Regression
- Features: TF-IDF (unigrams + bigrams)
- Max features: 5000
- Preprocessing: Stopword removal, lemmatization

## 🔌 API Endpoints (Flask)

### `POST /predict`
Predict if news text is fake or true.

**Request:**
```json
{
  "text": "News headline or article text"
}
```

**Response:**
```json
{
  "label": "FAKE",
  "confidence": 0.95,
  "is_fake": true
}
```

### `GET /samples`
Get all sample headlines.

### `GET /samples/fake`
Get fake news samples only.

### `GET /samples/true`
Get true news samples only.

### `GET /health`
Health check endpoint.

## 🏗️ Architecture

### Core Components

1. **TextProcessor** (`src/utils/text_processor.py`)
   - Cleans and preprocesses text
   - Removes URLs, HTML, special characters
   - Applies stopword removal and lemmatization

2. **ModelService** (`src/services/model_service.py`)
   - Loads and caches ML model
   - Generates predictions with confidence scores
   - Handles errors gracefully

3. **SampleService** (`src/services/sample_service.py`)
   - Manages sample headlines
   - Loads from JSON with fallback
   - Filters by label (fake/true)

4. **Config** (`src/config.py`)
   - Centralizes all configuration
   - Model paths and hyperparameters
   - UI settings

### Design Principles

- **Separation of concerns** - Clear module boundaries
- **No code duplication** - Shared utilities across UIs
- **Error handling** - Graceful degradation
- **Extensibility** - Easy to add new features

## 📊 Model Performance

- **Accuracy:** ~95% (on test set)
- **Features:** TF-IDF with 5000 max features
- **Training data:** Labeled news articles dataset
- **Preprocessing:** Comprehensive text cleaning pipeline

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact

**Raja Rathour**
- Instagram: [@raja.rathour.89](https://www.instagram.com/raja.rathour.89/?hl=en)
- GitHub: [@Raja-89](https://github.com/Raja-89)
- LinkedIn: [Raja Rathour](https://www.linkedin.com/in/raja-rathour-067965325/)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) - Interactive web apps
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- [NLTK](https://www.nltk.org/) - Natural language processing
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

## 📚 Technical Details

### Text Preprocessing Pipeline

1. Convert to lowercase
2. Remove content in square brackets
3. Remove URLs
4. Remove HTML tags
5. Remove non-alphabetic characters
6. Remove stopwords
7. Apply lemmatization
8. Filter by minimum word length

### Model Training Pipeline

1. Load and combine datasets
2. Clean and preprocess text
3. TF-IDF vectorization (unigrams + bigrams)
4. Train Logistic Regression classifier
5. Evaluate on test set
6. Save model and vectorizer

### Configuration Options

Edit `src/config.py` to customize:
- Model file paths
- TF-IDF parameters (max_features, min_df, max_df)
- N-gram range
- UI settings (host, port, theme colors)
- Sample data paths

---

**Made with ❤️ by Raja Rathour**
