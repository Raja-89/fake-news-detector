"""
Central configuration module for the Fake News Detector application.
Manages paths, model parameters, and UI settings.
"""
import os
from pathlib import Path
from typing import Tuple


class Config:
    """Central configuration for the application"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    SRC_DIR = BASE_DIR / "src"
    
    # Model configuration
    MODEL_DIR = BASE_DIR / "models"
    MODEL_PATH = str(MODEL_DIR / "fake_news_model.pkl")
    
    # Fallback to root directory if model not in models/ folder
    if not os.path.exists(MODEL_PATH):
        MODEL_PATH = str(BASE_DIR / "fake_news_model.pkl")
    
    # Data configuration
    DATA_DIR = SRC_DIR / "data"
    SAMPLES_PATH = str(DATA_DIR / "samples.json")
    
    # ML Model hyperparameters
    MAX_FEATURES = 5000
    MIN_DF = 2
    MAX_DF = 0.95
    NGRAM_RANGE: Tuple[int, int] = (1, 2)
    
    # Text processing configuration
    MIN_WORD_LENGTH = 2
    
    # UI Configuration - Streamlit
    STREAMLIT_PAGE_TITLE = "Fake News Detector"
    STREAMLIT_LAYOUT = "centered"
    
    # UI Configuration - Flask
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 5000
    FLASK_DEBUG = False
    
    # UI Theme colors
    PRIMARY_COLOR = "#6a0dad"
    SECONDARY_COLOR = "#bb86fc"
    BACKGROUND_DARK = "#121212"
    BACKGROUND_LIGHT = "#1e1e1e"
    
    # Sample headlines configuration
    DEFAULT_SAMPLE_COUNT = 5
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values on application startup.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If critical configuration is invalid
        """
        # Check if model file exists
        if not os.path.exists(cls.MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {cls.MODEL_PATH}. "
                "Please train the model first using scripts/train_model.py"
            )
        
        # Validate hyperparameters
        if cls.MAX_FEATURES <= 0:
            raise ValueError("MAX_FEATURES must be positive")
        
        if not (0 < cls.MIN_DF < 1 or cls.MIN_DF >= 1):
            raise ValueError("MIN_DF must be positive")
        
        if not (0 < cls.MAX_DF <= 1):
            raise ValueError("MAX_DF must be between 0 and 1")
        
        if len(cls.NGRAM_RANGE) != 2 or cls.NGRAM_RANGE[0] > cls.NGRAM_RANGE[1]:
            raise ValueError("NGRAM_RANGE must be a tuple (min, max) where min <= max")
        
        return True
    
    @classmethod
    def get_model_path(cls) -> str:
        """Get the model file path"""
        return cls.MODEL_PATH
    
    @classmethod
    def get_samples_path(cls) -> str:
        """Get the samples data file path"""
        return cls.SAMPLES_PATH


# Create a singleton instance
config = Config()
