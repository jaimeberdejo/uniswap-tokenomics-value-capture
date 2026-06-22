-- Uniswap weekly trading volume on Ethereum + blended LP-fee estimate (M1, volume side)
-- Checks whether the fee switch hurt usage (volume before vs after 28-Dec-2025).
-- LP fee is a ~0.19% blended estimate of the real per-tier fee; refine per-tier if needed.
-- Metric coverage: "Volume before vs after fee switch".
SELECT
  date_trunc('week', block_time) AS week,
  round(sum(amount_usd))            AS volume_usd,
  round(sum(amount_usd) * 0.0019)   AS lp_fees_usd_est
FROM dex.trades
WHERE blockchain = 'ethereum'
  AND project = 'uniswap'
  AND block_time >= timestamp '2025-09-01'
GROUP BY 1
ORDER BY 1
