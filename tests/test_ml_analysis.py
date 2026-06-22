#!/usr/bin/env python3
"""Behavioral tests for the Phase-4 ML companion (notebooks/ml_analysis.py).

These tests are runtime contracts, not unit-mocks: they import the companion and
exercise AI-03 (anomaly detection) and AI-04 (break-even) against the real cached
CSVs, then assert the verdict-sharpening / whitelist / break-even invariants the
plan requires. They run with no Dune key and no network access.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "notebooks" / "ml_analysis.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("ml_analysis", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ml_analysis"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load_module()


# --------------------------------------------------------------------------- #
# AI-03 — anomaly detection
# --------------------------------------------------------------------------- #
def test_anomaly_function_exists(mod):
    assert hasattr(mod, "run_anomaly_detection"), "AI-03 entry point missing"


def test_anomaly_whitelists_100m_week_and_flags_wallets(mod):
    df = mod.load_holder_features()
    entities = mod.load_entity_labels()
    as_of = mod.holder_features_as_of()
    res = mod.run_anomaly_detection(df, entities, as_of)

    # The 100M burn week (2025-12-22) must be whitelisted, not reported as an anomaly.
    assert res["whitelisted_week"].startswith("2025-12-22")
    assert res["whitelisted_week"] not in res["other_anomalous_weeks"]

    # WR-04: exactly ONE week (the 2025-12-22 100M event) is whitelisted — a too-broad
    # prefix that swept in extra weeks would inflate this count and silently shrink the
    # judged set.
    assert res["n_whitelisted"] == 1

    # Wallet anomalies must be flagged, each carrying an entity label + insight.
    assert len(res["flagged_wallets"]) >= 1
    for w in res["flagged_wallets"]:
        assert "addr" in w and "entity" in w and "insight" in w
        assert isinstance(w["insight"], str) and len(w["insight"]) > 0

    # Anomaly figure must be written.
    assert Path(res["figure"]).exists()


# --------------------------------------------------------------------------- #
# AI-02 — clustering (WR-04: pin k-selection + archetype labeling)
# --------------------------------------------------------------------------- #
def test_clustering_selects_k_and_labels_whale(mod):
    df = mod.load_holder_features()
    entities = mod.load_entity_labels()
    as_of = mod.holder_features_as_of()
    res = mod.run_clustering(df, entities, as_of)

    # k is selected by silhouette inside the configured 3..6 range, and the chosen
    # solution must clear a minimum separation bar (not a degenerate clustering).
    assert 3 <= res["chosen_k"] <= 6
    assert res["chosen_silhouette"] >= 0.25

    # The archetype set must include a "whale" cluster, and the known Uniswap Treasury
    # address (a large custodial holder) must land in it — the StandardScaler-before-KMeans
    # pipeline should separate the high-balance whale cluster cleanly.
    assert "whale" in set(res["archetypes"].values())
    assert res["archetypes"][res["treasury_cluster"]] == "whale"

    # Reviewer-specified 6-archetype scheme: at k=6 the labels must be drawn from
    # exactly {whale, active, retail-high, retail-mid, retail-low, dormant} and the
    # 'whale' / 'dormant' anchor tiers must both be present (not collapsed away).
    allowed = {"whale", "active", "retail-high", "retail-mid", "retail-low", "dormant"}
    assigned = set(res["archetypes"].values())
    assert assigned <= allowed, f"unexpected archetype label(s): {assigned - allowed}"
    if res["chosen_k"] == 6:
        assert assigned == allowed, f"expected all 6 archetypes at k=6, got {assigned}"


# --------------------------------------------------------------------------- #
# AI-04 — break-even model
# --------------------------------------------------------------------------- #
def test_breakeven_function_exists(mod):
    assert hasattr(mod, "run_breakeven"), "AI-04 entry point missing"


def test_breakeven_calibration_reproduces_headline_burn(mod):
    """WR-04: the calibrated blended take must reproduce the headline annualized burn
    (~16,368,222 UNI/yr) — a regression in LP_FEE_RATE, the volume window, or the
    USD->UNI conversion chain would break this even if the threshold stayed positive."""
    as_of = mod.holder_features_as_of()
    res = mod.run_breakeven(as_of)

    assert res["repro_burn_uni"] == pytest.approx(16_368_222, rel=1e-4)
    assert res["repro_burn_uni"] == pytest.approx(res["observed_ann_burn_uni"], rel=1e-6)
    # The calibrated effective take is a period-conditioned rate, clipped to [0, 0.30].
    assert 0.0 < res["take_fraction"] <= 0.30


def test_breakeven_two_scenarios_and_threshold(mod):
    as_of = mod.holder_features_as_of()
    res = mod.run_breakeven(as_of)

    # Scenario (b): a positive daily-volume USD break-even threshold.
    assert res["breakeven_daily_volume_usd_b"] > 0

    # Scenario (a): issuance 0 => already net-deflationary at any positive volume.
    assert res["issuance_a_uni_per_yr"] == 0
    assert res["headroom_a"] is not None

    # Scenario (b) issuance ~ 37.88M UNI/yr (2% tail + 20M growth).
    assert 35_000_000 <= res["issuance_b_uni_per_yr"] <= 40_000_000

    # No price prediction: the only price is the static cached spot.
    assert res["uni_price_usd"] == pytest.approx(3.03, rel=0.01)

    # Break-even figure must be written.
    assert Path(res["figure"]).exists()


def test_three_sharpens_the_verdict_sentences():
    text = MODULE_PATH.read_text()
    assert text.count("Sharpens the verdict:") >= 3
