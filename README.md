
# 🕵️‍♂️ Fake News Detector

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

> **A robust Machine Learning application designed to classify news articles as 'Real' or 'Fake' in real-time using Natural Language Processing (NLP).**

---

## 📖 Table of Contents
- [About The Project](#-about-the-project)
- [How It Works](#-how-it-works)
- [Key Features](#-key-features)
- [Technical Architecture](#-technical-architecture)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Model Performance](#-model-performance)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 About The Project

In an era of information overload, misinformation spreads rapidly. This **Fake News Detector** is an AI-powered tool that assists users in verifying the credibility of news articles. 

By analyzing the linguistic patterns and textual features of a given news headline or article body, the model predicts the likelihood of the information being authentic. The application is wrapped in a user-friendly **Streamlit** interface, making it accessible to non-technical users.

---

## 🧠 How It Works

The project utilizes a supervised machine learning pipeline:

1.  **Text Preprocessing:**
    * **Tokenization:** Breaking down text into individual words.
    * **Stemming:** Reducing words to their root form (e.g., "running" -> "run") using the Porter Stemmer.
    * **Stopword Removal:** Eliminating common words (like "the", "is", "at") that add little semantic meaning.
2.  **Vectorization:**
    * The cleaned text is converted into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**. This highlights words that are important to a specific document but rare across the corpus.
3.  **Classification:**
    * A **Logistic Regression** model is trained on these vectors to distinguish between "Real" and "Fake" news classes based on the probability of the input belonging to either category.

---

## ✨ Key Features

* **⚡ Real-Time Inference:** Get instant predictions upon entering text.
* **📊 Confidence Metrics:** (Optional) View the probability score of the prediction.
* **🌑 Dark Mode UI:** A sleek, modern interface optimized for readability.
* **🧩 Extensible:** The modular codebase allows for easy swapping of models (e.g., Random Forest, LSTM) or datasets.

---

## 🏗 Technical Architecture

### Tech Stack
* **Language:** Python 3.x
* **Frontend:** Streamlit
* **ML Libraries:** Scikit-learn, Pandas, NumPy
* **NLP:** NLTK (Natural Language Toolkit)

### Directory Structure
```text
fake-news-detector/
├── app.py                  # Main application entry point (Streamlit)
├── model.py                # Model training and serialization script
├── fake_news_model.pkl     # Pre-trained Logistic Regression model
├── requirements.txt        # Project dependencies
├── confusion_matrix.png    # Performance visualization
├── fake_img.jpeg           # UI assets
└── README.md               # Documentation
````

-----

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

  * Python 3.8 or higher installed.
  * Git installed.

### Installation

1.  **Clone the Repository**

    ```bash
    git clone [https://github.com/Raja-89/fake-news-detector.git](https://github.com/Raja-89/fake-news-detector.git)
    cd fake-news-detector
    ```

2.  **Create a Virtual Environment** (Recommended)

    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK Data** (If prompted during runtime)

    ```python
    import nltk
    nltk.download('stopwords')
    ```

-----

## 🎮 Usage Guide

1.  **Launch the Application**

    ```bash
    streamlit run app.py
    ```

2.  **Navigate to the UI**
    Open your browser and go to `http://localhost:8501`.

3.  **Enter News Text**

      * Copy a headline or a paragraph from a news article.
      * Paste it into the text area.
      * Click **"Predict"**.

4.  **Interpret Results**

      * ✅ **Real News:** The content is likely authentic.
      * ❌ **Fake News:** The content shows patterns of misinformation.

-----

## 📈 Model Performance

The Logistic Regression model was evaluated using standard metrics.
*(You can refer to `confusion_matrix.png` in the repo for visual details.)*

  * **Accuracy:** \~98% (on test dataset)
  * **Precision/Recall:** High balance between detecting fake news and minimizing false positives.

-----

## 🤝 Contributing

We welcome contributions from the community\! To ensure the security and integrity of the project, please adhere to the following **strict guidelines**.

### ⚠️ Mandatory Requirements

For your Pull Request to be accepted, your commits **MUST** include:

1.  **DCO (Developer Certificate of Origin) Sign-off**
      * Add `-s` to your commit command.
      * Example: `git commit -s -m "feat: updated preprocessing logic"`
2.  **GPG Signature Verification**
      * All commits must be signed with a GPG key to verify your identity.
      * Example: `git commit -S -m "feat: updated preprocessing logic"`

### How to Contribute

1.  **Fork** the project.
2.  **Create** your Feature Branch (`git checkout -b feature/NewFeature`).
3.  **Commit** your changes (**Signed & Verified**).
4.  **Push** to the branch (`git push origin feature/NewFeature`).
5.  Open a **Pull Request**.


## 📞 Contact

**Raja-89**

  * GitHub: [@Raja-89](https://www.google.com/search?q=https://github.com/Raja-89)

-----

*If you find this project useful, please give it a ⭐ on GitHub\!*

