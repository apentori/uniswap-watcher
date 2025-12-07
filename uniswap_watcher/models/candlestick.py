from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Candlestick(Base):
    __tablename__ = "candlesticks"
    id = Column(String, primary_key=True)
    token_1 = Column(String)      # e.g., "ETH"
    token_2 = Column(String)      # e.g., "USDC"
    open = Column(Float)          # First price in the hour
    high = Column(Float)          # Highest price in the hour
    low = Column(Float)           # Lowest price in the hour
    close = Column(Float)         # Last price in the hour
    volume = Column(Float)        # Total volume in the hour
    period_start = Column(DateTime)  # e.g., 2023-01-01 14:00:00

    def __init__(self, token_1, token_2, open, high, low, close, volume, period_start):
        self.id = f"{token_1}-{token_2}-{period_start}"
        self.token_1 = token_1
        self.token_2 = token_2
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.period_start = period_start

    def to_dict(self):
        return {
            "token_1": self.token_1,
            "token_2": self.token_2,
            "open": self.open,
            "close": self.close,
            "low": self.low,
            "volume": self.volume,
            "period_start": self.period_start
        }
