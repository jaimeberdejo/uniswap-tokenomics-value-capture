-- UNI Headline Value-Capture Metrics (single row)
-- Supply (net of burns), market cap, annualized burn rate, and BURN YIELD.
-- burn_yield_pct = annualized burned UNI / circulating supply (the "dividend-equivalent").
-- Metric coverage: "UNI supply before/after", "Annualized burn rate", "Burn yield".
WITH cum AS (
  SELECT sum(value/1e18) AS cumulative_burned
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    AND "to" = 0x000000000000000000000000000000000000dEaD
),
recent AS (
  SELECT sum(value/1e18) AS burned_90d
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    AND "to" = 0x000000000000000000000000000000000000dEaD
    AND evt_block_time >= now() - interval '90' day
),
price AS (
  SELECT price FROM prices.usd
  WHERE blockchain = 'ethereum'
    AND contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
  ORDER BY minute DESC LIMIT 1
)
SELECT
  round(cum.cumulative_burned, 0)                              AS cumulative_burned_uni,
  round(1e9 - cum.cumulative_burned, 0)                        AS total_supply_uni,
  round(price.price, 2)                                        AS uni_price_usd,
  round((1e9 - cum.cumulative_burned) * price.price / 1e9, 2)  AS market_cap_usd_bn,
  round(recent.burned_90d * (365.0/90), 0)                     AS annualized_burn_uni,
  round(recent.burned_90d * (365.0/90) * price.price / 1e6, 2) AS annualized_burn_usd_mn,
  round(100.0 * (recent.burned_90d * (365.0/90)) / (1e9 - cum.cumulative_burned), 3) AS burn_yield_pct
FROM cum, recent, price
