"""
Convenience script to run the Streamlit interface.
"""
import subprocess
import sys

if __name__ == "__main__":
    print("Starting Streamlit Fake News Detector...")
    print("Open your browser to http://localhost:8501")
    print("-" * 50)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ui/streamlit_app.py"])
