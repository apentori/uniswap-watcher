from uniswap_watcher.models.price import Price
from uniswap_watcher.config import DATE_FORMAT, DEFAULT_PRICE_FORMAT
from uniswap import Uniswap
from time import gmtime, strftime
import logging

class UniswapClient:
    def __init__(self, url: str, api_key: str, address: str = None, private_key: str=None):
        self.client = Uniswap(
            address=address,
            private_key=private_key,
            version=3,
            provider=f"{url}/{api_key}"
        )

    def get_token_price(self, token_1, token_2):
        logging.debug("Calling Uniswap contract to get price for par %s-%s", token_1, token_2)
        price = self.client.get_price_input(token_1.get("address"), token_2.get("address"), DEFAULT_PRICE_FORMAT)
        logging.debug("The Token price is %s", price)
        p = Price(token_1=token_1.get("name"),
                token_2=token_2.get("name"),
                amount=price / DEFAULT_PRICE_FORMAT,
                time=strftime(DATE_FORMAT, gmtime()))
        return p

