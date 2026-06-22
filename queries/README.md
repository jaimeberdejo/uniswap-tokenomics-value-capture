# queries/ — your Dune SQL (you author these)

This folder is intentionally left for **you** to fill in as you learn Dune + SQL (learning
guide Stage 4). Claude deliberately did **not** pre-write the SQL, because (a) it's your
graded analysis and (b) DuneSQL table/spell names drift and must be verified live in the
Dune catalog — pre-written SQL would likely be stale.

When you build each query on dune.com, also save a copy here as `m1_value_waterfall.sql`,
etc., so the repo has a versioned record (DATA-06 wants versioned queries). Then paste the
query's numeric ID into `scripts/export_dune.py` so the exporter can pull its results.

## What each query must compute — the spec is already written

You do **not** start from a blank page. The exact definition, fee parameters, entity-exclusion
list, waterfall formula, and reconciliation cross-check for every query are in:

> **`.planning/phases/01-foundation-research-reframing/FOUNDATION.md` → "## Metric Shortlist" (M1–M5)**

| File to create | Metric | Requirement |
|----------------|--------|-------------|
| `m1_value_waterfall.sql` | volume → LP fees → protocol fees → UNI burned, weekly across 28-Dec-2025 | DATA-01 |
| `m2_holder_concentration.sql` | top-N + Gini + Nakamoto, raw AND entity-adjusted | DATA-02 |
| `m3_governance_power.sql` | delegated voting-power concentration + UNIfication turnout | DATA-03 |
| `m4_supply_fdv.sql` | circulating vs total(onchain) vs FDV, post-burn | DATA-04 |
| `m5_issuance_vs_burn.sql` | weekly net supply: (inflation + 20M/yr budget) − Firepit burns | DATA-05 |
| `decimals_handtest.sql` | reproduce ONE known UNI swap by hand (Pitfall 6 guard) | — |

## Before you trust any query (PITFALLS.md P6)
1. Verify each table exists and is fresh: `SELECT max(block_time) FROM <table>`.
2. Normalize decimals explicitly (UNI `/1e18`, USDC `/1e6`); confirm with `decimals_handtest.sql`.
3. Pin time buckets to **UTC**.
4. If you forked a community query, rewrite its WHERE/SUM logic in your own words first and
   confirm whether its "fees" means **LP fees** or **protocol fees** (Pitfall 3).
5. Cross-check one month's totals against DefiLlama/Token Terminal within ~±10%.
</content>
