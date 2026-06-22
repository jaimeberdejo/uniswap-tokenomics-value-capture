#!/usr/bin/env python3
"""
export_dune.py — pull Dune query results into local CSVs (Phase 2 → Phase 4 bridge).

WHAT THIS DOES
  For each Dune query you list in QUERIES below, fetch its results and save them to
  data/<name>.csv with a "data as of" date stamp recorded in data/MANIFEST.csv.
  Those CSVs are the reproducible input for the Phase 4 ML notebook (DEL-03 says the
  notebook must run from cached CSVs WITHOUT a Dune key — so we commit the CSVs, not the key).

PREREQUISITES (your action items — see .planning/phases/02-onchain-data-dune-dashboards/02-RUN-CHECKLIST.md)
  1. Create a free Dune account and an API key.
  2. cp .env.example .env  and put your key in DUNE_API_KEY.
  3. Build + save your queries on dune.com, then paste each query's numeric ID into QUERIES below.
  4. pip install -r requirements.txt   (or just `pip install dune-client pandas python-dotenv`)

USAGE
  python scripts/export_dune.py                 # fetch LATEST saved results (no execution credits)
  python scripts/export_dune.py --execute       # RE-RUN the queries fresh (uses Dune credits)
  python scripts/export_dune.py --only m1_value_waterfall   # just one query by name

WHY "latest" by default: get_latest_result reads the query's last saved run and costs no
execution credits — friendly to the 2,500/mo free tier. Use --execute only when you need
fresh numbers (e.g., a new "data as of" snapshot for the report).
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# EDIT THIS: map a friendly name -> your Dune query ID (the number in the query URL,
# e.g. dune.com/queries/1234567 -> 1234567). Leave the ID as None until you've built
# the query on Dune; the script skips Nones with a clear message.
# Names map to the M1–M5 metrics in FOUNDATION.md §Metric Shortlist.
# ---------------------------------------------------------------------------
QUERIES: dict[str, int | None] = {
    "headline_metrics": 7773259,       # DATA-04: supply, market cap, annualized burn, burn yield
    "burn_over_time_usd": 7773260,     # DATA-01/05: weekly UNI burned + USD value
    "net_supply_mint_burn": 7773261,   # DATA-05: weekly minted vs burned (mints = 0)
    "uniswap_volume_weekly": 7773262,  # DATA-01: weekly Uniswap volume (fee-switch usage check)
    "top_holders": 7773263,            # DATA-02: top-25 holders, entity-flagged concentration
    "cumulative_burn": 7773381,        # cumulative UNI burned over time (-> ~106M)
    "governance_turnout": 7773416,  # DATA-03: turnout by proposal (#93 = UNIfication)
    "delegated_power": 7773417,
    "concentration_gini_nakamoto": 7773493,      # DATA-03: delegated voting-power concentration
}

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MANIFEST = DATA_DIR / "MANIFEST.csv"


def _load_key() -> str:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except ImportError:
        pass  # python-dotenv optional; env var may already be set
    key = os.environ.get("DUNE_API_KEY", "").strip()
    if not key:
        sys.exit(
            "ERROR: DUNE_API_KEY is not set.\n"
            "  cp .env.example .env  and add your key, or:  export DUNE_API_KEY=...\n"
            "  Get a key: dune.com -> Settings -> API."
        )
    return key


def _record_manifest(name: str, rows: int, cols: int, mode: str, stamp: str) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    new = not MANIFEST.exists()
    with MANIFEST.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "rows", "cols", "fetch_mode", "data_as_of_utc"])
        w.writerow([f"{name}.csv", rows, cols, mode, stamp])


def main() -> int:
    ap = argparse.ArgumentParser(description="Export Dune query results to data/*.csv")
    ap.add_argument("--execute", action="store_true",
                    help="re-run queries fresh (uses Dune credits) instead of fetching latest saved results")
    ap.add_argument("--only", metavar="NAME", help="export just one query by its name key in QUERIES")
    args = ap.parse_args()

    try:
        from dune_client.client import DuneClient
        from dune_client.query import QueryBase
    except ImportError:
        sys.exit("ERROR: dune-client not installed. Run: pip install -r requirements.txt")

    dune = DuneClient(_load_key())
    DATA_DIR.mkdir(exist_ok=True)

    items = QUERIES.items()
    if args.only:
        if args.only not in QUERIES:
            sys.exit(f"ERROR: --only '{args.only}' not in QUERIES. Choices: {', '.join(QUERIES)}")
        items = [(args.only, QUERIES[args.only])]

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    exported, skipped = 0, 0
    for name, qid in items:
        if qid is None:
            print(f"  - {name}: SKIPPED (no query ID yet — add it to QUERIES in this file)")
            skipped += 1
            continue
        print(f"  - {name}: fetching query {qid} ({'execute' if args.execute else 'latest'})...")
        try:
            if args.execute:
                df = dune.run_query_dataframe(QueryBase(query_id=qid))
            else:
                df = dune.get_latest_result_dataframe(qid)
        except Exception as e:  # noqa: BLE001 — surface any Dune/network error plainly
            print(f"    ! FAILED: {e}")
            continue
        out = DATA_DIR / f"{name}.csv"
        df.to_csv(out, index=False)
        _record_manifest(name, len(df), len(df.columns), "execute" if args.execute else "latest", stamp)
        print(f"    -> wrote {out.relative_to(DATA_DIR.parent)} ({len(df)} rows x {len(df.columns)} cols)")
        exported += 1

    print(f"\nDone. {exported} exported, {skipped} skipped. Data as of {stamp} (UTC).")
    if exported:
        print("Next: commit the CSVs (they are the reproducible Phase-4 input) — but NEVER commit .env.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
