# CBT with Biometric Verification (React + FastAPI) - Admin Protected

Single-folder project for easy use on mobile.

## Admin credentials (hardcoded)
- Username: admin
- Password: admin123
- Token returned: admin-token-please-change

## Backend
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend
```bash
npm install
npm start
```

## Notes
- Admin routes require header `Authorization: Bearer <token>`.
- This is a demo with mocked biometric verification.
