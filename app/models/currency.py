from sqlalchemy import Column, Integer, String, CHAR
from ..database import Base

class Currency(Base):
    """
    SQLAlchemy model representing a currency.

    Attributes:
        id (int): Primary key and unique identifier for the currency
        code (str): Three-character ISO 4217 currency code (e.g., USD, EUR, GBP)
        name (str): Full name of the currency (e.g., US Dollar, Euro, British Pound)
        symbol (str): Currency symbol (e.g., $, €, £)
    """
    __tablename__ = "Currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(CHAR(3), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    symbol = Column(String(10), nullable=False)

    def __repr__(self):
        return f"Currency(code={self.code}, name={self.name}, symbol={self.symbol})"