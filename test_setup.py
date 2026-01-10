"""
Quick test script to verify the setup is working correctly.
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.config import config
        from src.utils.text_processor import text_processor
        from src.services.model_service import model_service
        from src.services.sample_service import sample_service
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    try:
        from src.config import config
        print(f"  Model path: {config.MODEL_PATH}")
        print(f"  Samples path: {config.SAMPLES_PATH}")
        print(f"  Max features: {config.MAX_FEATURES}")
        print("✓ Configuration loaded")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return False

def test_text_processor():
    """Test text processing."""
    print("\nTesting text processor...")
    try:
        from src.utils.text_processor import text_processor
        
        test_text = "This is a TEST with URLs https://example.com and HTML <b>tags</b>!"
        cleaned = text_processor.clean_text(test_text)
        
        print(f"  Original: {test_text}")
        print(f"  Cleaned: {cleaned}")
        
        if cleaned and len(cleaned) > 0:
            print("✓ Text processor working")
            return True
        else:
            print("✗ Text processor returned empty result")
            return False
    except Exception as e:
        print(f"✗ Text processor failed: {e}")
        return False

def test_sample_service():
    """Test sample service."""
    print("\nTesting sample service...")
    try:
        from src.services.sample_service import sample_service
        
        sample_service.load_samples()
        fake_samples = sample_service.get_fake_samples(2)
        true_samples = sample_service.get_true_samples(2)
        
        print(f"  Loaded {len(fake_samples)} fake samples")
        print(f"  Loaded {len(true_samples)} true samples")
        
        if fake_samples and true_samples:
            print(f"  Sample fake: {fake_samples[0].text[:50]}...")
            print(f"  Sample true: {true_samples[0].text[:50]}...")
            print("✓ Sample service working")
            return True
        else:
            print("✗ Sample service returned no samples")
            return False
    except Exception as e:
        print(f"✗ Sample service failed: {e}")
        return False

def test_model_service():
    """Test model service."""
    print("\nTesting model service...")
    try:
        from src.services.model_service import model_service
        
        # Check if model file exists
        model_path = Path(model_service.model_path)
        if not model_path.exists():
            print(f"✗ Model file not found at {model_path}")
            print("  Please train the model first using: python scripts/train_model.py")
            return False
        
        model_service.load_model()
        print(f"  Model loaded from: {model_service.model_path}")
        
        # Test prediction
        test_text = "Breaking news: Scientists discover cure for cancer"
        result = model_service.predict(test_text)
        
        print(f"  Test prediction: {result.label}")
        print(f"  Confidence: {result.confidence:.2%}")
        print(f"  Valid: {result.is_valid}")
        
        if result.is_valid:
            print("✓ Model service working")
            return True
        else:
            print(f"✗ Model prediction failed: {result.error}")
            return False
    except FileNotFoundError as e:
        print(f"✗ Model file not found: {e}")
        print("  Please train the model first using: python scripts/train_model.py")
        return False
    except Exception as e:
        print(f"✗ Model service failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Fake News Detector - Setup Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_text_processor,
        test_sample_service,
        test_model_service
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Setup is complete.")
        print("\nYou can now run:")
        print("  - Streamlit: python run_streamlit.py")
        print("  - Flask: python run_flask.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
