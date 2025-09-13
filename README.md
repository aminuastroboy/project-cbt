# CBT System (with DeepFace Biometric Login)

A role-based Computer Based Testing (CBT) system with biometric login (using DeepFace).

## Features
- **Biometric login** with camera (face verification)
- **Role-based dashboards** (Student, Examiner, Admin)
- **Students**: Take exams, auto-score
- **Examiners**: Create exams, add questions
- **Admin**: Manage system (placeholder)

## Setup
```bash
pip install -r requirements.txt
createdb cbt_system
psql -d cbt_system -f schema.sql
streamlit run app.py
```

## Deployment on Streamlit Cloud
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `app.py`
4. Use a hosted PostgreSQL (e.g., Supabase/Neon/Render)
5. Configure DB credentials in Streamlit **Secrets**

## Notes
- PostgreSQL must be running online and accessible
- DeepFace handles biometric verification (easier to deploy than face_recognition)
