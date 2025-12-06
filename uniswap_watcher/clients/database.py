from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging
Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"
    token_1 = Column(String)
    token_2 = Column(String)
    amount = Column(Float)
    update_on = Column(DateTime, primary_key=True)

def build_url(config):
    url = f"{config.get('username')}:{config.get('password')}@{config.get('host')}:{config.get('port')}/{config.get('database')}"
    if config.get('type') == "postgres":
        url = "postgresql+psycopg2://" + url
    elif config.get('type') == "clickhouse":
        url = "clickhouse+native://" + url
    return url

class DatabaseClient:
    def __init__(self, config):
        self.engine = create_engine(build_url(config))
        Base.metadata.create_all(self.engine)  # Auto-create tables
        self.Session = sessionmaker(bind=self.engine)

    def insert(self, price):
        logging.debug("Inserting new price %s in database", price)
        session = self.Session()
        session.add(Price(
            token_1=price.token_1,
            token_2=price.token_2,
            amount=price.amount,
            update_on=datetime.strptime(price.time, "%Y%m%dT%H:%M:%S")
        ))
        session.commit()
        session.close()
