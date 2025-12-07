import logging
from time import sleep
from threading import Thread
from datetime import datetime, timedelta

from uniswap_watcher.clients import DatabaseClient, UniswapClient
from uniswap_watcher.models import Candlestick, Price
from sqlalchemy.orm import sessionmaker

def calculate_candlestick(prices, token_1, token_2):
    if not prices:
        return None

    open_price = prices[0].amount
    close_price = prices[-1].amount
    high_price = max(p.amount for p in prices)
    low_price = min(p.amount for p in prices)
    volume = 0  # Todo find correct way to calculate values

    return Candlestick(
        token_1=token_1,
        token_2=token_2,
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
        volume=volume,
        period_start=datetime.utcnow().replace(minute=0, second=0, microsecond=0),
    )

def calculate_hourly_candlesticks(dbClient: DatabaseClient, config):
    logging.info("Starting thread for candlestick calculation")
    while True:
        # Get all unique token pairs (adjust query as needed)
        for pair in config:
            logging.info("Calculating hourly candlestick for %s", pair)
            prices = dbClient.get_hourly_prices(pair.get("base").get("name"), pair.get("against").get("name"))
            candlestick = calculate_candlestick(prices, pair.get("base").get("name"), pair.get("against").get("name"))
            if candlestick:
                dbClient.store_candlestick(candlestick)
        next_run = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        sleep((next_run - datetime.now()).total_seconds())

def watch(config):
    logging.info("Configuring the clients")
    client = UniswapClient(url=config.provider_url, api_key=config.api_key)
    dbClient = DatabaseClient(config.database)
    logging.info("And now my watch begins")
    if config.generate_candlestick:
        Thread(
            target=calculate_hourly_candlesticks,
            args=(dbClient, config.token_to_tracks),
            daemon=True
        ).start()
    while True:
        for pair in config.token_to_tracks:
            logging.info("Watching for pair %s", pair.get("pair_name"))
            p = client.get_token_price(pair.get("base"), pair.get("against"))
            logging.info("Pair %s is now price %s", pair.get("pair_name"), p.amount)
            dbClient.insert(p)
        logging.info("Sleeping until the next check")
        sleep(config.frequency)



