#!/usr/bin/env python3
"""Assemble notebooks/ml-analysis.ipynb (the graded DEL-03 artifact) from the
validated companion notebooks/ml_analysis.py.

The notebook imports the validated functions from the .py companion and calls them
section by section, so the .ipynb reproduces the .py numbers/figures exactly
(random_state=42) and runs top-to-bottom from cached data/*.csv with NO Dune key.
Sections (markdown headers): Setup/load -> Clustering (AI-02) -> Anomaly (AI-03)
-> Break-even (AI-04) -> "How this sharpens the verdict" recap.
"""
from __future__ import annotations

from pathlib import Path

import nbformat as nbf
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "notebooks" / "ml-analysis.ipynb"

nb = new_notebook()
cells = []

cells.append(new_markdown_cell(
    "# Phase 4 — AI/ML Layer: Uniswap Tokenomics\n"
    "\n"
    "**Reproducible (DEL-03):** this notebook runs top-to-bottom from the cached "
    "`data/*.csv` snapshots with **no Dune key** and **no network call**. It imports the "
    "validated companion `notebooks/ml_analysis.py` so the numbers and figures here "
    "reproduce that script exactly (`random_state=42`).\n"
    "\n"
    "**Additive & cuttable:** this layer only *sharpens* the Phase-3 verdict "
    "(\"real but modest & unproven\"); it reads Phase 1-3 artifacts as inputs only and "
    "deleting it breaks no Phase 1-3 / verdict claim (the delete-the-AI-section test).\n"
    "\n"
    "Three outputs, each ending in a **\"Sharpens the verdict:\"** sentence:\n"
    "1. AI-02 — wallet clustering (KMeans)\n"
    "2. AI-03 — anomaly detection (IsolationForest)\n"
    "3. AI-04 — buy-and-burn break-even model"
))

# --- Setup / load -----------------------------------------------------------
cells.append(new_markdown_cell(
    "## 1. Setup / load\n"
    "Import the validated companion module and the cached holder/entity data. "
    "All paths are repo-relative `data/` so this runs in Colab/Jupyter from the repo."
))
cells.append(new_code_cell(
    "import importlib.util\n"
    "from pathlib import Path\n"
    "\n"
    "# Locate the repo root from the notebook's location (notebooks/ -> parent).\n"
    "REPO_ROOT = Path.cwd()\n"
    "if (REPO_ROOT / 'notebooks').exists() and (REPO_ROOT / 'data').exists():\n"
    "    pass  # launched from repo root\n"
    "elif REPO_ROOT.name == 'notebooks':\n"
    "    REPO_ROOT = REPO_ROOT.parent\n"
    "else:\n"
    "    # Fallback: search upward for a dir containing data/ and notebooks/.\n"
    "    p = REPO_ROOT\n"
    "    while p != p.parent and not ((p / 'data').exists() and (p / 'notebooks').exists()):\n"
    "        p = p.parent\n"
    "    REPO_ROOT = p\n"
    "\n"
    "_spec = importlib.util.spec_from_file_location(\n"
    "    'ml', REPO_ROOT / 'notebooks' / 'ml_analysis.py')\n"
    "ml = importlib.util.module_from_spec(_spec)\n"
    "_spec.loader.exec_module(ml)\n"
    "\n"
    "ml._ensure_figures_dir()\n"
    "df = ml.load_holder_features()\n"
    "entities = ml.load_entity_labels()\n"
    "as_of = ml.holder_features_as_of()\n"
    "print('holder_features rows:', len(df))\n"
    "print('columns:', list(df.columns))\n"
    "print('data-as-of:', as_of)"
))

# --- Clustering (AI-02) -----------------------------------------------------
cells.append(new_markdown_cell(
    "## 2. Clustering (AI-02)\n"
    "KMeans on log-scaled, StandardScaler-normalized behavioral features of the top-1000 "
    "UNI holders; silhouette-driven `k`; honest centroid-labeled archetypes; PCA scatter; "
    "treasury/CEX spot-check. Figures: `analysis/figures/silhouette.png`, `clusters.png`."
))
cells.append(new_code_cell("clustering = ml.run_clustering(df, entities, as_of)"))

