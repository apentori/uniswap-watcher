from sqlalchemy import create_engine, Column, String, Float, DateTime, and_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import logging
from uniswap_watcher.models.price import Price
from uniswap_watcher.models.candlestick import Candlestick
Base = declarative_base()

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
        session.add(price)
        session.commit()
        session.close()

    def get_hourly_prices(self, token_1, token_2):
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        session = self.Session()
        res = session.query(Price).filter(and_(Price.token_1 == token_1, Price.token_2 == token_2, Price.update_on >= one_hour_ago,)).order_by(Price.update_on).all()
        session.close()
        return res

    def store_candlestick(self, candlestick: Candlestick):
        session = self.Session()
        session.add(candlestick)
        session.commit()
