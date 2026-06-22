-- UNI Burn Over Time (weekly) + USD value
-- Burn = UNI transferred to the dead address (Firepit routes burns there).
-- Burn value = burned UNI x weekly avg UNI price (priced on Dune itself).
-- Metric coverage: "UNI burned over time", "Burn value in USD".
WITH burns AS (
  SELECT date_trunc('week', evt_block_time) AS week, sum(value/1e18) AS burned_uni
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    AND "to" = 0x000000000000000000000000000000000000dEaD
    AND evt_block_time >= timestamp '2025-12-01'
  GROUP BY 1
),
px AS (
  SELECT date_trunc('week', minute) AS week, avg(price) AS uni_price
  FROM prices.usd
  WHERE blockchain = 'ethereum'
    AND contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    AND minute >= timestamp '2025-12-01'
  GROUP BY 1
)
SELECT b.week,
       round(b.burned_uni, 0)               AS burned_uni,
       round(p.uni_price, 2)                AS uni_price,
       round(b.burned_uni * p.uni_price, 0) AS burn_usd
FROM burns b
LEFT JOIN px p ON b.week = p.week
ORDER BY b.week
