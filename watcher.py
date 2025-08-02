#!/usr/bin/env python
import os
import logging
import json
import yaml
import csv
import click
import psycopg2
from web3 import Web3
from uniswap import Uniswap
from time import gmtime, strftime, sleep
from datetime import datetime

logging.basicConfig(level=logging.INFO)

INFURA_BASE_URL="https://mainnet.infura.io/v3"
FILE_NAME="price.csv"
class Price:
    def __init__(self, token_1, token_2, amount, time):
        self.token_1 = token_1
        self.token_2 = token_2
        self.amount = amount
        self.time = time

    def to_dict(self):
        return {
            "token_1": self.token_1,
            "token_2": self.token_2,
            "amount": self.amount,
            "time": self.time
        }

class UniswapClient:
    def __init__(self, api_key):
        self.client = Uniswap(
            address=None,
            private_key=None,
            version=3,
            provider=f"{INFURA_BASE_URL}/{api_key}"
        )

    def get_token_price(self, token_1, token_2):
        price = self.client.get_price_input(token_1.get("address"), token_2.get("address"), 10**18)
        logging.debug("The Token price is %s", price)
        p = Price(token_1.get("name"), token_2.get("name"), price / 10**18, strftime("%Y%m%dT%H:%M:%S", gmtime()))
        return p

class Postgres:
    def __init__(self,host, port, name, user, password):
        self.conn = psycopg2.connect(database=name, host=host, user=user, password=password, port=port)
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


SNT={"name": "SNT", "address": "0x744d70FDBE2Ba4CF95131626614a1763DF805B9E" }
ETH={"name": "ETH", "address": "0x0000000000000000000000000000000000000000"}

def save_price(price):
    with open(FILE_NAME, "a") as file:
        writer = csv.DictWriter(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=["token_1", "token_2", "amount", "time"])
        logging.info(price.to_dict())
        writer.writerow(price.to_dict())

@click.command()
@click.option("-k", "--api-key",        prompt="Enter Infura API Key",          help="Infura API Key")
@click.option("-f", "--frequency",      default=300,                            help="Frequency between each call (in sec)")
@click.option("-h", "--psql-host",      default="localhost",                    help="Postgres Host")
@click.option("-p", "--psql-port",      default=5432,                           help="Postgres Port")
@click.option("-d", "--psql-database",  default="postgres",                     help="Postgres Database")
@click.option("-u", "--psql-username",  default="postgres",                      help="Postgres User")
@click.option("-P", "--psql-password",  prompt="Postgres Password",             help="Postgres Password")
@click.option("-l", "--log-level",      default="INFO",                         help="Log Level")
def main(api_key, frequency, psql_host, psql_port, psql_database, psql_username, psql_password, log_level):
    client = UniswapClient(api_key)
    psqlClient = Postgres(psql_host, psql_port, psql_database, psql_username, psql_password)
    while True:
        p = client.get_token_price(ETH, SNT)
        logging.info("The 1 eth is worth : %s SNT", p.amount)

        #save_price(p)
        psqlClient.insert(p)
        sleep(frequency)

main()

