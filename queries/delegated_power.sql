-- Delegated voting-power concentration (M3 / DATA-03).
-- Voting power follows DELEGATION, not balances: latest newBalance per delegate.
-- Finding: top delegate ~7%, ~12 delegates reach 50% (Nakamoto ~12) — more distributed
-- than token holdings (treasury alone is 30% of supply).
WITH latest AS (
  SELECT delegate, "newBalance"/1e18 AS vp,
    row_number() OVER (PARTITION BY delegate ORDER BY evt_block_number DESC, evt_index DESC) AS rn
  FROM uniswap_ethereum.uni_evt_delegatevoteschanged
),
cur AS (SELECT delegate, vp FROM latest WHERE rn = 1 AND vp > 0)
SELECT delegate,
       round(vp, 0) AS voting_power,
       round(100.0 * vp / (SELECT sum(vp) FROM cur), 2) AS pct_of_delegated
FROM cur
ORDER BY vp DESC
LIMIT 25
