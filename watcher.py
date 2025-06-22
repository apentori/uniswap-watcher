#!/usr/bin/env python
import os
import logging
import json
import time
from web3 import Web3
from uniswap import Uniswap

logging.basicConfig(level=logging.INFO)

PROVIDER_URL = os.environ.get('INFURA_BASE_URL','https://mainnet.infura.io/v3/') + os.environ.get('INFURA_API_KEY')

class UniswapClient:
    def __init__(self):
        self.client = Uniswap(
            address=None,
            private_key=None,
            version=3,
            provider=PROVIDER_URL
        )

    def get_token_price(self, token_1, token_2):
        price = self.client.get_price_input(token_1, token_2, 10**18)
        logging.degbut("The Token price is %s", price)
        return price / 10**18

SNT_ADDRESS= '0x744d70FDBE2Ba4CF95131626614a1763DF805B9E'
ETH_ADDRESS='0x0000000000000000000000000000000000000000'

def main():
    client = UniswapClient()
    while True:
        p = client.get_token_price(ETH_ADDRESS, SNT_ADDRESS)
        logging.info("The 1 eth is worth : %s SNT", p)
        time.sleep(5)

main()

