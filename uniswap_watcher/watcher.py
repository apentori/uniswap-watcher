import logging
from time import sleep

from uniswap_watcher.clients import PostgresClient, UniswapClient, ClickhouseClient


def watch(config):
    logging.info("Configuring the clients")
    client = UniswapClient(url=config.provider_url, api_key=config.api_key)
    dbClient = None
    if config.database.get("type") == "postgres":
        dbClient = PostgresClient(
            config.database.get("host"),
            config.database.get("port"),
            config.database.get("database"),
            config.database.get("username"),
            config.database.get("password"))
    else:
        dbClient = ClickhouseClient(
            config.database.get("host"),
            config.database.get("port"),
            config.database.get("database"),
            config.database.get("username"),
            config.database.get("password"))
    logging.info("And now my watch begins")
    while True:
        for pair in config.token_to_tracks:
            logging.info("Watching for pair %s", pair.get("pair_name"))
            p = client.get_token_price(pair.get("base"), pair.get("against"))
            logging.info("Pair %s is now price %s", pair.get("pair_name"), p.amount)
            dbClient.insert(p)
        logging.info("Sleeping until the next check")
        sleep(config.frequency)



