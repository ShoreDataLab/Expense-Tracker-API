from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import engine, SessionLocal, Base, get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Re-export everything from config
__all__ = ['engine', 'SessionLocal', 'Base', 'get_db']

Base = declarative_base()

def init_db():
    try:
        # Test connection and verify tables exist
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("Database connection verified successfully")
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        logger.exception("Full exception details:")
        raise

def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
    finally:
        logger.info("Closing database session")
        db.close()