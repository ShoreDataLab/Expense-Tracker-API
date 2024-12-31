from sqlalchemy import create_engine
from config import DATABASE_URL, Base
from app.models import user, account, transaction, recurring_transaction, expense, \
                budget, category, goal, currency, alert

def run_migrations():
    """
    Create all tables based on models
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)