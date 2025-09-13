# CBT System (with DeepFace Biometric Login, Debug Version)

Includes fixes for import errors on Streamlit Cloud.

## Debugging
- `app.py` now prints an error if `auth.py` import fails
- `auth.py` shows DeepFace errors directly in Streamlit
- Added `tensorflow` to requirements for DeepFace compatibility
