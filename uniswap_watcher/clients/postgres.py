import psycopg2
import logging
from datetime import datetime

class PostgresClient:
    def __init__(self,host, port, name, user, password):
        self.conn = psycopg2.connect(database=name, host=host, user=user, password=password, port=port)
        self._init_table()

    def _init_table(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS prices (token_1 TEXT, token_2 TEXT, amount float, update_on TIMESTAMP);")
        self.conn.commit()
        cursor.close()

    def insert(self, price):
        cursor = self.conn.cursor()
        logging.debug("Insert Price %s in the database", price)
        datetime_price = datetime.strptime(price.time, "%Y%m%dT%H:%M:%S")
        cursor.execute(f"INSERT INTO prices (token_1, token_2, amount, update_on) VALUES ('{price.token_1}', '{price.token_2}', {price.amount}, '{price.time}')")
        self.conn.commit()
        cursor.close()


    def close(self):
        self.conn.close()


