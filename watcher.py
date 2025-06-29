#!/usr/bin/env python
import os
import logging
import json
import csv
from web3 import Web3
from uniswap import Uniswap
from time import gmtime, strftime, sleep

logging.basicConfig(level=logging.INFO)

PROVIDER_URL = os.environ.get('INFURA_BASE_URL','https://mainnet.infura.io/v3/') + os.environ.get('INFURA_API_KEY')
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
    def __init__(self):
        self.client = Uniswap(
            address=None,
            private_key=None,
            version=3,
            provider=PROVIDER_URL
        )

    def get_token_price(self, token_1, token_2):
        price = self.client.get_price_input(token_1.get("address"), token_2.get("address"), 10**18)
        logging.debug("The Token price is %s", price)
        p = Price(token_1.get("name"), token_2.get("name"), price / 10**18, strftime("%Y%m%dT%H:%M:%S", gmtime()))
        return p

SNT={"name": "SNT", "address": "0x744d70FDBE2Ba4CF95131626614a1763DF805B9E" }
ETH={"name": "ETH", "address": "0x0000000000000000000000000000000000000000"}

def save_price(price):
    with open(FILE_NAME, "a") as file:
        writer = csv.DictWriter(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=["token_1", "token_2", "amount", "time"])
        logging.info(price.to_dict())
        writer.writerow(price.to_dict())

def main():
    client = UniswapClient()
    while True:
        p = client.get_token_price(ETH, SNT)
        logging.info("The 1 eth is worth : %s SNT", p.amount)
        save_price(p)
        sleep(60)

main()

