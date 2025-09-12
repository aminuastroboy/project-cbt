from fastapi import FastAPI, UploadFile, Form, File
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

@app.get("/admin/users/")
async def get_users():
    db = load_db()
    return db
