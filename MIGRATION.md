# Migration Guide

This document explains the changes made during the code reorganization.

## Old vs New Structure

### Old Files (Deprecated)
The following files in the root directory are now deprecated:

- `app.py` → Replaced by `src/ui/streamlit_app.py`
- `server.py` → Replaced by `src/ui/flask_app.py`
- `model.py` → Replaced by `scripts/train_model.py`
- `index.html` → Moved to `static/index.html`

**Note:** These old files are kept for reference but should not be used. They will be removed in a future version.

### New Structure

```
src/
├── config.py                 # Central configuration
├── utils/
│   └── text_processor.py    # Shared text processing
├── services/
│   ├── model_service.py     # Model management
│   └── sample_service.py    # Sample headlines
├── data/
│   └── samples.json         # Sample data
└── ui/
    ├── streamlit_app.py     # Streamlit interface
    └── flask_app.py         # Flask API

static/
└── index.html               # HTML interface

scripts/
└── train_model.py           # Model training

models/
└── fake_news_model.pkl      # Trained model
```

## Running the Application

### Old Way (Deprecated)
```bash
# Don't use these anymore
streamlit run app.py
python server.py
```

### New Way (Recommended)
```bash
# Streamlit interface
python run_streamlit.py
# or
streamlit run src/ui/streamlit_app.py

# Flask interface
python run_flask.py
# or
python src/ui/flask_app.py
```

## Key Improvements

1. **Modular Architecture**
   - Separated concerns into utils, services, and UI
   - No code duplication between interfaces
   - Easier to maintain and extend

2. **Sample Headlines Feature**
   - Interactive sample headlines in both UIs
   - 5 fake and 5 true news examples
   - One-click testing

3. **Configuration Management**
   - Centralized config in `src/config.py`
   - Easy to modify settings
   - Consistent across all components

4. **Better Error Handling**
   - Graceful degradation
   - Clear error messages
   - Fallback mechanisms

## Breaking Changes

### Import Paths
If you have custom code importing from the old files, update imports:

```python
# Old
from app import clean_text, predict_news

# New
from src.utils.text_processor import text_processor
from src.services.model_service import model_service

# Usage
cleaned = text_processor.clean_text(text)
result = model_service.predict(text)
```

### Model Path
The model is now expected in `models/` directory:
- Old: `fake_news_model.pkl` (root)
- New: `models/fake_news_model.pkl`

The config automatically checks both locations for backward compatibility.

## Migration Checklist

- [x] Create new directory structure
- [x] Implement shared utilities (text processor)
- [x] Implement services (model, samples)
- [x] Refactor Streamlit UI
- [x] Refactor Flask UI
- [x] Add sample headlines feature
- [x] Update documentation
- [x] Create convenience scripts

## Next Steps

1. Test both interfaces thoroughly
2. Remove old files once confirmed working
3. Update any external integrations
4. Consider adding more sample headlines

## Support

If you encounter issues during migration:
1. Check that all dependencies are installed
2. Ensure NLTK resources are downloaded
3. Verify model file exists
4. Review error messages in console

For questions, contact Raja Rathour (see README.md for contact info).
