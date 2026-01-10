"""
Streamlit UI for the Fake News Detector.
Provides an interactive interface for testing news headlines.
"""
import streamlit as st
from src.config import config
from src.services.model_service import model_service
from src.services.sample_service import sample_service


# --- Custom CSS for dark theme styling ---
CUSTOM_CSS = """
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

.sample-headline {
    background-color: #1e1e1e;
    padding: 0.75rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border: 1px solid #6a0dad;
    cursor: pointer;
    transition: all 0.3s;
}

.sample-headline:hover {
    background-color: #2a2a2a;
    border-color: #8e44ad;
}

.fake-badge {
    background-color: #dc3545;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}

.true-badge {
    background-color: #28a745;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}
</style>
"""


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'selected_sample' not in st.session_state:
        st.session_state.selected_sample = None
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None


def main():
    """Main Streamlit application."""
    # Configure page
    st.set_page_config(
        page_title=config.STREAMLIT_PAGE_TITLE,
        layout=config.STREAMLIT_LAYOUT
    )
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Load services
    try:
        model_service.load_model()
        sample_service.load_samples()
    except Exception as e:
        st.error(f"Error loading services: {e}")
        st.stop()
    
    # Header
    st.markdown("""
        <h1 style='text-align: center;'>Fake News Detector</h1>
        <p style='text-align: center; color: #ccc;'>Use machine learning to detect fake news in real time.</p>
    """, unsafe_allow_html=True)
    
    # Main input section
    st.markdown("### 📝 Enter News Text")
    text_input = st.text_area(
        "Paste a news headline or short article:",
        height=150,
        key="main_input",
        value=st.session_state.selected_sample if st.session_state.selected_sample else ""
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        predict_button = st.button("🔍 Detect News", type="primary")
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.selected_sample = None
            st.session_state.prediction_result = None
            st.rerun()
    
    # Make prediction
    if predict_button and text_input:
        with st.spinner("Analyzing..."):
            result = model_service.predict(text_input)
            st.session_state.prediction_result = result
    
    # Display prediction result
    if st.session_state.prediction_result:
        result = st.session_state.prediction_result
        if result.is_valid:
            icon = "🔴" if result.is_fake else "🟢"
            st.markdown(f"""
                <div class='sample-box'>
                    <h3>{icon} Prediction: {result.label}</h3>
                    <p>Confidence: <b>{result.confidence:.2%}</b></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Error: {result.error}")
    
    # Sample headlines section
    st.markdown("---")
    st.markdown("### 💡 Try Sample Headlines")
    st.markdown("Click on any sample headline below to test the detector:")
    
    # Create tabs for fake and true samples
    tab1, tab2 = st.tabs(["🔴 Fake News Examples", "🟢 True News Examples"])
    
    with tab1:
        fake_samples = sample_service.get_fake_samples(count=5)
        for i, sample in enumerate(fake_samples):
            if st.button(
                f"📰 {sample.text[:80]}..." if len(sample.text) > 80 else f"📰 {sample.text}",
                key=f"fake_{i}",
                use_container_width=True
            ):
                st.session_state.selected_sample = sample.text
                result = model_service.predict(sample.text)
                st.session_state.prediction_result = result
                st.rerun()
    
    with tab2:
        true_samples = sample_service.get_true_samples(count=5)
        for i, sample in enumerate(true_samples):
            if st.button(
                f"📰 {sample.text[:80]}..." if len(sample.text) > 80 else f"📰 {sample.text}",
                key=f"true_{i}",
                use_container_width=True
            ):
                st.session_state.selected_sample = sample.text
                result = model_service.predict(sample.text)
                st.session_state.prediction_result = result
                st.rerun()
    
    # About section
    st.markdown("---")
    st.markdown("""
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
          <p>Contact: <a href='https://www.instagram.com/raja.rathour.89/?hl=en' style='color: #bb86fc;'>Raja Rathour</a></p>
          <p><a href='https://github.com/Raja-89' style='color: #bb86fc;'>GitHub</a> | <a href='https://www.linkedin.com/in/raja-rathour-067965325/' style='color: #bb86fc;'>LinkedIn</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
