# CBT System

A role-based Computer Based Testing (CBT) system with biometric login (face recognition).

## Features
- **Biometric login** with camera (face recognition)
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

## Notes
- PostgreSQL must be running locally with user/password as set in `db.py`
- Face recognition requires `dlib` and `cmake` installed on your system
