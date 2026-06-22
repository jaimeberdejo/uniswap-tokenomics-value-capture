-- Daily USD price for UNI vs WETH vs AAVE (Dec 2025 – Jun 2026), for the Phase 5
-- "market evidence is suggestive, not conclusive" comparison: did UNI fall on its
-- own (burn-specific) or alongside ETH/DeFi peers (broader market forces)?
-- Source: Dune prices.usd (per-minute oracle prices), daily-averaged.
-- Cached to data/price_comparison.csv (data-as-of 2026-06-22) for the notebook/report.
SELECT cast(date_trunc('day', minute) AS date) AS day,
       symbol,
       round(avg(price), 4) AS price_usd
FROM prices.usd
WHERE contract_address IN (
  0x1f9840a85d5af5bf1d1762f925bdaddc4201f984,  -- UNI
  0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,  -- WETH (ETH)
  0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9   -- AAVE
)
  AND blockchain = 'ethereum'
  AND minute >= timestamp '2025-12-01'
  AND minute <  timestamp '2026-06-23'
GROUP BY 1, 2
ORDER BY 1, 2
