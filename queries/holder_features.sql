-- Per-wallet behavioral features for the top 1,000 UNI holders (Phase 4 ML input).
-- Extends the Phase-2 top_holders balance query (sum of transfer flows per address)
-- with activity/age/flow features so the Phase-4 notebook can cluster real behaviour
-- (size + activity + tenure + dormancy), not just balance bins.
-- Source: erc20_ethereum.evt_Transfer for UNI 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984.
-- Balance = sum(received) - sum(sent). Burn/zero addresses excluded. Cached to
-- data/holder_features.csv (data-as-of in MANIFEST.csv) so the notebook runs WITHOUT a Dune key (DEL-03).
WITH flows AS (
  SELECT "to" AS addr, value/1e18 AS amt, evt_block_time AS ts
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
  UNION ALL
  SELECT "from" AS addr, -value/1e18 AS amt, evt_block_time AS ts
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
),
agg AS (
  SELECT addr,
    sum(amt) AS balance,
    count(*) AS n_transfers,
    sum(CASE WHEN amt > 0 THEN amt ELSE 0 END) AS total_in,
    sum(CASE WHEN amt < 0 THEN -amt ELSE 0 END) AS total_out,
    min(ts) AS first_seen,
    max(ts) AS last_seen
  FROM flows
  GROUP BY 1
  HAVING sum(amt) > 1
)
SELECT addr,
  round(balance, 2) AS balance_uni,
  round(100.0 * balance / 893790420, 5) AS pct_of_supply,
  n_transfers,
  round(total_in, 2) AS total_in_uni,
  round(total_out, 2) AS total_out_uni,
  cast(first_seen AS varchar) AS first_seen,
  cast(last_seen AS varchar) AS last_seen,
  date_diff('day', first_seen, last_seen) AS active_span_days,
  date_diff('day', last_seen, cast(now() AS timestamp)) AS days_since_last
FROM agg
WHERE addr NOT IN (
  0x000000000000000000000000000000000000dEaD,
  0x0000000000000000000000000000000000000000
)
ORDER BY balance DESC
LIMIT 1000
