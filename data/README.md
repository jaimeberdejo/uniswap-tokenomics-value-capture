# data/ — cached Dune query exports

These CSVs are the **reproducible, author-generated** outputs of the Phase 2 Dune queries.
They are the input to the Phase 4 ML notebook, which (per DEL-03) must run from these CSVs
**without** a Dune API key. So: **commit the CSVs**, never commit `.env` or any key.

Populate them by running `python scripts/export_dune.py` after you've built the queries on
Dune and added their IDs to `scripts/export_dune.py`. Each run also appends a row to
`MANIFEST.csv` recording the row/column counts and the "data as of" UTC timestamp.

## Expected files (one per metric — see FOUNDATION.md §Metric Shortlist)

| File | Metric | Requirement | Expected columns (guide — finalize when you build the query) |
|------|--------|-------------|--------------------------------------------------------------|
| `m1_value_waterfall.csv` | Value waterfall, weekly | DATA-01 | `week, volume_usd, lp_fees_usd, protocol_fees_usd, uni_burned_usd` |
| `m2_holder_concentration.csv` | Holder concentration | DATA-02 | `metric, raw, entity_adjusted` (top10/top50/top100 share, Gini, Nakamoto) |
| `m3_governance_power.csv` | Governance voting power | DATA-03 | `delegate, voting_power, share` (+ a turnout summary row/file) |
| `m4_supply_fdv.csv` | Circulating vs FDV | DATA-04 | `date, circulating, total_supply_onchain, price_usd, market_cap, fdv` |
| `m5_issuance_vs_burn.csv` | Net supply trajectory | DATA-05 | `week, inflation_uni, growth_budget_uni, burned_uni, net_delta_uni` |

Column names are a starting guide from the Phase 1 shortlist — adjust to whatever your
verified queries actually return, then update this table to match.

## Data hygiene reminders (from PITFALLS.md)
- **Decimals:** UNI = 18, USDC = 6 — confirm your query already divided by `1e18`/`1e6`. Hand-test one known swap.
- **"data as of":** every chart/figure in the report cites the `MANIFEST.csv` timestamp.
- **Supply:** `total_supply_onchain` comes from `totalSupply()` onchain, never a hardcoded 1B.
</content>
