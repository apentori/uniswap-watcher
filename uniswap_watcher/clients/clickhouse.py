import clickhouse_connect
import logging
from datetime import datetime

class ClickhouseClient:
    def __init__(self, host: str, port: int, name: str, user: str, password: str):
        self.conn = clickhouse_connect.get_client(
                database=name,
                host=host,
                user=user,
                password=password,
                port=port
            )
        self._init_table()

    def _init_table(self):
        self.conn.command("""
            CREATE TABLE IF NOT EXISTS prices (
                token_1 TEXT,
                token_2 TEXT,
                amount float,
                update_on DateTime) ENGINE=MergeTree()
                ORDER BY update_on
            """)
    def insert(self, price):
        logging.debug("Insert Price %s in the database", price)
        datetime_price = datetime.strptime(price.time, "%Y%m%dT%H:%M:%S")
        data=[price.token_1, price.token_2, price.amount, datetime_price]
        self.conn.insert(
            'prices', [data], column_names=['token_1', 'token_2', 'amount', 'update_on'])
