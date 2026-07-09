#* define get_db dependency
from app.db_connector import SessionLocal

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()