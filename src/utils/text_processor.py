"""
Text processing utilities for cleaning and preprocessing news text.
Handles stopword removal, lemmatization, and text normalization.
"""
import re
from typing import List, Optional
from src.config import config


class TextProcessor:
    """
    Handles text cleaning and preprocessing for the fake news detector.
    
    This class provides methods to clean raw text by removing URLs, HTML tags,
    special characters, stopwords, and applying lemmatization.
    """
    
    def __init__(self):
        """Initialize the text processor with NLTK resources."""
        self._stop_words = None
        self._lemmatizer = None
        self._initialize_nltk_resources()
    
    def _initialize_nltk_resources(self):
        """
        Initialize NLTK stopwords and lemmatizer with graceful degradation.
        If NLTK resources are unavailable, the processor will still work
        with reduced functionality.
        """
        try:
            from nltk.corpus import stopwords
            self._stop_words = set(stopwords.words("english"))
        except Exception:
            # Fallback to empty set if NLTK stopwords unavailable
            self._stop_words = set()
        
        try:
            from nltk.stem import WordNetLemmatizer
            self._lemmatizer = WordNetLemmatizer()
        except Exception:
            # Fallback to identity lemmatizer
            class _IdentityLemmatizer:
                def lemmatize(self, word: str) -> str:
                    return word
            self._lemmatizer = _IdentityLemmatizer()
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess a single text string.
        
        Steps:
        1. Convert to lowercase
        2. Remove content in square brackets
        3. Remove URLs
        4. Remove HTML tags
        5. Remove non-alphabetic characters
        6. Remove stopwords
        7. Apply lemmatization
        8. Filter words by minimum length
        
        Args:
            text: Raw text string to clean
            
        Returns:
            Cleaned text string with words separated by spaces
            
        Raises:
            ValueError: If text is None
        """
        if text is None:
            raise ValueError("Text cannot be None")
        
        # Handle empty string
        if not text.strip():
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove content in square brackets (e.g., [citation needed])
        text = re.sub(r"\[.*?\]", "", text)
        
        # Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        
        # Remove HTML tags
        text = re.sub(r"<.*?>+", "", text)
        
        # Remove non-alphabetic characters (keep only letters and spaces)
        text = re.sub(r"[^a-zA-Z]", " ", text)
        
        # Tokenize, remove stopwords, and lemmatize
        try:
            words = [
                self._lemmatizer.lemmatize(word)
                for word in text.split()
                if word not in self._stop_words and len(word) > config.MIN_WORD_LENGTH
            ]
        except Exception:
            # Fallback without lemmatization if it fails
            words = [
                word
                for word in text.split()
                if word not in self._stop_words and len(word) > config.MIN_WORD_LENGTH
            ]
        
        return " ".join(words)
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """
        Clean and preprocess a batch of text strings.
        
        Args:
            texts: List of raw text strings to clean
            
        Returns:
            List of cleaned text strings
            
        Raises:
            ValueError: If texts is None or contains None values
        """
        if texts is None:
            raise ValueError("Texts list cannot be None")
        
        cleaned_texts = []
        for i, text in enumerate(texts):
            if text is None:
                raise ValueError(f"Text at index {i} is None")
            cleaned_texts.append(self.clean_text(text))
        
        return cleaned_texts
    
    @property
    def has_stopwords(self) -> bool:
        """Check if stopwords are available."""
        return len(self._stop_words) > 0
    
    @property
    def has_lemmatizer(self) -> bool:
        """Check if lemmatizer is available."""
        return hasattr(self._lemmatizer, 'lemmatize')


# Create a singleton instance for convenience
text_processor = TextProcessor()
