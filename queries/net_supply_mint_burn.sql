-- UNI Net Supply: minted vs burned, weekly (M5)
-- minted = transfers FROM the zero address (new issuance / inflation / growth budget)
-- burned = transfers TO the dead address
-- Finding: minted is 0 — UNI's 2% inflation cap is unused, so UNI is currently net-deflationary.
-- Metric coverage: "Growth budget/emissions", "UNI supply before/after".
SELECT
  date_trunc('week', evt_block_time) AS week,
  sum(CASE WHEN "from" = 0x0000000000000000000000000000000000000000 THEN value/1e18 ELSE 0 END) AS minted_uni,
  sum(CASE WHEN "to"   = 0x000000000000000000000000000000000000dEaD THEN value/1e18 ELSE 0 END) AS burned_uni
FROM erc20_ethereum.evt_Transfer
WHERE contract_address = 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
  AND ("from" = 0x0000000000000000000000000000000000000000
       OR "to" = 0x000000000000000000000000000000000000dEaD)
  AND evt_block_time >= timestamp '2025-09-01'
GROUP BY 1
ORDER BY 1
