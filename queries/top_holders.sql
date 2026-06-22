-- Top UNI holders (concentration, M2), derived from full transfer history.
-- Balances = sum(received) - sum(sent) per address. Burn/zero addresses excluded.
-- Known entities flagged so raw vs entity-adjusted concentration is visible (address != entity).
-- Metric coverage: "Holder concentration".
WITH flows AS (
  SELECT "to" AS addr, value/1e18 AS amt
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
  UNION ALL
  SELECT "from" AS addr, -value/1e18 AS amt
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
),
bal AS (
  SELECT addr, sum(amt) AS balance
  FROM flows
  GROUP BY 1
  HAVING sum(amt) > 1
)
SELECT
  addr,
  round(balance, 0) AS balance_uni,
  round(100.0 * balance / 893790420, 3) AS pct_of_supply,
  CASE addr
    WHEN 0x1a9c8182c09f50c8318d769245bea52c32be35bc THEN 'Uniswap Timelock/Treasury'
    WHEN 0xf977814e90da44bfa03b6295a0616a897441acec THEN 'Binance (CEX)'
    WHEN 0x28c6c06298d514db089934071355e5743bf21d60 THEN 'Binance (CEX)'
    ELSE 'unlabeled'
  END AS entity
FROM bal
WHERE addr NOT IN (
  0x000000000000000000000000000000000000dEaD,
  0x0000000000000000000000000000000000000000
)
ORDER BY balance DESC
LIMIT 25
