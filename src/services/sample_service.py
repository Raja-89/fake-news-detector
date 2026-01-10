"""
Sample headlines service for managing and accessing test data.
Provides fake and true news samples for users to test the detector.
"""
import json
import random
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from src.config import config


@dataclass
class Sample:
    """
    Represents a sample news headline for testing.
    
    Attributes:
        text: The headline or article text
        label: Classification label ("fake" or "true")
        category: Topic category (e.g., "politics", "health")
        source: Optional source attribution
    """
    text: str
    label: str
    category: str = ""
    source: str = ""
    
    @property
    def is_fake(self) -> bool:
        """Check if this sample is fake news."""
        return self.label.lower() == "fake"
    
    @property
    def is_true(self) -> bool:
        """Check if this sample is true news."""
        return self.label.lower() == "true"


class SampleService:
    """
    Manages sample headlines for testing the fake news detector.
    
    Loads samples from JSON file with fallback to hardcoded samples
    if the file is unavailable.
    """
    
    # Hardcoded fallback samples
    FALLBACK_SAMPLES = [
        Sample(
            text="BREAKING: Scientists Discover Chocolate Cures All Diseases, Big Pharma Hiding Truth",
            label="fake",
            category="health",
            source="Fallback"
        ),
        Sample(
            text="SHOCKING: World Leaders Secretly Replaced by Robots, Insider Reveals",
            label="fake",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="Pope Francis Shocks World, Endorses Presidential Candidate",
            label="fake",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="FBI Agent Suspected in Hillary Email Leaks Found Dead in Apparent Murder-Suicide",
            label="fake",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="Donald Trump Sent His Own Plane to Transport 200 Stranded Marines",
            label="fake",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="Washington (Reuters) - The U.S. Senate confirmed Jerome Powell as Federal Reserve chairman",
            label="true",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="NASA's Perseverance Rover Successfully Lands on Mars After Seven-Month Journey",
            label="true",
            category="science",
            source="Fallback"
        ),
        Sample(
            text="Supreme Court Upholds Affordable Care Act in 7-2 Decision",
            label="true",
            category="politics",
            source="Fallback"
        ),
        Sample(
            text="Global COVID-19 Vaccine Distribution Reaches 1 Billion Doses Milestone",
            label="true",
            category="health",
            source="Fallback"
        ),
        Sample(
            text="European Union Announces New Climate Change Legislation Targeting Net Zero by 2050",
            label="true",
            category="environment",
            source="Fallback"
        ),
    ]
    
    def __init__(self, samples_path: Optional[str] = None):
        """
        Initialize the sample service.
        
        Args:
            samples_path: Path to samples JSON file. If None, uses config default.
        """
        self.samples_path = samples_path or config.get_samples_path()
        self._samples: List[Sample] = []
        self._loaded = False
    
    def load_samples(self) -> None:
        """
        Load samples from JSON file with fallback to hardcoded samples.
        
        If the JSON file is not found or contains invalid data,
        falls back to hardcoded samples.
        """
        try:
            samples_file = Path(self.samples_path)
            
            if not samples_file.exists():
                print(f"Warning: Samples file not found at {self.samples_path}, using fallback samples")
                self._samples = self.FALLBACK_SAMPLES.copy()
                self._loaded = True
                return
            
            with open(samples_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate JSON structure
            if 'samples' not in data:
                raise ValueError("JSON file must contain 'samples' key")
            
            # Parse samples
            self._samples = []
            for item in data['samples']:
                # Validate required fields
                if 'text' not in item or 'label' not in item:
                    print(f"Warning: Skipping invalid sample (missing text or label): {item}")
                    continue
                
                # Validate label
                if item['label'].lower() not in ['fake', 'true']:
                    print(f"Warning: Skipping sample with invalid label: {item['label']}")
                    continue
                
                sample = Sample(
                    text=item['text'],
                    label=item['label'],
                    category=item.get('category', ''),
                    source=item.get('source', '')
                )
                self._samples.append(sample)
            
            if not self._samples:
                print("Warning: No valid samples found in file, using fallback samples")
                self._samples = self.FALLBACK_SAMPLES.copy()
            
            self._loaded = True
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in samples file: {e}")
            print("Using fallback samples")
            self._samples = self.FALLBACK_SAMPLES.copy()
            self._loaded = True
        except Exception as e:
            print(f"Error loading samples: {e}")
            print("Using fallback samples")
            self._samples = self.FALLBACK_SAMPLES.copy()
            self._loaded = True
    
    def _ensure_loaded(self) -> None:
        """Ensure samples are loaded before accessing them."""
        if not self._loaded:
            self.load_samples()
    
    def get_fake_samples(self, count: int = 5) -> List[Sample]:
        """
        Get fake news samples.
        
        Args:
            count: Maximum number of samples to return
            
        Returns:
            List of fake news samples
        """
        self._ensure_loaded()
        fake_samples = [s for s in self._samples if s.is_fake]
        return fake_samples[:count]
    
    def get_true_samples(self, count: int = 5) -> List[Sample]:
        """
        Get true news samples.
        
        Args:
            count: Maximum number of samples to return
            
        Returns:
            List of true news samples
        """
        self._ensure_loaded()
        true_samples = [s for s in self._samples if s.is_true]
        return true_samples[:count]
    
    def get_all_samples(self) -> List[Sample]:
        """
        Get all samples.
        
        Returns:
            List of all samples
        """
        self._ensure_loaded()
        return self._samples.copy()
    
    def get_random_sample(self, label: Optional[str] = None) -> Optional[Sample]:
        """
        Get a random sample, optionally filtered by label.
        
        Args:
            label: Optional label filter ("fake" or "true")
            
        Returns:
            Random sample or None if no samples available
        """
        self._ensure_loaded()
        
        if label:
            label_lower = label.lower()
            if label_lower == "fake":
                samples = [s for s in self._samples if s.is_fake]
            elif label_lower == "true":
                samples = [s for s in self._samples if s.is_true]
            else:
                samples = self._samples
        else:
            samples = self._samples
        
        return random.choice(samples) if samples else None


# Create a singleton instance for convenience
sample_service = SampleService()
