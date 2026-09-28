from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# -----------------------------
# CORS (fixes Network error)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Database connection
# -----------------------------
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
except:
    conn = None
    cursor = None

# -----------------------------
# Test endpoint
# -----------------------------
@app.get("/test")
def test():
    if cursor is None:
        return {"error": "DB not available locally"}
    cursor.execute("SELECT * FROM test_actions LIMIT 1;")
    row = cursor.fetchone()
    return {"data": row}

# -----------------------------
# Login model
# -----------------------------
class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------------
# Login endpoint
# -----------------------------
@app.post("/login")
def login(request: LoginRequest):
    if request.email == "test@example.com" and request.password == "123":
        return {"status": "ok", "user": request.email}

    raise HTTPException(status_code=401, detail="Invalid email or password")