# --- Anomaly (AI-03) --------------------------------------------------------
cells.append(new_markdown_cell(
    "## 3. Anomaly detection (AI-03)\n"
    "IsolationForest (`random_state=42`) on (a) the **same** holder feature matrix -> "
    "flagged wallets each mapped to a stated insight and cross-referenced to entity labels; "
    "and (b) the weekly burn series with the **2025-12-22 100M-burn week whitelisted**, "
    "reporting any OTHER anomalous weeks. Figure: `analysis/figures/anomalies.png`."
))
cells.append(new_code_cell("anomaly = ml.run_anomaly_detection(df, entities, as_of)"))

# --- Break-even (AI-04) -----------------------------------------------------
cells.append(new_markdown_cell(
    "## 4. Break-even (AI-04)\n"
    "The daily Uniswap volume at which protocol-fee buy-and-burn turns UNI "
    "net-deflationary, in two issuance scenarios: (a) current issuance = 0 (headroom) and "
    "(b) 2% tail + 20M/yr growth re-enabled (break-even daily volume). Constants are "
    "documented and traceable to FOUNDATION.md / headline_metrics.csv. The only price used "
    "is the static cached spot for USD->UNI conversion — **no price prediction**. "
    "Figure: `analysis/figures/breakeven.png`."
))
cells.append(new_code_cell("breakeven = ml.run_breakeven(as_of)"))

# --- Report context figures -------------------------------------------------
cells.append(new_markdown_cell(
    "## 5. Report context figures (before/after UNIfication)\n"
    "Spanish-labelled context charts embedded in the report body, all read from the "
    "cached `data/*.csv` (no network): weekly volume + burn value "
    "(`volume_burn_timeline.png`), UNI vs ETH vs AAVE rebased to 100 at UNIfication "
    "(`price_comparison.png`), and Uniswap TVL (`tvl_timeline.png`)."
))
cells.append(new_code_cell(
    "fig_volume_burn = ml.make_volume_burn_timeline()\n"
    "fig_price = ml.make_price_comparison()\n"
    "fig_tvl = ml.make_tvl_timeline()"
))

# --- Recap ------------------------------------------------------------------
cells.append(new_markdown_cell(
    "## 6. How this sharpens the verdict\n"
    "Each output ends in one verdict-sharpening sentence (printed above); restated here:\n"
    "\n"
    "- **AI-02 (clustering):** the holder base splits into distinct behavioral archetypes, "
    "with a high-balance custodial/treasury *whale* cluster apart from dispersed "
    "active/retail holders — so pro-rata burn value capture concentrates in a few large "
    "wallets rather than meaningfully reaching dispersed holders.\n"
    "- **AI-03 (anomaly):** no hidden second structural burn beyond the one-time 100M "
    "UNIfication event, and the flagged wallets are dominated by labeled custodial/CEX "
    "churn — reinforcing that value capture is real but modest and concentrated, not a "
    "broad reflexive flywheel.\n"
    "- **AI-04 (break-even):** net-deflationary at any volume while issuance is 0, but a "
    "re-enabled 2% tail + 20M growth budget would require ~3x today's volume to stay "
    "deflationary — so sustainability is conditional on volume holding up **and** the "
    "revocable zero-issuance policy persisting.\n"
    "\n"
    "**Honest scope / delete-the-AI-section note:** clustering covers only the top-1000 "
    "holders (long-tail and on-DEX LP-position detection are out of this snapshot); the "
    "break-even uses a static spot price purely for USD->UNI conversion (no forecast). This "
    "whole layer reads Phase 1-3 artifacts as inputs only and asserts **no new verdict** — "
    "removing it breaks nothing upstream. It sharpens, never gates, the Phase-3 verdict: "
    "*real but modest & unproven.*"
))

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}

OUT.write_text(nbf.writes(nb))
print("wrote", OUT)
