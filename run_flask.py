"""
Convenience script to run the Flask interface.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.flask_app import run_app

if __name__ == "__main__":
    print("Starting Flask Fake News Detector...")
    print("Open your browser to http://localhost:5000")
    print("-" * 50)
    run_app()
