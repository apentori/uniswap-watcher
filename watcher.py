#!/usr/bin/env python
import os
import logging
import json
from web3 import Web3
from uniswap import Uniswap

logging.basicConfig(level=logging.INFO)

api_key=os.environ.get('INFURA_API_KEY')
infura_url = f"https://mainnet.infura.io/v3/{api_key}"
logging.info("infura URL : %s ", infura_url)
uniswap = Uniswap(
    address=None,
    private_key=None,
    version=3,
    provider=infura_url
)
snt= '0x744d70FDBE2Ba4CF95131626614a1763DF805B9E'
weth='0x0000000000000000000000000000000000000000'

price = uniswap.get_price_input(weth, snt, 10**18)
logging.info(price)
