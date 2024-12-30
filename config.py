# Link for Swagger UI http://localhost:8000/docs

# config.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Direct database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootpassword',
    'database': 'EXPENSE_TRACKER',
    'port': '3306',
}

# Create SQLAlchemy URL
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

JWT_SECRET_KEY='sBnfuOoGncjpvZWtilIuUmMn9dJpW4nZJbm0Lra9_JQ'
JWT_REFRESH_SECRET_KEY='YkXCbBK3KWpvLX3AOpHse9KLPOOCwWWW9ATSTgYwwwg'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7