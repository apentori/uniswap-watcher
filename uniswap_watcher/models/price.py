from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"
    token_1 = Column(String)
    token_2 = Column(String)
    amount = Column(Float)
    update_on = Column(DateTime, primary_key=True)

    def __init__(self, token_1: str, token_2: str, amount: float, update_on: str):
        self.token_1 = token_1
        self.token_2 = token_2
        self.amount = amount
        self.update_on = update_on

    def to_dict(self):
        return {
            "token_1": self.token_1,
            "token_2": self.token_2,
            "amount": self.amount,
            "update_on": self.update_on
        }
