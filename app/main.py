from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.session import engine, Base

# تجربة الاتصال بقاعدة البيانات وتفعيل الـ Vector
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    db_status = "Connected & Tables Created"
except Exception as e:
    db_status = f"DB Error: {str(e)}"

app = FastAPI(title="Step 2 Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "running", "database": db_status}
