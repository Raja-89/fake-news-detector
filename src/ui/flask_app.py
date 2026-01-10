"""
Flask API for the Fake News Detector.
Provides RESTful endpoints for predictions and sample headlines.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from src.config import config
from src.services.model_service import model_service
from src.services.sample_service import sample_service


# Initialize Flask app
app = Flask(__name__, static_folder='../../static')
CORS(app)

# Load services on startup
try:
    model_service.load_model()
    sample_service.load_samples()
    print("✓ Model and samples loaded successfully")
except Exception as e:
    print(f"✗ Error loading services: {e}")


@app.route('/')
def index():
    """Serve the main HTML page."""
    static_dir = Path(__file__).parent.parent.parent / 'static'
    return send_from_directory(static_dir, 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict if news text is fake or true.
    
    Request JSON:
        {
            "text": "News headline or article text"
        }
    
    Response JSON:
        {
            "label": "FAKE" or "TRUE",
            "confidence": 0.95,
            "is_fake": true
        }
    
    Error Response:
        {
            "error": "Error message"
        }
    """
    try:
        # Get request data
        payload = request.get_json(force=True) or {}
        text = payload.get('text', '')
        
        # Validate input
        if not text or not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Make prediction
        result = model_service.predict(text)
        
        # Check for prediction errors
        if not result.is_valid:
            return jsonify({"error": result.error}), 500
        
        # Return successful prediction
        return jsonify({
            "label": result.label,
            "confidence": result.confidence,
            "is_fake": result.is_fake
        })
        
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route('/samples', methods=['GET'])
def get_samples():
    """
    Get all sample headlines.
    
    Response JSON:
        {
            "samples": [
                {
                    "text": "Headline text",
                    "label": "fake" or "true",
                    "category": "politics",
                    "source": "Source name"
                },
                ...
            ]
        }
    """
    try:
        samples = sample_service.get_all_samples()
        return jsonify({
            "samples": [
                {
                    "text": s.text,
                    "label": s.label,
                    "category": s.category,
                    "source": s.source
                }
                for s in samples
            ]
        })
    except Exception as e:
        return jsonify({"error": f"Failed to load samples: {str(e)}"}), 500


@app.route('/samples/fake', methods=['GET'])
def get_fake_samples():
    """
    Get fake news sample headlines.
    
    Query Parameters:
        count: Number of samples to return (default: 5)
    
    Response JSON:
        {
            "samples": [...]
        }
    """
    try:
        count = request.args.get('count', default=5, type=int)
        samples = sample_service.get_fake_samples(count=count)
        return jsonify({
            "samples": [
                {
                    "text": s.text,
                    "label": s.label,
                    "category": s.category,
                    "source": s.source
                }
                for s in samples
            ]
        })
    except Exception as e:
        return jsonify({"error": f"Failed to load fake samples: {str(e)}"}), 500


@app.route('/samples/true', methods=['GET'])
def get_true_samples():
    """
    Get true news sample headlines.
    
    Query Parameters:
        count: Number of samples to return (default: 5)
    
    Response JSON:
        {
            "samples": [...]
        }
    """
    try:
        count = request.args.get('count', default=5, type=int)
        samples = sample_service.get_true_samples(count=count)
        return jsonify({
            "samples": [
                {
                    "text": s.text,
                    "label": s.label,
                    "category": s.category,
                    "source": s.source
                }
                for s in samples
            ]
        })
    except Exception as e:
        return jsonify({"error": f"Failed to load true samples: {str(e)}"}), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Response JSON:
        {
            "status": "ok",
            "model_loaded": true,
            "samples_loaded": true
        }
    """
    return jsonify({
        "status": "ok",
        "model_loaded": model_service.is_loaded,
        "samples_loaded": len(sample_service.get_all_samples()) > 0
    })


def run_app():
    """Run the Flask application."""
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )


if __name__ == '__main__':
    run_app()
