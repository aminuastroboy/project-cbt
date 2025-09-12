from fastapi import FastAPI, UploadFile, Form, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "db.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_TOKEN = "admin-token-please-change"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": {}, "results": {}}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

@app.post("/register/")
async def register(email: str = Form(...), name: str = Form(...)):
    db = load_db()
    if email in db["users"]:
        return {"status": "error", "message": "User already exists"}
    db["users"][email] = {"name": name, "face_encoding": [0.1,0.2,0.3]}
    save_db(db)
    return {"status": "success", "message": "User registered"}

@app.post("/verify/")
async def verify(email: str = Form(...)):
    db = load_db()
    if email in db["users"]:
        return {"status": "success", "message": "Face verified (mock)"}
    return {"status": "error", "message": "User not found"}

@app.post("/verify/face")
async def verify_face(email: str = Form(...), file: UploadFile = File(...)):
    db = load_db()
    if email not in db["users"]:
        return {"status": "error", "message": "User not found"}
    # Mock: Always accept uploaded image if email exists
    return {"status": "success", "message": "Face verified with image (mock)"}

@app.post("/exam/submit/")
async def submit(email: str = Form(...), score: int = Form(...)):
    db = load_db()
    if email not in db["users"]:
        return {"status": "error", "message": "User not found"}
    db["results"][email] = {"score": score}
    save_db(db)
    return {"status": "success", "message": "Result saved"}

@app.post("/admin/login")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"status": "success", "token": ADMIN_TOKEN}
    return {"status": "error", "message": "Invalid credentials"}

def check_admin(token: str = Header(None, alias="Authorization")):
    # Expect header "Authorization: Bearer <token>"
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if token.startswith("Bearer "):
        t = token.split(" ", 1)[1]
    else:
        t = token
    if t != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")

@app.get("/admin/users/")
async def get_users(authorization: str = Header(None)):
    check_admin(authorization)
    db = load_db()
    return db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
