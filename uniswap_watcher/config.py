from yaml import safe_load
import logging

"""
DEFAULT CONFIGURATION
"""
DATE_FORMAT="%Y%m%dT%H:%M:%S"
DEFAULT_PRICE_FORMAT=10**18

config=None

class Config:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def load_config(config_path: str, api_key: str, db_password: str):
    logging.debug("Loading configuration from file %s", config_path)
    with open(config_path) as f:
        logging.debug("Opening config file %s", config_path)
        c=safe_load(f)
        logging.info("API KEY : %s", api_key)
        if api_key:
            logging.info("Using API KEY from environment variable")
            c["api_key"] = api_key
        if db_password:
            logging.info("Using db password from environment variable")
            c.get("database")["password"] = db_password

        config=Config(**c)
        logging.debug("Configuration loaded")
        return config

