-- Cumulative UNI burned over time (weekly running total) -> rising line.
-- Tells the "supply permanently shrinking" story (reaches ~106M burned).
WITH weekly AS (
  SELECT date_trunc('week', evt_block_time) AS week, sum(value/1e18) AS burned
  FROM erc20_ethereum.evt_Transfer
  WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
    AND "to" = 0x000000000000000000000000000000000000dEaD
    AND evt_block_time >= timestamp '2025-12-01'
  GROUP BY 1
)
SELECT week, round(sum(burned) OVER (ORDER BY week), 0) AS cumulative_burned_uni
FROM weekly
ORDER BY week
