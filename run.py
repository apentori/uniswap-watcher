#!/usr/bin/env python
import logging
import click
from uniswap_watcher.config import load_config
from uniswap_watcher.watcher import watch

@click.command()
@click.option("-c", "--config-file", default="config.yaml", help="Path to the config file")
@click.option("-l", "--log-level",   default="INFO",        help="Log Level")
def run(config_file, log_level):
    logging.basicConfig(level=log_level.upper())
    config = load_config(config_file)
    watch(config)


if __name__ == "__main__":
    run()
