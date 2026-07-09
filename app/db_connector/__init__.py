from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "database" / "database.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SQLALCHMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

#* create `sqlalchemy` engine
engine = create_engine(SQLALCHMY_DATABASE_URL)

#* create `sqlalchemy` session
SessionLocal = sessionmaker(bind=engine, autoflush=False)

#* define `Base` for Models
Base = declarative_base()