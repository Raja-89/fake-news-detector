# 🕵️‍♂️ Fake News Detector

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

A machine learning-based web application that detects whether a news article is **FAKE** or **TRUE** in real-time. Built using Natural Language Processing (NLP) techniques and Logistic Regression, this app provides an interactive interface with confidence scores and dark mode styling.

## 🚀 Features

* **Real-time Prediction:** Instantly classifies news articles as Fake or True.
* **Confidence Score:** Displays the probability/confidence level of the prediction.
* **Interactive UI:** User-friendly interface built with [Streamlit](https://streamlit.io/).
* **Dark Mode:** Custom styled for better visibility and aesthetics.
* **Robust NLP Pipeline:** Utilizes TF-IDF vectorization for text processing.
* **Model Performance:** Includes visualization of the Confusion Matrix for model evaluation.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit, HTML/CSS
* **Machine Learning:** Scikit-Learn (Logistic Regression)
* **NLP:** NLTK, TF-IDF Vectorizer
* **Data Manipulation:** Pandas, NumPy

## 📂 File Structure

* `app.py`: The main Streamlit application script.
* `model.py`: Script used to train the machine learning model.
* `fake_news_model.pkl`: The pre-trained serialized model file.
* `requirements.txt`: List of Python dependencies.
* `confusion_matrix.png`: Visual representation of model performance.
* `fake_img.jpeg`: Asset used in the application.

## 💿 Installation

Follow these steps to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Raja-89/fake-news-detector.git](https://github.com/Raja-89/fake-news-detector.git)
    cd fake-news-detector
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

1.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  **Access the app:**
    The application will automatically open in your default web browser at `http://localhost:8501`.

3.  **Test it out:**
    Paste a news headline or article snippet into the text box and click the prediction button to see the results.

## 🧠 Model Training

If you wish to retrain the model with your own dataset:

1.  Ensure your dataset is formatted correctly (check `model.py` for expected input structure).
2.  Run the training script:
    ```bash
    python model.py
    ```
    This will generate a new `fake_news_model.pkl` file.

## 🤝 Contributing

Contributions are welcome! Please ensure you adhere to the following guidelines to ensure your changes can be merged.

### Requirements for Commits
To contribute to this repository, the following are **strictly required** for your commits to be merged successfully:

1.  **DCO Sign-off:** All commits must be signed off to certify the Developer Certificate of Origin (e.g., `git commit -s -m "message"`).
2.  **GPG Signature:** All commits must be verified with a GPG signature.

### Steps to Contribute
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (**remember to sign-off and GPG sign**).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.
---
Made with ❤️ by [Raja-89](https://github.com/Raja-89)
