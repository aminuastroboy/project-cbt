# 🖥️ CBT System with Biometric Verification (Python + Streamlit)

Minimal but complete CBT prototype with biometric login, admin exam management, and student exam taking.

## Setup
1) Python env & install:
```
pip install -r requirements.txt
```
2) PostgreSQL:
```
createdb cbt_system
psql -d cbt_system -f schema.sql
```
3) Run app:
```
streamlit run app.py
```
