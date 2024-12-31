from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from your config
from config import DATABASE_URL, Base

# Print the DATABASE_URL for debugging
print(f"Database URL: {DATABASE_URL}")

# Import your models
from app.models import user, account, recurring_transaction, expense, transaction, \
    budget, category, goal, currency, alert

# Alembic configuration
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Directly create engine with DATABASE_URL
    connectable = create_engine(DATABASE_URL)
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()