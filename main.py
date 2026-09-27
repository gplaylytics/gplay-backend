from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

@app.get("/test")
def test():
    cursor.execute("SELECT * FROM test_actions LIMIT 1;")
    row = cursor.fetchone()
    return {"data": row}
