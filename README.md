# Uniswap Pair Watcher

## Description

Small app to monitor Uniswap Pool price.

## Fonctionnality

## Configuration

Set up the configuration file `config.yaml`.

The extraction configuration is handle by those parameters
```yaml
provider_url: "https://mainnet.infura.io/v3/"
api_key: ""
# Frequency of Call to Uniswap
frequency: 600
generate_candlestick: false
```

The database configuration with:
```yaml
database:
  type: clickhouse # Also available for postgres
  host: db
  port: 9000
  username: watcher
  password: password
  database: watcher
```

The pool to monitores:
```yaml
token_to_tracks:
  - pair_name: "SNT-ETH"
    base:
      name: "ETH"
      address: "0x0000000000000000000000000000000000000000"
    against:
      name: "SNT"
      address: "0x744d70FDBE2Ba4CF95131626614a1763DF805B9E"
  - pair_name: "ETH-USDT"
    base:
      name: "ETH"
      address: "0x0000000000000000000000000000000000000000"
    against:
      name: "USDT"
      address: "0xdAC17F958D2ee523a2206206994597C13D831ec7"
```

## Running

Run the `docker-compose.yaml` file.
The python code can be run on it's on, with:

```bash
run.py --config-path config.yaml \
  --api-key $INFURA_KEY \
  --db-password $DB_PASSWORD
```
> Each configuration parameter can be pass as a environment variable, prefixed with `WATCHER_`.

## Functionnality

* Extract price of Token according to Uniswap Pool
* Todos:
  * Calculate the volume of transaction for each pool.
