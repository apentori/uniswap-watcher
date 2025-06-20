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
web3 = Web3(Web3.HTTPProvider(infura_url))

if not web3.is_connected():
    raise Exception("Not connected to Ethereum network")

uniswap_router_address = '0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af'# '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'

def load_abi():
    with open('contract-abi.json', 'r') as f:
        abi = json.load(f)
        return abi

uniswap_router_abi = load_abi()

uniswap_router = web3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)

path = [
    '0x744d70fdbe2ba4cf95131626614a1763df805b9e'
]

amount_out = uniswap_router.functions.getAmounts(amount_in, path).call()

logging.info("Amount out: %s", amount_out[-1])
