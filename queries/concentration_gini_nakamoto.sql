-- Holder concentration: Gini + Nakamoto (M2 / DATA-02), entity-adjusted.
-- Excludes burn/zero/treasury/CEX so the number reflects real holders.
-- Gini ~0.995 (huge long tail of tiny holders); Nakamoto ~39 (addresses to reach 50%).
WITH flows AS (
  SELECT "to" AS addr, value/1e18 AS amt FROM erc20_ethereum.evt_Transfer
   WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
  UNION ALL
  SELECT "from" AS addr, -value/1e18 AS amt FROM erc20_ethereum.evt_Transfer
   WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
),
bal AS (SELECT addr, sum(amt) AS balance FROM flows GROUP BY 1 HAVING sum(amt) > 0.01),
adj AS (
  SELECT balance FROM bal WHERE addr NOT IN (
    0x000000000000000000000000000000000000dEaD, 0x0000000000000000000000000000000000000000,
    0x1a9c8182c09f50c8318d769245bea52c32be35bc, 0xf977814e90da44bfa03b6295a0616a897441acec,
    0x28c6c06298d514db089934071355e5743bf21d60)
),
r AS (SELECT balance, row_number() OVER (ORDER BY balance) AS i, count(*) OVER () AS n, sum(balance) OVER () AS tot FROM adj),
nak AS (SELECT row_number() OVER (ORDER BY balance DESC) AS rnk, sum(balance) OVER (ORDER BY balance DESC) AS cum, sum(balance) OVER () AS tot FROM adj)
SELECT
  (SELECT count(*) FROM adj) AS holders,
  round((SELECT (2.0*sum(i*balance)/(max(n)*max(tot))) - (max(n)+1.0)/max(n) FROM r), 4) AS gini_entity_adjusted,
  (SELECT min(rnk) FROM nak WHERE cum >= 0.5*tot) AS nakamoto_entity_adjusted
