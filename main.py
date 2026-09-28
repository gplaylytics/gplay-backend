from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow your Vercel frontend
    allow_credentials=True,
    allow_methods=["*"],   # <-- THIS fixes the OPTIONS issue
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Connect to Supabase PostgreSQL
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
except:
    conn = None
    cursor = None


# -----------------------------
# Test endpoint (your original)
# -----------------------------
@app.get("/test")
def test():
    if cursor is None:
        return {"error": "DB not available locally"}
    cursor.execute("SELECT * FROM test_actions LIMIT 1;")
    row = cursor.fetchone()
    return {"data": row}


from fastapi import HTTPException
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    email = request.email
    password = request.password

    # Temporary login for testing
    if email == "test@example.com" and password == "123":
        return {"status": "ok", "user": email}

    raise HTTPException(status_code=401, detail="Invalid email or password")


# -----------------------------
# Login request model
# -----------------------------
class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------------
# Login endpoint
# -----------------------------
@app.post("/login")
def login(request: LoginRequest):
    email = request.email
    password = request.password

    # TEMPORARY: Replace with real DB check later
    if email == "test@example.com" and password == "123":
        return {"status": "ok", "user": email}

    raise HTTPException(status_code=401, detail="Invalid email or password")
