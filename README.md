# CBT System with Biometric Verification

## Setup
1. Create PostgreSQL DB:
   createdb cbt_system

2. Apply schema:
   psql -U postgres -d cbt_system -f schema.sql

3. Install requirements:
   pip install -r requirements.txt

4. Run app:
   streamlit run app.py
