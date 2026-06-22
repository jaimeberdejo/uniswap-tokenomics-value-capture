-- Governance turnout by proposal (M3 / DATA-03), Uniswap Governor Bravo.
-- Proposal #93 = UNIfication (125.3M UNI for, 742 against, ~98.8%) — the standout.
-- support: 1=for, 0=against, 2=abstain.
SELECT "proposalId" AS proposal,
  count(*) AS voters,
  round(sum(CASE WHEN support=1 THEN votes/1e18 ELSE 0 END), 0) AS for_uni,
  round(sum(CASE WHEN support=0 THEN votes/1e18 ELSE 0 END), 0) AS against_uni,
  round(sum(CASE WHEN support=2 THEN votes/1e18 ELSE 0 END), 0) AS abstain_uni,
  min(evt_block_time) AS started
FROM uniswap_v3_ethereum.governorbravodelegate_evt_votecast
WHERE evt_block_time >= timestamp '2025-10-01'
GROUP BY 1
ORDER BY started DESC
