from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@db-server/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1")) # text() is a SQLAlchemy function that wraps a raw SQL string
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")