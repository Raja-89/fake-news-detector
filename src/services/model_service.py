"""
Model service for loading ML model and making predictions.
Handles model caching, text preprocessing, and prediction generation.
"""
import pickle
from dataclasses import dataclass
from typing import List, Optional, Tuple, Any
from pathlib import Path
from src.config import config
from src.utils.text_processor import TextProcessor


@dataclass
class PredictionResult:
    """
    Represents the result of a fake news prediction.
    
    Attributes:
        label: Classification label ("FAKE" or "TRUE")
        confidence: Confidence score between 0.0 and 1.0
        is_fake: Boolean indicating if news is fake
        error: Optional error message if prediction failed
    """
    label: str
    confidence: float
    is_fake: bool
    error: Optional[str] = None
    
    @property
    def is_true(self) -> bool:
        """Check if this prediction is true news."""
        return not self.is_fake
    
    @property
    def is_valid(self) -> bool:
        """Check if this is a valid prediction (no error)."""
        return self.error is None


class ModelService:
    """
    Manages ML model loading and prediction operations.
    
    Loads and caches the trained model and vectorizer, coordinates
    with TextProcessor for preprocessing, and generates predictions
    with confidence scores.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the model service.
        
        Args:
            model_path: Path to model pickle file. If None, uses config default.
        """
        self.model_path = model_path or config.get_model_path()
        self._model: Optional[Any] = None
        self._vectorizer: Optional[Any] = None
        self._text_processor = TextProcessor()
        self._loaded = False
    
    def load_model(self) -> None:
        """
        Load the ML model and vectorizer from pickle file.
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            ValueError: If model file is corrupted or invalid
        """
        model_file = Path(self.model_path)
        
        if not model_file.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please train the model first using scripts/train_model.py"
            )
        
        try:
            with open(model_file, 'rb') as f:
                self._model, self._vectorizer = pickle.load(f)
            
            # Validate loaded objects
            if not hasattr(self._model, 'predict'):
                raise ValueError("Loaded model doesn't have predict method")
            
            if not hasattr(self._vectorizer, 'transform'):
                raise ValueError("Loaded vectorizer doesn't have transform method")
            
            self._loaded = True
            
        except pickle.UnpicklingError as e:
            raise ValueError(f"Corrupted model file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
    
    def _ensure_loaded(self) -> None:
        """Ensure model is loaded before making predictions."""
        if not self._loaded:
            self.load_model()
    
    def predict(self, text: str) -> PredictionResult:
        """
        Predict if a news text is fake or true.
        
        Args:
            text: Raw news text to classify
            
        Returns:
            PredictionResult with label, confidence, and metadata
        """
        try:
            # Validate input
            if not text or not text.strip():
                return PredictionResult(
                    label="ERROR",
                    confidence=0.0,
                    is_fake=False,
                    error="Empty text provided"
                )
            
            # Ensure model is loaded
            self._ensure_loaded()
            
            # Preprocess text
            cleaned_text = self._text_processor.clean_text(text)
            
            # Check if cleaned text is empty
            if not cleaned_text:
                return PredictionResult(
                    label="ERROR",
                    confidence=0.0,
                    is_fake=False,
                    error="Text contains no valid words after preprocessing"
                )
            
            # Vectorize
            vectorized = self._vectorizer.transform([cleaned_text])
            
            # Predict
            prediction = self._model.predict(vectorized)[0]
            probabilities = self._model.predict_proba(vectorized)[0]
            
            # Format result
            label = "TRUE" if prediction == 1 else "FAKE"
            confidence = float(max(probabilities))
            is_fake = prediction == 0
            
            return PredictionResult(
                label=label,
                confidence=confidence,
                is_fake=is_fake
            )
            
        except ValueError as e:
            # Re-raise ValueError (from text processor or validation)
            return PredictionResult(
                label="ERROR",
                confidence=0.0,
                is_fake=False,
                error=str(e)
            )
        except Exception as e:
            # Catch any other errors
            return PredictionResult(
                label="ERROR",
                confidence=0.0,
                is_fake=False,
                error=f"Prediction failed: {str(e)}"
            )
    
    def predict_batch(self, texts: List[str]) -> List[PredictionResult]:
        """
        Predict multiple news texts at once.
        
        Args:
            texts: List of raw news texts to classify
            
        Returns:
            List of PredictionResult objects
        """
        if not texts:
            return []
        
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        
        return results
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._loaded
    
    @property
    def model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self._loaded:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "model_type": type(self._model).__name__,
            "vectorizer_type": type(self._vectorizer).__name__,
            "model_path": self.model_path
        }


# Create a singleton instance for convenience
model_service = ModelService()
