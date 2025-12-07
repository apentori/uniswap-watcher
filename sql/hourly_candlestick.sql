--- This is an example of SQL query to generate candlestick graphs based on the price with clickhouse

WITH tmp_prices AS (
  SELECT
    token_1,
    token_2,
    update_on,
    amount as price
  FROM prices
  WHERE token_1 = 'ETH' AND token_2 = 'SNT' -- Replace with your desired token pair
)
SELECT
    token_1,
    token_2,
    toStartOfHour(update_on) AS hour_interval,
    argMin(price, update_on) AS open,
    max(price) AS high,
    min(price) AS low,
    argMax(price, update_on) AS close
FROM tmp_prices
GROUP BY
    token_1,
    token_2,
    hour_interval
ORDER BY hour_interval ASC;

